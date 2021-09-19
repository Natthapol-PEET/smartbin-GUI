import os
from time import sleep
from serial import Serial
import json
from _smartbinAPI import update_bin
import json
from manageTinyDB import update_cc

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
    send = f"{id}\n"

    ser.write(send.encode())

    while True:
        output = ser.readline().decode().rstrip()

        if output != "":
            output = output.replace("'", '"')
            output = json.loads(output)
            # [update] send data to server 
            update_bin(output['can'], output['pete'], output['plastic'], output['other'])
            update_cc(output['can'], output['pete'], output['plastic'], output['other'])
            print("output :", output)
            break
        
def check_before_send(id):
    try:
        '''
            Production
        '''
        senddata(id)    
        return True
    except:
        return False