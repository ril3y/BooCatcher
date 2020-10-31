import io
import random
import picamera
import time
from picamera import PiCamera
from pubsub import pub
from threading import Thread

class CoffinCamera(object):
    
    # self.camera = PiCamera()
    # self.camera.resolution=(1024,768)
    # self.camera.annotate_background = picamera.Color('black')
    # self.camera.start_preview()
    def __init__(self  ):
        print("[#] Camera Started")
        self.res = (800, 600)
        self.time_buffer = 20
        self.camera = None
        self.state = True
        self.TAKE_PICTURE = False
        self.WRITE_VIDEO = False
        self.frames = 30

        self.camera = PiCamera()
        self.camera.resolution = self.res
        self.camera.annotate_background = picamera.Color('black')
        
        pub.subscribe(self.camera_listener, 'CAMERA-MESSAGES')


        # self.recording_thread = Thread(target=self.start_recording() )
        # self.recording_thread.start()
        #self.start_recording()
         #Kick off the video recording to memory
        
        
    def camera_listener(self, msg=None):
        print("Got pysub message in CoffinCamera")
        self.TAKE_PICTURE = True
        self.WRITE_VIDEO = True
        if msg == "picture":
            for i in range(0,5): #snap 5 pictures
                print("Picture saved as: %s" % self.capture_image())
        elif msg == "video":
            pass
            #TODO
            
    def capture_image(self, filename=None):
         if not filename:
             filename = (time.ctime().replace(" ","-").replace(":","-")+".jpg")
         self.camera.capture('static/images/' + filename)
         return filename

    # def stop_recording(self):
    #     self.state = False

    # def write_video(self ):
    #     print('Writing video!')
    #     with self.stream.lock:
    #         # Find the first header frame in the video
    #         for frame in self.stream.frames:
    #             if frame.frame_type == picamera.PiVideoFrameType.sps_header:
    #                 self.stream.seek(frame.position)
    #                 break
    #         # Write the rest of the stream to disk
    #         _name = time.ctime().replace(" ","-").replace(":","-")+".motion.h264"
    #         with io.open('./video/'+_name, 'wb') as output:
    #             output.write(self.stream.read())
    #         self.camera.stop_recording()

    # def write_now(self):
    #     # Randomly return True (like a fake motion detection routine)
    #     return random.randint(0, 10) == 0

    
    # def filenames(self):
    #     frame = 0
    #     while frame < self.frames:
    #         yield 'static/images/image%02d.jpg' % frame
    #         frame += 1

    # def start_recording(self):
    #     print("Recording started to mem circular buffer")
    #     self.state = True #Enabled recording
    #     with picamera.PiCamera() as self.camera:
    #         self.stream = picamera.PiCameraCircularIO(self.camera, seconds=20)
    #         self.camera.resolution = self.res
    #         self.camera.start_recording(self.stream, format='h264')
    #         try:
    #             while self.state:
    #                 self.camera.wait_recording(1)
    #                 #Process Still Frames
    #                 if self.TAKE_PICTURE:
    #                     print("Taking Picutres...")
    #                     start = time.time()
    #                     self.camera.capture_sequence(self.filenames(), use_video_port=True)
    #                     finish = time.time()
    #                     print('Captured %d frames at %.2ffps' % (self.frames, self.frames / (finish - start)))
    #                     # for i in range(0,5):
    #                     #     filename = (time.ctime().replace(" ","-").replace(":","-")+".jpg")
    #                     #     self.camera.capture('static/images/' + filename, use_video_port=True)
    #                     self.TAKE_PICTURE = False

    #                 if self.WRITE_VIDEO:
    #                     print("Capturing additional 10 seconds of video...")
    #                     # Keep recording for 10 seconds and only then write the
    #                     # stream to disk
    #                     self.WRITE_VIDEO = False
    #                     self.camera.wait_recording(10)
    #                     self.write_video()
                    
    #         finally:
    #             self.camera.stop_recording()   


if __name__ == "__main__":
    cc  = CoffinCamera(20)
    cc.start_recording()
