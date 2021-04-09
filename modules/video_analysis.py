#model loading
from modules.landmarks import firstmodify, ifoverborder, finalmodify

#image processing
import cv2
import numpy as np

#extra module
import time
import os

from django.conf import settings
from emotion_detector.apps import EmotionDetectorConfig 
from mood_detector.apps import MoodDetectorConfig
from face_detector.apps import FaceDetectorConfig
from collections import defaultdict

emotions = settings.EMOTION_LISTS
moods = settings.MOOD_LISTS
net = FaceDetectorConfig.net

def video_analysis(video_dir, out_video_dir):
	all_data = defaultdict(lambda : [0.00, 0.00, 0.00, 0.00])

	predicted_emotion = "Neutral"
	original_time = round(time.time(), 2)

	top_data = ["Neutral", "100", "Neutral", "100"]

	cap = cv2.VideoCapture(video_dir)

	frame_width = int(cap.get(3)) 
	frame_height = int(cap.get(4)) 
	size = (frame_width, frame_height)
	out_video = cv2.VideoWriter(out_video_dir, cv2.VideoWriter_fourcc(*'mp4v'), 20.0, size) 

	ret, frame = cap.read()

	while ret:
		(h, w) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(cv2.resize(frame, (200, 200)), 1.0, (200, 200), (104.0, 177.0, 123.0))

		net.setInput(blob)
		detections = net.forward()

		height, width, channels = frame.shape
		green = (0, 255, 0)
		line_thick = round(height/120)
	
		for i in range(0, detections.shape[2]):
			confidence = detections[0, 0, i, 2]
			if confidence > settings.FACE_DETECT_CONFIDENCE:
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				length = detections[0, 0, i, 3:7]

				if length[3] < 1:
					(startX, startY, endX, endY) = box.astype("int")
					startX = max(startX, 0)
					startY = max(startY, 0)

					left, right, up, bottom = firstmodify(startX, endX, startY, endY)
					left, right, up, bottom = ifoverborder(left, right, up, bottom, w, h)
					left, right, up, bottom = finalmodify(left, right, up, bottom)
					
					width = (right - left)
					height = (bottom - up)
					f = 0.3

					left += int ( width * f / 2 )
					right -= int ( width * f / 2 )
					up += int (height * f / 2)
					bottom -= int (height * f / 2)
					
					try:
						roi = frame[up:bottom, left:right]

						time_span = int(round(time.time() - original_time, 2) * 100)

						if (time_span % settings.NUM_FRAMES_TO_DETECT) == 0:
							roi = cv2.resize(roi, (200,200), interpolation = cv2.INTER_AREA)
							output = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
							temp_output = output/255.
							temp_output = np.array([temp_output])

							#emotion
							emotion_predictions = EmotionDetectorConfig.model.predict(temp_output)

							if len(emotion_predictions):
								top_index = np.argmax(emotion_predictions[0])
								top_data[0] = emotions[top_index]
								top_data[1] = str(int(emotion_predictions[0][top_index] * 100))


								for i in range(len(emotions)):
									all_data[emotions[i]][0] += emotion_predictions[0][i]
								all_data["count"][0] += 1.0

								all_data[emotions[top_index]][1] += 1.0
								all_data["count"][1] += 1.0

							#mood
							mood_predictions = MoodDetectorConfig.model.predict(temp_output)

							if len(mood_predictions):
								top_index = np.argmax(mood_predictions[0])
								top_data[2] = moods[top_index]
								top_data[3] = str(int(mood_predictions[0][top_index] * 100))

								for i in range(len(moods)):
									all_data[moods[i]][2] += mood_predictions[0][i]
								all_data["count"][2] += 1.0

								all_data[moods[top_index]][3] += 1.0
								all_data["count"][3] += 1.0

					
						cv2.rectangle(frame, (left, up), (right, bottom), green, thickness = line_thick)	
						cv2.putText(frame, "{}: {}% - {}: {}%".format(top_data[0], top_data[1], top_data[2], top_data[3]), (int(left), int(up)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
					except:
						pass

		out_video.write(frame)
		ret, frame = cap.read()

	cap.release()
	out_video.release()
	cv2.destroyAllWindows()

	return all_data


