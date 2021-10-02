import cv2
import time
import requests
from _smartbinAPI import prediction_donate, prediction_login
import config
import os
import time

class micro_control:
    def create_imgname(self):
        seconds = time.time()
        imgname = str(seconds).split('.')[0] + '.jpg'

        return imgname

    def cap_image(self):
        print("cap image")
        imgname = self.create_imgname()
        
        cap = cv2.VideoCapture(config.camera_index)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        #cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        cap.set(cv2.CAP_PROP_EXPOSURE, 25)
        
        cnt = 0
        while cnt < 5:
            ret, frame = cap.read()
            cnt += 1
        
        
        # ret, frame = cap.read()

        if ret:
            image_origin = 'image/' + 'origin-' + imgname.split('.')[0] + '.jpg'
            cv2.imwrite(image_origin, frame)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            image_grey = 'image/' + 'grey-' + imgname
            cv2.imwrite(image_grey, gray)
        else:
            image_grey = -1
            image_origin = -1
        '''
        
        image_origin = 'image/' + 'origin-' + imgname.split('.')[0] + '.jpg'
        image_grey = 'image/' + 'grey-' + imgname
        os.system('sudo fswebcam -S 20 --no-banner -d /dev/video1 -r 1280x720 ' + image_origin)
        os.system('sudo fswebcam -S 20 --no-banner -d /dev/video1 -r 1280x720 ' + image_grey)
        '''
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
            else:
                response = prediction_login(image_origin, AccessToken)

            if response == 404:
                return 404, 404, 404

            id = response.json()['id']

            print(f"id: {id}")

        return id, image_grey, image_origin

    
# img_name, imgname_origin = micro_control().cap_image()
