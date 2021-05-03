import cv2
import time
import requests
from _smartbinAPI import prediction_donate, prediction_login

class micro_control:
    def create_imgname(self):
        seconds = time.time()
        imgname = str(seconds).split('.')[0] + '.jpg'

        return imgname

    def cap_image(self):
        imgname = self.create_imgname()

        cap = cv2.VideoCapture('http://192.168.0.100:4747/mjpegfeed')          # ios
        # cap = cv2.VideoCapture('http://192.168.43.224:4747/mjpegfeed')    # android
        
        cnt = 0
        while cnt < 10:
            _, frame = cap.read()
            cnt += 1

        image_origin = 'image/' + 'origin-' + imgname.split('.')[0] + '.jpg'
        cv2.imwrite(image_origin, frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        image_grey = 'image/' + 'grey-' + imgname
        cv2.imwrite(image_grey, gray)

        cap.release()
        cv2.destroyAllWindows()

        return image_grey, image_origin

    def prediction(self, AccessToken):
        image_grey, image_origin = self.cap_image()

        # image_grey = 'image/1603470042.jpg' 
        # image_origin = 'image/1603470042.jpg'

        if AccessToken == 'donate':
            response = prediction_donate(image_grey)
            print(response)
        else:
            response = prediction_login(image_grey, AccessToken)

        # id = response.json()['id']
        
        

        # return image_grey, id, image_origin
        return image_grey, 1, image_origin

    
# img_name, imgname_origin = micro_control().cap_image()
