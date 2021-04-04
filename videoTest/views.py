from django.shortcuts import render
import requests
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading


def index_view(request):
    return render(request, 'index.html')

class VideoCamera(object):
    rect = 0
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()
            if self.rect == 1:
                cv2.rectangle(self.frame, (0, 0), (255, 255), (255, 0, 0), 2)
            # How to make rectangle: cv2.rectangle(self.frame, (startX, startY), (endX, endY), Color: (R, G, B), Width)

global_camera = VideoCamera()

def gen(camera):
    i = 0
    while True:
        frame = camera.get_frame()
        i+=1
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def stop_feed(request):
    global_camera.__del__()

def make_rectangle(request):
    global_camera.rect = 1

@gzip.gzip_page
def livefeed(request):
    try:
        cam = VideoCamera()
        global_camera = cam
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace; boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass
