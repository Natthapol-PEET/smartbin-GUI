from kivy.app import App
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
import os
import threading

# add sound
from kivy.core.audio import SoundLoader
# sound = SoundLoader.load('Audacity/1-เริ่มใช้งาน.wav').play()
# sound.play()
# sound.stop()

from DateTime import get_date, get_time, \
    get_start_time, calculate_time, create_timeout

# from database import DataBase
from micro_control import micro_control
# from firebase_storage import upload_preds, upload_origin

from _smartbinAPI import login_uname, login_qrCode, get_qrcode_accessTK, \
                            decode_token, update_bin, get_data_type

from config import input_data_len

from manageTinyDB import update_access_token, get_user_token, \
    get_date_time, get_data_pie, update_data_type, get_calculate_point, \
        get_data_type_from_db, update_data_pie, reset_db

# init data type 
update_data_type()

# Hide mouse cursor on desktop
Window.show_cursor = True

# Full Screen
Window.fullscreen = False
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

class video_screen(Screen, Video):
    state = StringProperty()

    # def __init__(self, **kwargs):
    #     super(video_screen, self).__init__(**kwargs)
    #     video = Video(source='NSC2020.mp4', state='play')

    def on_enter(self, *args):
        self.state = "play"
    #     self.video = Video(source="sample_1280x720.mkv")
    #     self.state = "play"
    #     self.option = {'eos' : 'loop'}
    #     self.allow_stretch = True
    #     self.play = True
    
    def btn_click(self):
        sm.transition.direction = "right"
        sm.current = "HomeScreen"
        # stop video
        self.state = "stop"


class thank_screen(Screen):
    def my_callback(self, dt):
        sm.transition.direction = "right"
        sm.current = "HomeScreen"

    def on_enter(self, *args):
        SoundLoader.load('Audacity/17-ขอบคุณค่ะ.wav').play()
        Clock.schedule_once(self.my_callback, 3)


class PointScreen(Screen):
    total_point = StringProperty()

    def on_enter(self, *args):
        self.soundScore = SoundLoader.load('Audacity/15-คะแนนสะสมครั้งนี้.wav')
        self.soundScore.play()
        # get calculate point from db
        # show point total to screen
        self.total_point = get_calculate_point()

    def btn_home(self):
        self.soundScore.stop()
        # SoundLoader.load('Audacity/16-ยืนยัน.wav').play()
        sm.transition.direction = "left"
        sm.current = "thank_screen"


class ProcessScreen2(Screen):
    Date = StringProperty(0)
    Time = StringProperty(0)
    User = StringProperty(None)
    can_pie = StringProperty(0)
    pet_pie = StringProperty(0)
    plastic_pie = StringProperty(0)
    trash_pie = StringProperty(0)
    sum_pie = StringProperty(0)
    time_left = StringProperty('14.19')

    def on_enter(self, *args):
        SoundLoader.load('Audacity/14-กำลังประมวลผล.wav').play()
        # get user from db
        self.User, _ = get_user_token()
        # get date time from db
        self.Time, self.Date = get_date_time()
        # get data type from db
        self.can_pie, self.pet_pie, self.plastic_pie, \
            self.trash_pie, self.sum_pie = get_data_pie()

        # reload timeout
        Clock.schedule_interval(self.calculate_timeout, 1)

    def calculate_timeout(self, dt):
        global start_time, timeout
        self.time_left = calculate_time(start_time, timeout)

        if self.time_left == '00:0':
            sm.transition.direction = "left"
            sm.current = "thank_screen"


class ReadyScreen2(Screen):
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
        super(ReadyScreen2, self).__init__(**kwargs)

    def on_enter(self, *args):
        if self.sum_pie != "0":
            SoundLoader.load('Audacity/13-พร้อมทำงาน.wav').play()
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
        # capture image
        mc = micro_control()
        # prediction
        self.id, self.image_grey, self.image_origin = mc.prediction(self.AccessToken)
        # remove image origin and gray
        os.remove(self.image_origin)
        os.remove(self.image_grey)

        # update data in db and update value screen
        self.caned_pie, self.pet_pie, self.plastic_pie, self.trash_pie, \
            self.sum_pie = update_data_pie(self.id)
    
        self.endprocess()

    def collect(self):
        # SoundLoader.load('Audacity/11-แลกเพิ่ม.wav').play()

        # update date/time on screen
        self.Date = get_date(); self.Time = get_time()
        self.startprocess()
        threading.Thread(target=self.micro_working).start()

    def startprocess(self):
        sm.transition.direction = "left"
        sm.current = "ProcessScreen2"
    
    def endprocess(self):
        sm.transition.direction = "right"
        sm.current = "ReadyScreen2"

    def reset(self):
        # reset screen
        self.glass_pie = "0"
        self.plastic_pie = "0"
        self.can_pie = "0"
        self.sum_pie = "0"

    def lookscore(self):
        SoundLoader.load('Audacity/12-ดูคะแนน.wav').play()

        self.reset()
        sm.transition.direction = "left"
        sm.current = "PointScreen"


