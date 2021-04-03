from tensorflow.keras.models import load_model
import cv2
import numpy as np

from emotion_detector.apps import EmotionDetectorConfig 

emotions = ['Anger', 'Contempt', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

def emotion_mood_detect(image, faces, predicted_emotion, prediction_result):
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
					prediction_result = str(predictions[0])
					max_index = np.argmax(predictions[0])
					predicted_emotion = emotions[max_index]
			except:
				pass
			
			cv2.putText(image, predicted_emotion, (int(left), int(up)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
			cv2.putText(image, prediction_result, (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,255), 1)

	return image, predicted_emotion, prediction_result
