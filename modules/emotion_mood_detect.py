from tensorflow.keras.models import load_model
import cv2
import numpy as np
from django.conf import settings
from emotion_detector.apps import EmotionDetectorConfig 
from mood_detector.apps import MoodDetectorConfig
from collections import defaultdict

emotions = settings.EMOTION_LISTS
moods = settings.MOOD_LISTS

def emotion_mood_detect(image, faces, top_data, all_data):
	if image is not None and faces is not None and len(faces) > 0:
		for face in faces:
			try:
				left, up, right, bottom = face[0], face[1], face[2], face[2]
				roi = image[up:bottom, left:right]
				roi = cv2.resize(roi, (200, 200), interpolation = cv2.INTER_AREA)
				output = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
				temp_output = output / 255.
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


				cv2.rectangle(image, (left, up), (right, bottom), green, thickness=line_thick)
				cv2.putText(image, "{}: {}% - {}: {}%".format(top_data[0], top_data[1], top_data[2], top_data[3]), (int(left), int(up)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
			except:
				pass

	return image