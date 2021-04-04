import os
import cv2
import numpy as np
from modules.landmarks import firstmodify, ifoverborder, finalmodify
from django.conf import settings

DEPLOY_PROTOTXT_TXT = os.path.join(settings.BASE_DIR, settings.DEPLOY_PROTOTXT_TXT)
RES_CAFFE_MODEL = os.path.join(settings.BASE_DIR, settings.RES_CAFFE_MODEL)
net = cv2.dnn.readNetFromCaffe(DEPLOY_PROTOTXT_TXT, RES_CAFFE_MODEL)

def face_detect(image, predicted_emotion):
	faces = []

	if image is not None and net is not None:
		try:
			(h, w) = image.shape[:2]
			blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
			net.setInput(blob)
			detections = net.forward()
		except:
			pass

		height, width, channels = image.shape
		green = (0, 255, 0)
		line_thick = round(height/120)

		if detections is not None:
			for i in range(0, detections.shape[2]):
				confidence = detections[0, 0, i, 2]
				if confidence > 0.75:
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

						faces.append([left, up, right, bottom])

						cv2.rectangle(image, (left, up), (right, bottom), green, thickness=line_thick)
						cv2.putText(image, predicted_emotion, (int(left), int(up)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
						# cv2.putText(image, prediction_result, (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,255), 1)


	return image, faces