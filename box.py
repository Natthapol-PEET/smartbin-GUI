import RPi.GPIO as GPIO
import time

servoPOW = 6
servoPIN = 26
lightPIN = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
GPIO.setup(servoPOW, GPIO.OUT)
GPIO.setup(lightPIN, GPIO.OUT)

def move():
    GPIO.output(servoPOW, True)
    p = GPIO.PWM(servoPIN, 50)
    p.start(6.9)
    p.ChangeDutyCycle(3.5)
    time.sleep(1)
    p.stop()
    
def close():
    p = GPIO.PWM(servoPIN, 50)
    p.start(3.5)
    p.ChangeDutyCycle(6.9)
    time.sleep(1)
    p.stop()
    GPIO.output(servoPOW, False)
    
def off_light():
    GPIO.output(lightPIN, False)

def on_light():
    GPIO.output(lightPIN, True)
    time.sleep(1)

'''
 Production Code
'''

'''
import RPi.GPIO as GPIO
import time

servoPIN = 26
lightPIN = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
GPIO.setup(lightPIN, GPIO.OUT)

def move():
    p = GPIO.PWM(servoPIN, 50)
    p.start(8.0)
    p.ChangeDutyCycle(3.5)
    time.sleep(1)
    p.stop()
    
def close():
    p = GPIO.PWM(servoPIN, 50)
    p.start(3.5)
    p.ChangeDutyCycle(8.0)
    time.sleep(1)
    p.stop()
    
def off_light():
    GPIO.output(lightPIN, False)

def on_light():
    GPIO.output(lightPIN, True)
'''
'''
 Develop Code
'''

# def move():
#     print("move")

# def close():
#     print("close")

# def off_light():
#     print("off_light")

# def on_light():
#     print("on_light")

