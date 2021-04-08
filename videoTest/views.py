from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from django.conf import settings

import time
import cv2
import threading
from collections import defaultdict

from modules.face_detect import face_detect
from modules.emotion_mood_detect import emotion_mood_detect, load_results_to_posted
from modules.save_logs import print_data_to_file

def index_view(request):
	return render(request, 'index.html')

class VideoCamera(object):
	rect = 0
	def __init__(self):
		self.original_time = time.time()
		self.top_data = ["Neutral", "100", "Neutral", "100"]
		self.all_data = defaultdict(lambda : [0.00, 0.00, 0.00, 0.00])
		self.posted = defaultdict(lambda : dict)

		self.saved_time = 0
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

			self.frame, self.faces = face_detect(self.frame, self.top_data)

			cur_time = time.time()
			ntime_span = int(round(cur_time - self.original_time, 2)  * 100)
			time_span = int(round(cur_time - self.original_time, 0))

			if ntime_span % settings.NUM_FRAMES_TO_DETECT == 0:
				self.frame = emotion_mood_detect(self.frame, self.faces, self.top_data, self.all_data)

			if time_span % settings.NUM_SECONDS_TO_SAVE == 0 and self.saved_time != time_span:
				load_results_to_posted(self.all_data, self.posted)
				print_data_to_file(cur_time, self.posted)
				self.saved_time = time_span

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield(b'--frame\r\n'
			  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_stop(request):
	cv2.rectangle(global_camera.frame, (0, 0), (255, 255), (255, 0, 0), 2)

def make_rectangle(request):
	global_camera.rect = 1

@gzip.gzip_page
def livefeed(request):
	try:
		return StreamingHttpResponse(gen(global_camera), content_type="multipart/x-mixed-replace; boundary=frame")
	except:  # This is bad! replace it with proper handling
		pass

global_camera = VideoCamera()

