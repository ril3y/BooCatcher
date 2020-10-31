import pydub
from pydub import AudioSegment
from pydub.playback import play
import os
from random import randint
import _thread
from pubsub import pub
import threading
from time import sleep
from threading import Thread
class CoffinSoundManger():

    def __init__(self):
        self.sounds = []
        self.DAEMON_RUN = True
        self._populate_sound_files()
        self.queue = [] 
        #self.sound_daemon = Thread(target=self.sound_thread, )

        self.sound_daemon = Thread(target=self.sound_thread)
        self.sound_daemon.start()
        
        pub.subscribe(self.sound_listener, 'SOUND-MESSAGES')
   
    """
    Whatever we put (filename of sound in sounds dir) into the 
    self.queue this daemon will check it and then play it instantly
    """

    def stop_sound_daemon(self):
        self.DAEMON_RUN = False

    def sound_thread(self):
        print("[#] Sound Daemon Thread Started")
        while self.DAEMON_RUN:
            sleep(.25)
            if self.queue:
                #process the queue
                _file = self.queue.pop()
                self.play_sound_file(_file)
                

    def _push_file_to_queue(self, filename):
        self.queue.append(filename)

    def sound_listener(self, files):
        print('Function Sound received:')
        for f in files:
            print('  filename =', f)
            self._push_file_to_queue(f)
       
    def play_open_sound(self):
        play(self._get_sound("sounds/lidcreak.mp3"))

    def play_random_sound(self):
        top_index = len(self.sounds)
        current_sound = self.sounds[randint(0, top_index)]
        print("Playing %s " % current_sound)
        _audio = AudioSegment.from_file("sounds/"+current_sound, format="mp3")
        play(_audio)

    def play_sound_file(self, filename):
        print("Attempting to play %s" % filename)
        f = self._get_sound(filename)
        if f:
            play(f)
        

    def _get_sound(self, filename):
        return(AudioSegment.from_file(filename, format='mp3'))

    def _populate_sound_files(self):
        files = os.listdir('sounds')
        for f in files:
            if f.endswith(".mp3"):
                #print("\t[-]Adding %s to the sounds" % f)
                self.sounds.append(f)

if __name__ == "__main__":
    csm = CoffinSoundManger()

    csm.play_sound_file("sounds/wickedmalelaugh1.mp3")
    csm.stop_sound_daemon()