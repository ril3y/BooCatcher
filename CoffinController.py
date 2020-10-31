import asyncio
import datetime as dt
import argparse
import _thread
import sys,os
import datetime

from CoffinLED import CoffinLED
from CoffinWeb import CoffinWebServer
from CoffinCamera import CoffinCamera
from CoffinCamera import CoffinCamera
from CoffinSound import CoffinSoundManger
from CoffinMotion import CoffinMotion

from colors import *
from multiprocessing import Process
from threading import Thread

from random import randint
import random
from time import sleep
lightning_delay = [.03, .01, .02, .04]
SLEEP_TIME = .025
import json

from pubsub import pub





class CoffinController(object):

    def __init__(self):
        self.led = CoffinLED()
        #_thread.start_new_thread( self.capture_camera_frames,( 2, ) )

        self.sound = CoffinSoundManger()
        self.motion = CoffinMotion()
        self.camera = CoffinCamera()  

   
        #_thread.start_new_thread(CoffinWebServer(__name__).run(host= '0.0.0.0'),2)
        # self.camera = CoffinCamera()
        # Camthread1 = Thread(target=self.camera.start_recording)
        # Camthread1.start()

        

        #Setup Pub Sub Subscriptions 
        # pub.subscribe(self.listener1, 'rootTopic')
        # pub.subscribe(self.led_listener, 'LED')

        # pub.subscribe(self.websocket_listener, 'ws')     

        #self.coffin_camera = CoffinCamera(20)
        #self.coffin_camera.start_recording()

    def listener(self, cmd, args):
        print('Function listener received:')
        print('  cmd =', cmd)
        print('  args =', args)

        if cmd == "ACTIVE_CHECK":
            pass
    
    def websocket_listener(self, message):
        print('Function websocket_listener received:')
        print('MESSAGE =', message)

    def run(self):
        print("[#] Starting Boo Detection!")
        self.led.set_strip_color((255,0,0))
        CoffinWebServer(__name__).run(host= '0.0.0.0')
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CoffinController')
    parser.add_argument('-c', '--close', action='store_true',     help="Closes Coffin")
    parser.add_argument('-o', '--open', action='store_true',     help="Opens Coffin")
    parser.add_argument('-r', '--run', action='store_true',     help="Runs Coffin")
    
    try:
        args = parser.parse_args()
    except Exception as e:
        print(e)

    if args.close:
        CoffinController.motion.close_coffin()
    elif args.run:
        CoffinController().run()
