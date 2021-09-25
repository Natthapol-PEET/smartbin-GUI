'''
Production Code
'''

import time
import RPi.GPIO as GPIO
 
GPIO.setmode(GPIO.BCM)
 
GPIO_TRIGGER = 20
GPIO_ECHO = 21
 
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    GPIO.output(GPIO_TRIGGER, True)
 
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
    
    begin_time = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
        if time.time() - begin_time > 1:
            break
 
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
def isHaveObject():
    start_time = time.time()
    
    while True:
        dist = distance()
        print ("Measured Distance = ", dist, " cm")
        time.sleep(1)
        
        if time.time() - start_time > 10:
            return 0
            break
        
        if dist < 23:
            time.sleep(2)
            return 1
            break


'''
Develop Code
'''

# def distance():
# 	import time
# 	time.sleep(3)
# 	return 20
