import os
# Audio setting
# os.environ['KIVY_AUDIO'] = 'sdl2'
# os.environ['KIVY_VIDEO'] = 'sdl2'

import kivy 
from kivy.app import App
kivy.require('1.9.0')

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.uix.image import Image
from kivy.uix.video import Video
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
# to change the kivy default settings we use this module config
from kivy.config import Config
  
# 0 being off 1 being on as in true / false
# you can use 0 or 1 && True or False
# Config.set('graphics', 'resizable', True)

import threading

from DateTime import get_date, get_time, \
    get_start_time, calculate_time, create_timeout

# from database import DataBase
from micro_control import micro_control
# from firebase_storage import upload_preds, upload_origin

from _smartbinAPI import login_uname, login_qrCode, get_qrcode_accessTK, \
                            decode_token, get_data_type

from config import input_data_len

from manageTinyDB import update_access_token, get_user_token, \
    get_date_time, get_data_pie, update_data_type, get_calculate_point, \
        get_data_type_from_db, update_data_pie, reset_db, get_cc

from box import move, close, off_light, on_light
from detect_object import isHaveObject
from send_to_arduino import check_before_send

from sound import play_sound, play_video_create, stop_video_create

# Hide mouse cursor on desktop
Window.show_cursor = False

# Full Screen
Window.fullscreen = True
# Window.fullscreen = 'auto'

# Set windows size
Window.size = (800, 480)

# class library
mc = micro_control

# count time out
start_time = get_start_time()
timeout = create_timeout()

# current screen
current_screen = ""


def alert_popup(desc):
    layout = GridLayout(cols = 1, padding = 10)
  
    popupLabel = Label(text = desc)
    closeButton = Button(text = "Back to Main page")

    layout.add_widget(popupLabel)
    layout.add_widget(closeButton)       

    # Instantiate the modal popup and display
    popup = Popup(title ='Alert',
                    content = layout,
                    size_hint =(None, None), size =(400, 200),
                    separator_color=[47 / 255., 167 / 255., 212 / 255., 1.])  
    popup.open()   

    # Attach close button press with popup.dismiss action
    closeButton.bind(on_press=popup.dismiss, state=callback) 

def callback(instance, value):
    sm.transition.direction = "right"
    sm.current = "HomeScreen"


# class video_screen(Screen, Video):
#     state = StringProperty()

#     def on_enter(self, *args):
#         self.state = "play"
    
#     def btn_click(self):
#         sm.transition.direction = "right"
#         sm.current = "HomeScreen"
#         # stop video
#         self.state = "stop"
#         # stop_video_create()


screen_net = False

class NetworkError(Screen):
    def on_enter(self, *args):
        global screen_net
        screen_net = True

        self.SCI = Clock.schedule_interval(self.ping_host, 3)

    def ping_host(self, dt):
        hostname = "kusesmartbin.csc.ku.ac.th"
        response = os.system("ping -c 1 " + hostname)

        if response == 0:
            sm.transition.direction = "right"
            sm.current = "HomeScreen"

    def on_leave(self):
        self.SCI.cancel()
            


class thank_screen(Screen):
    def my_callback(self, dt):
        sm.transition.direction = "right"
        sm.current = "HomeScreen"

    def on_enter(self, *args):
        play_sound('Audacity/17-ขอบคุณค่ะ.wav')
        Clock.schedule_once(self.my_callback, 6)


class PointScreen(Screen):
    total_point = StringProperty()

    def on_enter(self, *args):
        play_sound('Audacity/15-คะแนนสะสมครั้งนี้.wav')
        # get calculate point from db
        # show point total to screen
        self.total_point = get_calculate_point()

        # close box
        # close()

    def btn_home(self):
        # play_sound('Audacity/16-ยืนยัน.wav')
        sm.transition.direction = "left"
        sm.current = "thank_screen"

