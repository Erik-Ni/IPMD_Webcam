from tensorflow.keras.models import load_model
import cv2
import numpy as np

def read_model(model_dir):
	model = load_model(model_dir)
	return model

def emotion_mood_detect(image, model):
	face_predictions = []

	faces = face_detect(image)

	for face in faces:
		left, up, right, bottom = face[0], face[1], face[2], face[2]
		roi = image[up:bottom, left:right]
		roi = cv2.resize(roi, (200,200), interpolation = cv2.INTER_AREA)
		output = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
		temp_output = output/255.
		test_data = np.array([temp_output])
		
		predictions = model.predict(test_data)
		# prediction_result = str(predictions[0])
		# max_index = np.argmax(predictions[0])	
		# predicted_emotion = emotions[max_index]

		face_predictions.append(predictions[0])

	return face_predictions