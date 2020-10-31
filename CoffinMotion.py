
import _thread
import board
import RPi.GPIO as GPIO
from time import sleep
from CoffinCamera import CoffinCamera
from pubsub import pub
import time
import datetime
import os
import sys

from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from threading import Timer
MOTION_PIN = 15
FORWARD_PWM = 12
MOTION_PIN = 15
OPEN_PIN = 26
CLOSE_PIN = 20
ENABLE_RELAY_PIN = 21
COFFIN_OPEN_CLOSE_TIME = 5



class CoffinScheduler(object):
    
    def __init__(self, zipcode, start_time, stop_time):
        self.start_time = self._parse_time(start_time)
        self.stop_time = self._parse_time(stop_time)
        self.zipcode = zipcode
        
        self._is_active_weather = True
        self._is_active_time = True

        owm = OWM('1751e90b69159f768490ae24139d8d3e')
        self.weather_manager = owm.weather_manager()
        self.check_weather()
        self.isTimeActive()
        
        pub.sendMessage("SYSTEM-STATUS", is_active = self.isActive())
        #Start our timer to check weather later
        self.timer = Timer(5400, self.check_weather)
        #self.timer.start()

    def isTimeActive(self):

        _now = datetime.datetime.now()
        if _now.hour < self.stop_time.hour and _now.hour != self.stop_time.hour:
            pass
        elif _now.hour == self.stop_time.hour and _now.minute <= self.stop_time.minute:
            pass
        else:
            print("[! SCHEDULER ! ] Stop Time is preventing the Coffin from going Active.")
            return False


        if _now.hour > self.start_time.hour and _now.hour != self.start_time.hour:
            return True
        elif _now.hour == self.start_time.hour and _now.minute >= self.start_time.minute:
            return True
        else:
            print("[! SCHEDULER ! ] Start Time is preventing the Coffin from going Active.")
            return False

        print("[! SCHEDULER ! ]\tStart-Time: %s \n\t[# SCHEDULER #] Stop-time: %s"% (self.start_time, self.stop_time))
        return False

    def _parse_time(self, time_string):
        #11:45am - IE
        _tmp_time = datetime.datetime.strptime(time_string,'%I:%M%p')
        #print("[#] Parsed Time String: %s" % _tmp_time)
        return _tmp_time 

    def isActive(self):
        if self._is_active_weather and self.isTimeActive():
            return True
        else:
            print("[! SCHEDULER !] Weather is preventing the Coffin from going Active")
            return False

    def check_weather(self):
        print("[# SCHEDULER #] Checking Weather....")
        self.current_weather = self.weather_manager.weather_at_zip_code(self.zipcode, 'us').weather
        
        if(self.current_weather.detailed_status.find('rain') > 0):
                print("[! SCHEDULER !] Weather is preventing Coffing from going Active.\n[! SCHEDULER !] Rain Detected - %s" % self.current_weather.detailed_status)
                self._is_active_weather = False #We got the rain.
                return False
        else:
            return True
        #print(self.current_weather.detailed_status)
        

class CoffinMotion():

    
    def __init__(self):
        self.time_since_last_motion = 0
        self.scheduler = CoffinScheduler('20833', start_time='4:15pm', stop_time='10:30pm')
        self.LOCK  = False #semaphor
        self.initialize_pins()
        self.close_coffin()
        self._isActive = False
        #pub.subscribe(self.listener_status, is_active)
        print("[# COFFIN MOTION #] Motion System ARMED - Waiting for motion...")
   
    #def listener_status(self, is_active)
    #    self._isActive = is_active


    def open_close_coffin(self, delay):
        self.open_coffin()
        sleep(delay)
        self.close_coffin()
        #Releasing Lock
        self.LOCK = False



    def motion_callback(self, channel ):
        if self.LOCK:
            #we are already in a motion callback we must wait.
            #print("Passing lock is set")
            pass
        else:
            now = time.perf_counter()
            if  self.time_since_last_motion == 0:
                self.time_since_last_motion = time.perf_counter()
            else:
                tmp_time = time.perf_counter()
                print("[# COFFIN MOTION # ] Time Since Last Motion: %f Seconds" % ( tmp_time - self.time_since_last_motion))
                self.time_since_last_motion = tmp_time #update the last motion time
            self.LOCK = True
            print(" [# COFFIN MOTION #] LOCK SET")
            print("[! COFFIN MOTION !] Motion Detected! (channel:%s) " % str(channel))
    
            #Send our messages to the other subsystems of the Coffin
            #pub.sendMessage('LED-MESSAGES', color=(255,0,0),  msg="strobe" ) 
            pub.sendMessage("CAMERA-MESSAGES", msg="picture")
            pub.sendMessage('LED-MESSAGES', color=(255,0,0))
            
            if self.scheduler.isActive():
                pub.sendMessage("SOUND-MESSAGES", files=["sounds/lidcreak.mp3","sounds/wickedmalelaugh1.mp3","sounds/nmh_scream1.mp3"])
                self.open_close_coffin()
            else:
                #The system is inactive due to rain or timing
                print("[! COFFIN MOTION ! ] System is in-active... Skipping sounds and motion")


    def open_close_coffin(self):
        delay=(4)
        self.open_coffin()
        sleep(delay)
        self.close_coffin()
        #Releasing Lock
        print("[# COFFIN MOTION #] Releasing LOCK")
        self.LOCK = False

    def initialize_pins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(MOTION_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(OPEN_PIN, GPIO.OUT)
        GPIO.setup(CLOSE_PIN, GPIO.OUT)
        GPIO.setup(ENABLE_RELAY_PIN, GPIO.OUT)
        #Configure Interrupts
        GPIO.add_event_detect(MOTION_PIN, GPIO.RISING, callback=self.motion_callback, bouncetime=20000)


    def close_coffin(self):
        print("Closing the Coffin")
        self._enable_actuator()
        GPIO.output(CLOSE_PIN, GPIO.LOW)
        sleep(.1)
        GPIO.output(OPEN_PIN, GPIO.HIGH)
        sleep(COFFIN_OPEN_CLOSE_TIME)
        self._disable_actuator()
        pub.sendMessage('LED-MESSAGES', color=(0,20,255))

    def open_coffin(self):
        print("Opening the Coffin")
        pub.sendMessage('LED-MESSAGES', color=(255,0,0))
        self._enable_actuator()
        GPIO.output(OPEN_PIN, GPIO.LOW)
        sleep(.1)
        #self.sound_manager.play_open_sound()
        GPIO.output(CLOSE_PIN, GPIO.HIGH)
        sleep(COFFIN_OPEN_CLOSE_TIME)
        self._disable_actuator()

    def _disable_actuator(self):
        GPIO.output(ENABLE_RELAY_PIN, GPIO.LOW)
        
    def _enable_actuator(self):
        GPIO.output(ENABLE_RELAY_PIN, GPIO.HIGH)




if __name__ == "__main__":
    cm = CoffinMotion()
    print("waiting for motion")
    while 1:
        sleep(5)