class ProcessScreen1(Screen):
    Date = StringProperty(get_date())
    Time = StringProperty(get_time())
    User = StringProperty(None)
    can_pie = StringProperty(0)
    pet_pie = StringProperty(0)
    plastic_pie = StringProperty(0)
    trash_pie = StringProperty(0)
    sum_pie = StringProperty(0)
    time_left = StringProperty('14.19')

    def on_enter(self, *args):
        play_sound('Audacity/14-กำลังประมวลผล.wav')
        # get user from db
        self.User, _ = get_user_token()

        # get time from db
        # self.Time, self.Date = get_date_time()
        # reload datetime
        Clock.schedule_interval(self.update_datetime, 10)

        # get data pie from db
        self.can_pie, self.pet_pie, self.plastic_pie, \
            self.trash_pie, self.sum_pie = get_data_pie()

        # reload timeout
        Clock.schedule_interval(self.calculate_timeout, 1)

    def calculate_timeout(self, dt):
        global start_time, timeout
        self.time_left = calculate_time(start_time, timeout)

        if self.time_left == '00:00':
            sm.transition.direction = "left"
            sm.current = "thank_screen"

    def update_datetime(self, dt):
        self.Date = get_date()
        self.Time = get_time()


class ReadyScreen1(Screen):
    # ready_text = StringProperty("กดปุ่มแลกขยะ\nเพื่อเริ่มทำงาน ...")
    User = StringProperty(None)
    Date = StringProperty(get_date())
    Time = StringProperty(get_time())
    can_pie = StringProperty(0)
    pet_pie = StringProperty(0)
    plastic_pie = StringProperty(0)
    trash_pie = StringProperty(0)
    sum_pie = StringProperty(0)
    time_left = StringProperty('14.30')

    def __init__(self,**kwargs):
        super(ReadyScreen1, self).__init__(**kwargs)

    # def on_enter(self, *args):
    #     self.ready_text = "กดปุ่มแลกขยะ\nเพื่อเริ่มทำงาน ..."
        
    #     # get user and access token in db
    #     self.User, self.AccessToken = get_user_token()

    #     # reload datetime
    #     Clock.schedule_interval(self.update_datetime, 10)

    #     # reload timeout
    #     Clock.schedule_interval(self.calculate_timeout, 1)

    
    def on_enter(self, *args):
        # if self.sum_pie != "0":
        play_sound('Audacity/13-พร้อมทำงาน.wav')

        self.User, self.AccessToken = get_user_token()

        # reload datetime
        Clock.schedule_interval(self.update_datetime, 10)

        # reload timeout
        Clock.schedule_interval(self.calculate_timeout, 1)

        # get data type from db
        self.can_pie, self.pet_pie, self.plastic_pie, \
            self.trash_pie, self.sum_pie = get_data_pie()


    def calculate_timeout(self, dt):
        global start_time, timeout
        self.time_left = calculate_time(start_time, timeout)

        if self.time_left == '00:0':
            sm.transition.direction = "left"
            sm.current = "thank_screen"

    def update_datetime(self, dt):
        self.Date = get_date()
        self.Time = get_time()

    def micro_working(self):
        move()
        # detect object
        state = isHaveObject()
        print(f"state: {state}")

        # close box
        close()

        if state == 1:
            # prediction
            self.id, self.image_grey, self.image_origin = micro_control().prediction(self.AccessToken)

            if self.id == 404:
                sm.transition.direction = "left"
                sm.current = "NetworkError"
            
            if self.image_grey == -1:
                alert_popup("Camera not responding \nPlease contact the relevant staff.")
            else:
                # remove image origin and gray
                os.remove(self.image_origin)
                os.remove(self.image_grey)

                if self.id == -1:   # server not response
                    alert_popup("Server not responding \nPlease make a new transaction later.")
                else:
                    # update data in db and update value screen
                    self.caned_pie, self.pet_pie, self.plastic_pie, self.trash_pie, \
                        self.sum_pie = update_data_pie(self.id)

                    # ส่ง id ไปยัง arduino
                    serial_state = check_before_send(self.id)

                    if not serial_state:
                        # Error
                        alert_popup("Serial Error\nPlease contact the relevant staff.")

                    # open box
                    # move()

                self.endprocess()

        elif state == 0:
            self.endprocess()
        else:
            # Error
            alert_popup("Camera not responding \nPlease contact the relevant staff.")

    def collect(self):
        # update date/time on screen
        self.Date = get_date(); self.Time = get_time()
        self.startprocess()
        threading.Thread(target=self.micro_working).start()
        play_sound('Audacity/13-พร้อมทำงาน.wav')


    def startprocess(self):
        sm.transition.direction = "left"
        sm.current = "ProcessScreen1"
    
    def endprocess(self):
        self.reset()
        sm.transition.direction = "right"
        sm.current = "ReadyScreen1"

    def reset(self):
        # reset value screen
        self.can_pie = "0"
        self.pet_pie = "0"
        self.plastic_pie = "0"
        self.trash_pie = "0"
        self.sum_pie = "0"

    def lookscore(self):
        play_sound('Audacity/12-ดูคะแนน.wav')

        # ปิดไฟ
        off_light()

        self.reset()
        sm.transition.direction = "left"
        sm.current = "PointScreen"


