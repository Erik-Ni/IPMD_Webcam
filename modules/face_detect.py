import os
import cv2
import numpy as np
from modules.landmarks import firstmodify, ifoverborder, finalmodify
from django.conf import settings
from face_detector.apps import FaceDetectorConfig

def face_detect(image, top_data):
	faces = []
	net = FaceDetectorConfig.net

	if image is not None and net is not None:
		try:
			(h, w) = image.shape[:2]
			blob = cv2.dnn.blobFromImage(cv2.resize(image, (200, 200)), 1.0, (200, 200), (104.0, 177.0, 123.0))
			net.setInput(blob)
			detections = net.forward()
		except:
			pass

		height, width, channels = image.shape
		green = (0, 255, 0)
		line_thick = round(height / 120)

		if detections is not None:
			for i in range(0, detections.shape[2]):
				confidence = detections[0, 0, i, 2]
				if confidence > settings.FACE_DETECT_CONFIDENCE:
					box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
					len = detections[0, 0, i, 3:7]

					if len[3] < 1:
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

						if left < right and up < bottom:
							faces.append([left, up, right, bottom])
							cv2.rectangle(image, (left, up), (right, bottom), green, thickness = line_thick)
							cv2.putText(image, "{}: {}% - {}: {}%".format(top_data[0], top_data[1], top_data[2], top_data[3]), (int(left), int(up)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

	return image, faces