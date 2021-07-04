
import cv2
import numpy as np

cap = cv2.VideoCapture('NSC2020.mp4')

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('NSC2020_resize.mp4',fourcc, 30, (800, 480))

while True:
    ret, frame = cap.read()
    if ret == True:
        b = cv2.resize(frame, (800, 480),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
        out.write(b)
    else:
        break
    
cap.release()
out.release()
cv2.destroyAllWindows()


