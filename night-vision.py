#!/usr/bin/env python
from flask import Flask, render_template, Response
from video_stream import VideoStream
import cv2
import io
import time
import picamera

"""
Video streaming from Raspberry Pi camera.
Use the following URLs to see the video stream:
- local: http://127.0.0.1:5000/
- remote: http://<ip-address-of-raspberry-pi>/5000/
Use the command '$ip a' to get the ip-address.
"""

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming"""
    return render_template('index.html')

def gen():
    """Video streaming"""
    video_stream = VideoStream()
    # Warm-up camera
    # camera.start_preview()
    time.sleep(2)
    video_stream.start()
    while True:
        frame = video_stream.get_frame()
        if not(frame is None):
            ret, jpeg = cv2.imencode('.jpeg', frame)
            yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')



@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
        