class EnterIDScreen(Screen):
    sid = StringProperty()

    def __init__(self,**kwargs):
        super(EnterIDScreen, self).__init__(**kwargs)
        self.std_len = input_data_len

    def one(self):
        if len(self.sid) < self.std_len:
            self.sid += '1'

    def two(self):
        if len(self.sid) < self.std_len:
            self.sid += '2'

    def three(self):
        if len(self.sid) < self.std_len:
            self.sid += '3'

    def four(self):
        if len(self.sid) < self.std_len:
            self.sid += '4'

    def five(self):
        if len(self.sid) < self.std_len:
            self.sid += '5'

    def six(self):
        if len(self.sid) < self.std_len:
            self.sid += '6'

    def seven(self):
        if len(self.sid) < self.std_len:
            self.sid += '7'

    def eight(self):
        if len(self.sid) < self.std_len:
            self.sid += '8'

    def nine(self):
        if len(self.sid) < self.std_len:
            self.sid += '9'

    def zero(self):
        if len(self.sid) < self.std_len:
            self.sid += '0'

    def delete(self):
        play_sound('Audacity/9-ลบ.wav')

        stdOddlen = len(self.sid)
        if stdOddlen != 0:
            self.sid = self.sid[0: stdOddlen-1]

    def ok(self):
        global start_time

        play_sound('Audacity/10-ตกลง.wav')

        # login by student id -> get access token
        access_token = login_uname( 'b' + self.sid )

        if access_token == 404:
            sm.transition.direction = "left"
            sm.current = "NetworkError"

        # update user to db
        update_access_token(self.sid, access_token)

        if access_token == -1:
            sm.transition.direction = "left"
            sm.current = "InvalidScreen"
        else:
            sm.transition.direction = "left"
            sm.current = "ReadyScreen1"

            start_time = get_start_time()
        
        # reset student id from screen
        self.sid = ''

    def btn_back(self):
        play_sound('Audacity/4-ย้อนกลับ.wav')
        self.sid = ''
        sm.transition.direction = "right"
        sm.current = "LoginScreen"


