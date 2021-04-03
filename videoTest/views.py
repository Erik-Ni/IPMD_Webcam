from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import time
import cv2
import threading

from modules.face_detect import face_detect
from modules.emotion_mood_detect import emotion_mood_detect

def index_view(request):
	return render(request, 'index.html')

class VideoCamera(object):
	def __init__(self):
		self.original_time = round(time.time(), 2)
		self.predicted_emotion = "Neutral"
		self.prediction_result = ""

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

			self.frame, self.faces = face_detect(self.frame, self.predicted_emotion, self.prediction_result)

			time_span = round(time.time(), 2) - self.original_time
			time_span = int(round(time_span, 2) * 100)

			if time_span % 10 == 0:
				self.frame, self.predicted_emotion, self.prediction_result = emotion_mood_detect(self.frame, self.faces, self.predicted_emotion, self.prediction_result)

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield(b'--frame\r\n'
			  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def livefeed(request):
	try:
		cam = VideoCamera()
		return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace; boundary=frame")
	except:  # This is bad! replace it with proper handling
		pass