class ProcessScreen1(Screen):
    Date = StringProperty(0)
    Time = StringProperty(0)
    User = StringProperty(None)
    can_pie = StringProperty(0)
    pet_pie = StringProperty(0)
    plastic_pie = StringProperty(0)
    trash_pie = StringProperty(0)
    sum_pie = StringProperty(0)
    time_left = StringProperty('14.19')

    def on_enter(self, *args):
        SoundLoader.load('Audacity/14-กำลังประมวลผล.wav').play()
        # get user from db
        self.User, _ = get_user_token()
        # get time from db
        self.Time, self.Date = get_date_time()
        # get data pie from db
        self.can_pie, self.pet_pie, self.plastic_pie, \
            self.trash_pie, self.sum_pie = get_data_pie()

        # reload timeout
        Clock.schedule_interval(self.calculate_timeout, 1)

    def calculate_timeout(self, dt):
        global start_time, timeout
        self.time_left = calculate_time(start_time, timeout)

        if self.time_left == '00:0':
            sm.transition.direction = "left"
            sm.current = "thank_screen"


class ReadyScreen1(Screen):
    ready_text = StringProperty("กดปุ่มแลกขยะ\nเพื่อเริ่มทำงาน ...")
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

    def on_enter(self, *args):
        # get user and access token in db
        self.User, self.AccessToken = get_user_token()

        # reload datetime
        Clock.schedule_interval(self.update_datetime, 10)

        # reload timeout
        Clock.schedule_interval(self.calculate_timeout, 1)

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
        # capture image
        mc = micro_control()
        # prediction
        self.id, self.image_grey, self.image_origin = mc.prediction(self.AccessToken)
        # remove image origin and gray
        os.remove(self.image_origin)
        os.remove(self.image_grey)

        # update data in db and update value screen
        self.caned_pie, self.pet_pie, self.plastic, \
            self.trash_pie, self.sum_pie = update_data_pie(self.id)
    
        self.endprocess()

    def collect(self):
        if self.ready_text == "พร้อมทำงาน ...\n":
            # update date/time on screen
            self.Date = get_date(); self.Time = get_time()
            self.startprocess()
            threading.Thread(target=self.micro_working).start()
        else:
            SoundLoader.load('Audacity/13-พร้อมทำงาน.wav').play()
        self.ready_text = "พร้อมทำงาน ...\n"

    def startprocess(self):
        sm.transition.direction = "left"
        sm.current = "ProcessScreen1"
    
    def endprocess(self):
        self.reset()
        sm.transition.direction = "right"
        sm.current = "ReadyScreen2"

    def reset(self):
        # reset value screen
        self.can_pie = "0"
        self.pet_pie = "0"
        self.plastic_pie = "0"
        self.trash_pie = "0"
        self.sum_pie = "0"

    def lookscore(self):
        SoundLoader.load('Audacity/12-ดูคะแนน.wav').play()

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
        SoundLoader.load('Audacity/9-ลบ.wav').play()

        stdOddlen = len(self.sid)
        if stdOddlen != 0:
            self.sid = self.sid[0: stdOddlen-1]

    def ok(self):
        global start_time

        SoundLoader.load('Audacity/10-ตกลง.wav').play()

        # login by student id -> get access token
        access_token = login_uname( 'b' + self.sid )
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
        SoundLoader.load('Audacity/4-ย้อนกลับ.wav').play()
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
        login_qrCode()

    def btn_back(self):
        SoundLoader.load('Audacity/4-ย้อนกลับ.wav').play()
        sm.transition.direction = "right"
        sm.current = "LoginScreen"


