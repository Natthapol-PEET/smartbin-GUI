import os
from time import sleep
from serial import Serial
import json

def senddata(id):
    port = '/dev/ttyUSB0'
    allport = os.popen('ls /dev/ttyUSB*').read()
    for p in allport.split('\n'):
        if 'ttyUSB_DEVICE1' not in p:
            port = p
            break

    ser = Serial(
            port=port,
            baudrate = 9600,
            timeout = 5
        )

    sleep(2)

    # send = str(input("type : ")) + '\n'
    send = f"type : {id}\n"

    ser.write(send.encode())

    while True:
        output = ser.readline().decode().rstrip()

        if True:
        # if output == ___:
            print("output :", output)
            break
        
def check_before_send(id):
    try:
        senddata(id)
        return True
    except:
        return False