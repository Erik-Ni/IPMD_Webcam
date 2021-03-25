import cv2
import numpy as np
from landmarks import firstmodify, ifoverborder, finalmodify

# define the path to the face detector
DEPLOY_PROTOTXT_TXT = "face_models/deploy.prototxt.txt"
RES_CAFFEMODEL = "face_models/res10_300x300_ssd_iter_140000.caffemodel"
net = cv2.dnn.readNetFromCaffe(DEPLOY_PROTOTXT_TXT, RES_CAFFEMODEL)

def face_detect(image):
	faces = []

	if image is not None and net is not None:
		(h, w) = image.shape[:2]
		blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
		net.setInput(blob)
		detections = net.forward()

		height, width, channels = image.shape
		green = (0, 255, 0)
		line_thick = round(height/120)


		for i in range(0, detections.shape[2]):
			confidence = detections[0, 0, i, 2]
			if confidence > 0.5:
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

	return faces