class InvalidScreen(Screen):
    def btn_back(self):
        SoundLoader.load('Audacity/4-ย้อนกลับ.wav').play()
        sm.transition.direction = "right"
        sm.current = "EnterIDScreen"


class LoginScreen(Screen):
    def btn_byQRcode(self):
        SoundLoader.load('Audacity/7-scan-QR-Code.wav').play()
        # load qr-code from smartbin api 
        login_qrCode()

        sm.transition.direction = "left"
        sm.current = "QRcodeScreen"

    def btn_byID(self):
        SoundLoader.load('Audacity/8-ป้อนรหัสนิสิต.wav').play()
        sm.transition.direction = "left"
        sm.current = "EnterIDScreen"

    def btn_back(self):
        SoundLoader.load('Audacity/4-ย้อนกลับ.wav').play()
        sm.transition.direction = "right"
        sm.current = "ExScreen"


class HowToScreen(Screen):
    def btn_back(self):
        SoundLoader.load('Audacity/4-ย้อนกลับ.wav').play()
        sm.transition.direction = "right"
        sm.current = "MenuScreen"


class ExScreen(Screen):
    def btn_collect(self):
        SoundLoader.load('Audacity/5-สะสมแต้ม.wav').play()
        sm.transition.direction = "left"
        sm.current = "LoginScreen"

    def btn_donate(self):
        global start_time

        SoundLoader.load('Audacity/6-บริจาค.wav').play()

        # update user in db
        update_access_token('donate', 'donate')

        sm.transition.direction = "left"
        sm.current = "ReadyScreen1"

        start_time = get_start_time()
        
    def btn_back(self):
        SoundLoader.load('Audacity/4-ย้อนกลับ.wav').play()
        sm.transition.direction = "right"
        sm.current = "MenuScreen"


class MenuScreen(Screen):
    can_point = StringProperty(0)
    pet_point = StringProperty(0)
    plastic_point = StringProperty(0)
    trash_point = StringProperty(0)

    def __init__(self,**kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        # get data type from db
        names, points = get_data_type_from_db()
        
        # update data to screen
        self.can_point = '  ' + names[0] + '\n' + str(points[0]) + ' คะแนน'
        self.pet_point = names[1] + '\n  ' + str(points[1]) + ' คะแนน'
        self.plastic_point = names[2] + '\n' + str(points[2]) + ' คะแนน'
        self.trash_point = names[3] + '\n  '+str(points[3]) + ' คะแนน'

    def on_enter(self, *args):
        global current_screen
        current_screen = "MenuScreen"

    def btn_ex(self):
        SoundLoader.load('Audacity/2-แลกขยะ.wav').play()
        sm.transition.direction = "left"
        sm.current = "ExScreen"

    def btn_howto(self):
        SoundLoader.load('Audacity/3-วิธีใช้.wav').play()
        sm.transition.direction = "left"
        sm.current = "HowToScreen"

    def btn_back(self):
        SoundLoader.load('Audacity/4-ย้อนกลับ.wav').play()
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
        can_cc = 50
        pet_cc = 30
        plastic_cc = 40
        trash_cc = 10

        # update data to screen
        self.can_cc_cap = 'กระป๋อง '+ str(can_cc) +' %'
        self.pet_cc_cap = 'พลาสติกใส '+ str(pet_cc) +' %'
        self.plastic_cc_cap = 'พลาสติกทั่วไป ' + str(plastic_cc) +' %'
        self.trash_cc_cap = 'ขยะทั่วไป '+ str(trash_cc) +' %'

        # update Tank capacity
        update_bin(can_cc, pet_cc, plastic_cc, trash_cc)

    def on_enter(self, *args):
        global current_screen
        current_screen = "HomeScreen"

        # reset scroe
        reset_db()

        # play video
        Clock.schedule_once(self.play_video, 8)


    def play_video(self, dt):
        if current_screen == "HomeScreen":
            sm.transition.direction = "left"
            sm.current = "video_screen"

    def btn_start(self):
        SoundLoader.load('Audacity/1-เริ่มใช้งาน.wav').play()
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
            ReadyScreen2(name="ReadyScreen2"), ProcessScreen2(name="ProcessScreen2"),
            PointScreen(name="PointScreen"), thank_screen(name="thank_screen"),
            video_screen(name="video_screen")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "HomeScreen"
# sm.current = "video_screen"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()