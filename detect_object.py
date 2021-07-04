'''
import cv2
import time
import numpy as np
import config

image_size = (100, 100)
area_offset = [300, 1500]     # 0 - 10000 (100*100)
timeout = 10000

def background_subtraction():
	# backSub = cv2.createBackgroundSubtractorMOG2()
	backSub = cv2.createBackgroundSubtractorKNN()

	cap = cv2.VideoCapture(config.camera_index)

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

	time.sleep(3)
	return state
	
'''


import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
 
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    GPIO.output(GPIO_TRIGGER, True)
 
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
 

    return distance
 

def background_subtraction():
    start_time = time.time()
    
    while True:
        dist = distance()
        print ("Measured Distance = ", dist, " cm")
        time.sleep(1)
        
        if time.time() - start_time > 10:
            return 0
            break
        
        if dist < 30:
            time.sleep(2)
            return 1
            break
            
'''

def background_subtraction():
	return 1

'''