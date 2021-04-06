from tensorflow.keras.models import load_model
import cv2
import numpy as np
from django.conf import settings
from emotion_detector.apps import EmotionDetectorConfig 

emotions = settings.EMOTION_LISTS

def emotion_mood_detect(image, faces, top_data, all_data):
	if image is not None and faces is not None and len(faces) > 0:
		for face in faces:
			try:
				left, up, right, bottom = face[0], face[1], face[2], face[2]
				roi = image[up:bottom, left:right]
				roi = cv2.resize(roi, (200,200), interpolation = cv2.INTER_AREA)
				output = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
				temp_output = output/255.
				temp_output = np.array([temp_output])

				predictions = EmotionDetectorConfig.model.predict(temp_output)

				if len(predictions):
					top_index = np.argmax(predictions[0])
					top_data[0] = emotions[top_index]
					top_data[1] = str(int(predictions[0][top_index] * 100))

					for i in range(len(emotions)):
						all_data[emotions[i]] += predictions[0][i]
					all_data["count"] += 1

			except:
				pass
			
			cv2.putText(image, "{}: {}%".format(top_data[0], top_data[1]), (int(left), int(up)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

	return image
