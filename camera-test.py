import picamera
import time

camera = picamera.PiCamera()
try:
    camera.resolution = (1280, 720)
    '''
    camera.start_preview()
    '''
    time.sleep(2)
    camera.capture('frame.jpeg')
finally:
    camera.close()