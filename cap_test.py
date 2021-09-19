import cv2 

vid = cv2.VideoCapture(0) 

ret, frame = vid.read() 

# cv2.imwrite('image/image_test.jpg', frame)

while 1:
                    cv2.imshow('frame', frame) 
                    if cv2.waitKey(1) & 0xFF == ord('q'): 
                                        break

vid.release() 
cv2.destroyAllWindows() 
