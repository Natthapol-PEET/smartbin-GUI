import cv2
import time
import requests
from _smartbinAPI import prediction_donate, prediction_login
import config

class micro_control:
    def create_imgname(self):
        seconds = time.time()
        imgname = str(seconds).split('.')[0] + '.jpg'

        return imgname

    def cap_image(self):
        imgname = self.create_imgname()

        # cap = cv2.VideoCapture(0)   # webcam rpi
        cap = cv2.VideoCapture(config.camera_index)       # android
        # cap = cv2.VideoCapture('http://192.168.43.224:4747/mjpegfeed')    # ios
        
        cnt = 0
        while cnt < 10:
            ret, frame = cap.read()
            cnt += 1

        if ret:
            image_origin = 'image/' + 'origin-' + imgname.split('.')[0] + '.jpg'
            cv2.imwrite(image_origin, frame)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            image_grey = 'image/' + 'grey-' + imgname
            cv2.imwrite(image_grey, gray)
        else:
            image_grey = -1
            image_origin = -1

        cap.release()
        cv2.destroyAllWindows()

        return image_grey, image_origin

    def prediction(self, AccessToken):
        image_grey, image_origin = self.cap_image()

        # image_grey = 'image/1603470042.jpg' 
        # image_origin = 'image/1603470042.jpg'

        if image_grey == -1:
            return -1, -1, -1
        else:
            if AccessToken == 'donate':
                response = prediction_donate(image_origin)
                print(response)
            else:
                response = prediction_login(image_origin, AccessToken)

            id = response.json()['id']

            print(id)

        return id, image_grey, image_origin

    
# img_name, imgname_origin = micro_control().cap_image()