class QRcodeScreen(Screen):
    def __init__(self,**kwargs):
        super(QRcodeScreen, self).__init__(**kwargs)
        self.image = Image(source='login_qrCode.png')
        self.add_widget(self.image)

    # come in screen
    def on_enter(self):
        # reload image
        self.QRcodeScreen_updatePic = Clock.schedule_interval(self.update_pic, 0.1)
        # request get qr-code image
        self.QRcodeScreen_getQr = Clock.schedule_interval(self.get_qrCode, 15)
        # request get qr-code image
        self.QRcodeScreen_getAccess = Clock.schedule_interval(self.get_qrcode_accessTK, 1)

    # back
    def on_leave(self):
        # cancel time interval
        self.QRcodeScreen_updatePic.cancel()
        self.QRcodeScreen_getQr.cancel()
        self.QRcodeScreen_getAccess.cancel()

    def get_qrcode_accessTK(self, dt):
        global start_time
        access_token = get_qrcode_accessTK()

        if access_token == 404:
            sm.transition.direction = "left"
            sm.current = "NetworkError"

        if access_token != -1:
            # decode user from access token
            uname = decode_token(access_token)
            # update user in db
            update_access_token(uname, access_token)

            sm.transition.direction = "left"
            sm.current = "ReadyScreen1"

            start_time = get_start_time()

            # cancel time interval (stop reload qr-code)
            self.QRcodeScreen_updatePic.cancel()
            self.QRcodeScreen_getQr.cancel()
            self.QRcodeScreen_getAccess.cancel()


    def update_pic(self, dt):
        # reload qr-code every 15 minute
        self.image.reload()

    def get_qrCode(self, dt):
        statusCode = login_qrCode()

        if statusCode == 404:
            sm.transition.direction = "left"
            sm.current = "NetworkError"

    def btn_back(self):
        play_sound('Audacity/4-ย้อนกลับ.wav')
        sm.transition.direction = "right"
        sm.current = "LoginScreen"


class InvalidScreen(Screen):
    def btn_back(self):
        play_sound('Audacity/4-ย้อนกลับ.wav')
        sm.transition.direction = "right"
        sm.current = "EnterIDScreen"


class LoginScreen(Screen):
    def btn_byQRcode(self):
        play_sound('Audacity/7-scan-QR-Code.wav')
        # load qr-code from smartbin api 
        statusCode = login_qrCode()

        if statusCode == 404:
            sm.transition.direction = "left"
            sm.current = "NetworkError"

        sm.transition.direction = "left"
        sm.current = "QRcodeScreen"

    def btn_byID(self):
        play_sound('Audacity/8-ป้อนรหัสนิสิต.wav')
        sm.transition.direction = "left"
        sm.current = "EnterIDScreen"

    def btn_back(self):
        play_sound('Audacity/4-ย้อนกลับ.wav')
        sm.transition.direction = "right"
        sm.current = "ExScreen"


class HowToScreen(Screen):
    def btn_back(self):
        play_sound('Audacity/4-ย้อนกลับ.wav')
        sm.transition.direction = "right"
        sm.current = "MenuScreen"


class ExScreen(Screen):
    def on_enter(self):
        # off LED
        off_light()

    def btn_collect(self):
        play_sound('Audacity/5-สะสมแต้ม.wav')

        # on LED
        on_light()

        sm.transition.direction = "left"
        sm.current = "LoginScreen"

    def btn_donate(self):
        global start_time

        play_sound('Audacity/6-บริจาค.wav')
        
        # on LED
        on_light()

        # update user in db
        update_access_token('donate', 'donate')

        sm.transition.direction = "left"
        sm.current = "ReadyScreen1"

        start_time = get_start_time()
        
    def btn_back(self):
        play_sound('Audacity/4-ย้อนกลับ.wav')
        sm.transition.direction = "right"
        sm.current = "MenuScreen"


