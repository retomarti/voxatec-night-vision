import io
import time
from picamera import PiCamera
from picamera.array import PiRGBArray
from threading import Thread



class VideoStream:
    
    def __init__(self, resolution=(800, 600), framerate=25):
        # initialize camera and stream
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)
        # initiallize the frame & status
        self.frame = None
        self.stopped = False
        
        
    def start(self):
        # start thread
        Thread(target=self.read_frames, args=()).start()
        
        
    def read_frames(self):
        # thread to read frames from camera
        for frame in self.stream:
            # grab the frame from the stream and clear stream
            self.frame = frame.array
            self.rawCapture.truncate(0)
            # if thread should be stopped
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return
            
            
    def get_frame(self):
        # return most recently read frame
        return self.frame
    
    
    def stop(self):
        # stop thread
        self.stopped = True
        
        
        