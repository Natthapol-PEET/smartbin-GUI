import cv2
import time
import numpy as np

image_size = (100, 100)
area_offset = [300, 1500]
timeout = 10000

def background_subtraction():
	# backSub = cv2.createBackgroundSubtractorMOG2()
	backSub = cv2.createBackgroundSubtractorKNN()

	cap = cv2.VideoCapture(0)

	cnt = 0
	start_time = time.time()
	state = None

	while True:
		ret, frame = cap.read()
		
		if ret:
			frame = cv2.resize(frame, image_size)
			fgMask = backSub.apply(frame)
			cnt += 1
			# cv2.imshow('Frame', frame)
			# cv2.imshow('FG Mask', fgMask)

			if cnt > 10:
				whiteArea = 0
				# whiteArea = sum(list(row).count(255) for row in fgMask)
				unique, counts = np.unique(fgMask, return_counts=True)
				np_dict = dict(zip(unique, counts))
				if 255 in np_dict:
					whiteArea = np_dict[255]
					print(whiteArea)
				
				if whiteArea > area_offset[0] and whiteArea < area_offset[1]:
					print(whiteArea)
					state = 1
					break
					
			if time.time() - start_time > timeout:
				state = 0
				break

		else:
			state = -1
			break

	cap.release()
	cv2.destroyAllWindows()

	return state


background_subtraction()