class MenuScreen(Screen):
    can_point = StringProperty(0)
    pet_point = StringProperty(0)
    plastic_point = StringProperty(0)
    trash_point = StringProperty(0)

    def __init__(self,**kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.update_points_screen()


    def update_points_screen(self):
        # get data type from db
        data_list = get_data_type_from_db()

        # update data to screen
        for elem in data_list:
            if elem["id"] == 0:
                self.can_point = '  ' + elem["class"] + '\n' + str(elem["points"]) + ' คะแนน'
            elif elem["id"] == 1:
                self.pet_point = elem["class"] + '\n  ' + str(elem["points"]) + ' คะแนน'
            elif elem["id"] == 2:
                self.plastic_point = elem["class"] + '\n' + str(elem["points"]) + ' คะแนน'
            elif elem["id"] == 3:
                self.trash_point = '   ' +elem["class"] + '\n  '+ str(elem["points"]) + ' คะแนน'


    def on_enter(self, *args):
        global current_screen
        current_screen = "MenuScreen"

    def btn_ex(self):
        play_sound('Audacity/2-แลกขยะ.wav')
        sm.transition.direction = "left"
        sm.current = "ExScreen"

    def btn_howto(self):
        play_sound('Audacity/3-วิธีใช้.wav')
        sm.transition.direction = "left"
        sm.current = "HowToScreen"

    def btn_back(self):
        play_sound('Audacity/4-ย้อนกลับ.wav')
        sm.transition.direction = "right"
        sm.current = "HomeScreen"


class HomeScreen(Screen):
    can_cc_cap = StringProperty()
    pet_cc_cap = StringProperty()
    plastic_cc_cap = StringProperty()
    trash_cc_cap = StringProperty()

    def __init__(self,**kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        # read capacity form sensor
        cc = get_cc()
        can_cc = cc[0]['can_cc']
        pet_cc = cc[0]['pete_cc']
        plastic_cc = cc[0]['plastic_cc']
        trash_cc = cc[0]['other_cc']

        # update data to screen
        # self.can_cc_cap = ' กระป๋อง '+ '\n   ' + str(can_cc) +' %'
        # self.pet_cc_cap = 'พลาสติกใส ' + '\n     ' + str(pet_cc) +' %'
        # self.plastic_cc_cap = 'ขวดพลาสติกขุ่น' + '\n      ' + str(plastic_cc) +' %'
        # self.trash_cc_cap = '  ขยะทั่วไป '+ '\n    ' + str(trash_cc) +' %'
        self.can_cc_cap = ' กระป๋อง '+ '\n     ' + ('ว่าง' if can_cc < 90 else 'เต็ม')
        self.pet_cc_cap = 'พลาสติกใส ' + '\n       ' + ('ว่าง' if pet_cc < 90 else 'เต็ม')
        self.plastic_cc_cap = 'ขวดพลาสติกขุ่น' + '\n        ' + ('ว่าง' if plastic_cc < 90 else 'เต็ม')
        self.trash_cc_cap = '  ขยะทั่วไป '+ '\n      ' + ('ว่าง' if trash_cc < 90 else 'เต็ม')


    def on_enter(self, *args):
        global current_screen, screen_net

        screen_net = False
        current_screen = "HomeScreen"

        # init data type 
        update_data_type()

        # reset scroe
        reset_db()

        # play video
        self.nsc_sound_cancel = Clock.schedule_once(self.play_video, 4)

        # close box
        close()
        # ปิดไฟ
        off_light()


    def play_video(self, dt):
        if screen_net == False:
            play_video_create('Audacity/NSC2020.wav')


    def btn_start(self):
        self.nsc_sound_cancel.cancel()
        stop_video_create()

        play_sound('Audacity/1-เริ่มใช้งาน.wav')
        sm.transition.direction = "left"
        # sm.transition = NoTransition()
        sm.current = "MenuScreen"


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")

sm = WindowManager()

screens = [HomeScreen(name="HomeScreen"), MenuScreen(name="MenuScreen"),
            ExScreen(name="ExScreen"), HowToScreen(name="HowToScreen"),
            LoginScreen(name="LoginScreen"), QRcodeScreen(name="QRcodeScreen"),
            EnterIDScreen(name="EnterIDScreen"), InvalidScreen(name="InvalidScreen"),
            ReadyScreen1(name="ReadyScreen1"), ProcessScreen1(name="ProcessScreen1"), 
            PointScreen(name="PointScreen"), thank_screen(name="thank_screen"),
            NetworkError(name="NetworkError")]
for screen in screens:
    sm.add_widget(screen)

# init data type 
statusCode = update_data_type()

if statusCode == 404:
    sm.current = "NetworkError"
else:
    sm.current = "HomeScreen"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
