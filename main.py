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
import os
import threading

# add sound
# from kivy.core.audio import SoundLoader
# sound = SoundLoader.load('file_example_WAV_1MG.wav')
# sound.play()
# sound.stop()

from DateTime import get_date, get_time, \
    get_start_time, calculate_time, create_timeout

# from database import DataBase
from micro_control import micro_control
# from firebase_storage import upload_preds, upload_origin

from _smartbinAPI import login_uname, login_qrCode, get_qrcode_accessTK, \
                            decode_token, update_bin, get_data_type

# Hide mouse cursor on desktop
Window.show_cursor = True

# Full Screen
Window.fullscreen = False
# Window.fullscreen = 'auto'

# Set windows size
Window.size = (800, 480)

# class library
mc = micro_control

# global
unknown, general_plastic, clear_plastic, caned, sump = 0, 0, 0, 0, 0
calculatescore = 0

# count time out
start_time = get_start_time()
timeout = create_timeout()


class PointScreen(Screen):
    total_point = StringProperty(0)
    current = ""

    def on_enter(self, *args):
        global calculatescore
        
        # show point total to screen
        self.total_point = str(calculatescore)

    def btn_home(self):
        # reset value
        global glass, plastic, can, sump, calculatescore
        glass, can, plastic, sump = 0, 0, 0, 0
        calculatescore = 0
        sm.transition.direction = "right"
        sm.current = "HomeScreen"


class ProcessScreen(Screen):
    Date = StringProperty(0)
    Time = StringProperty(0)
    User = StringProperty(None)
    unknown_pie = StringProperty(0)
    general_plastic_pie = StringProperty(0)
    clear_plastic_pie = StringProperty(0)
    caned_pie = StringProperty(0)
    sum_pie = StringProperty(0)
    time_left = StringProperty('14.19')
    current = ""

    def on_enter(self, *args):
        self.User, self.Date, self.Time, self.unknown_pie, \
            self.general_plastic_pie, self.clear_plastic_pie, \
            self.caned_pie, self.sum_pie = self.current

        # reload timeout
        Clock.schedule_interval(self.calculate_timeout, 1)

    def calculate_timeout(self, dt):
        global start_time, timeout
        self.time_left = calculate_time(start_time, timeout)


class ReadyScreen(Screen):
    global unknown, general_plastic, clear_plastic, caned, sump

    User = StringProperty(None)
    Date = StringProperty(get_date())
    Time = StringProperty(get_time())
    unknown_pie = StringProperty(0)
    general_plastic_pie = StringProperty(0)
    clear_plastic_pie = StringProperty(0)
    caned_pie = StringProperty(0)
    sum_pie = StringProperty(0)
    time_left = StringProperty('14.30')
    current = ""

    def __init__(self,**kwargs):
        super(ReadyScreen, self).__init__(**kwargs)
        self.Class, self.Points = get_data_type()

    def on_enter(self, *args):
        self.AccessToken, uname = self.current.split(',')

        if uname == "donate":
            self.User = "User donate"
        else:
            self.User = uname

        # reload datetime
        Clock.schedule_interval(self.update_datetime, 10)

        # reload timeout
        Clock.schedule_interval(self.calculate_timeout, 1)

    def calculate_timeout(self, dt):
        global start_time, timeout
        self.time_left = calculate_time(start_time, timeout)

    def update_datetime(self, dt):
        self.Date = get_date()
        self.Time = get_time()
    
    def micro_working(self):
        global unknown, general_plastic, clear_plastic, caned, sump, calculatescore
    
        mc = micro_control()
        self.image_grey, self.ClassFolder, self.image_origin = mc.prediction(self.AccessToken)
        os.remove(self.image_origin)
        os.remove(self.image_grey)

        # update value screen
        if self.Class[self.ClassFolder] == 'ไม่ทราบประเภท':
            self.unknown_pie = str(unknown + 1)
            calculatescore += self.Points[self.ClassFolder]
        elif self.Class[self.ClassFolder] == 'กระป๋อง':
            self.caned_pie = str(caned + 1)
            calculatescore += self.Points[self.ClassFolder]
        elif self.Class[self.ClassFolder] == 'พลาสติกทั่วไป':
            self.general_plastic_pie = str(general_plastic + 1)
            calculatescore += self.Points[self.ClassFolder]
        else:   # พลาสติกใส
            self.clear_plastic_pie = str(clear_plastic + 1)
            calculatescore += self.Points[self.ClassFolder]
        
        self.sum_pie = str(int(self.unknown_pie) + int(self.general_plastic_pie) + \
            int(self.clear_plastic_pie) + int(self.caned_pie))

        # update value in global
        unknown = int(self.unknown_pie)
        general_plastic = int(self.general_plastic_pie)
        clear_plastic = int(self.clear_plastic_pie)
        caned = int(self.caned_pie)
        sump = int(self.sum_pie)
    
        self.endprocess()

    def collect(self):
        # update date/time on screen
        self.Date = get_date(); self.Time = get_time()
        self.startprocess()
        threading.Thread(target=self.micro_working).start()

    def startprocess(self):
        ProcessScreen.current = self.User, get_date(), get_time(), str(self.unknown_pie), \
                                str(self.general_plastic_pie), str(self.clear_plastic_pie), str(self.caned_pie), str(self.sum_pie)

        sm.transition.direction = "left"
        sm.current = "ProcessScreen"
    
    def endprocess(self):
        sm.transition.direction = "right"
        sm.current = "ReadyScreen"

    def reset(self):
        # reset screen
        self.glass_pie = "0"
        self.plastic_pie = "0"
        self.can_pie = "0"
        self.sum_pie = "0"

    def lookscore(self):
        self.reset()
        sm.transition.direction = "left"
        sm.current = "PointScreen"


class EnterIDScreen(Screen):
    sid = StringProperty()

    def __init__(self,**kwargs):
        super(EnterIDScreen, self).__init__(**kwargs)
        self.std_len = 10

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
        stdOddlen = len(self.sid)
        if stdOddlen != 0:
            self.sid = self.sid[0: stdOddlen-1]

    def ok(self):
        global start_time
        access_token = login_uname( 'b' + self.sid )

        if access_token == -1:
            sm.transition.direction = "left"
            sm.current = "InvalidScreen"
        else:
            ReadyScreen.current = access_token + ',' + self.sid
            sm.transition.direction = "left"
            sm.current = "ReadyScreen"

            start_time = get_start_time()
        
        self.sid = ''

    def btn_back(self):
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
            uname = decode_token(access_token)
            ReadyScreen.current = access_token + ',' + uname
            sm.transition.direction = "left"
            sm.current = "ReadyScreen"

            start_time = get_start_time()

            # cancel time interval
            self.QRcodeScreen_updatePic.cancel()
            self.QRcodeScreen_getQr.cancel()
            self.QRcodeScreen_getAccess.cancel()


    def update_pic(self, dt):
        self.image.reload()

    def get_qrCode(self, dt):
        login_qrCode()

    def btn_back(self):
        sm.transition.direction = "right"
        sm.current = "LoginScreen"


class InvalidScreen(Screen):
    def btn_back(self):
        sm.transition.direction = "right"
        sm.current = "EnterIDScreen"


class LoginScreen(Screen):
    def btn_byQRcode(self):
        # load qr-code api 
        login_qrCode()

        sm.transition.direction = "left"
        sm.current = "QRcodeScreen"

    def btn_byID(self):
        sm.transition.direction = "left"
        sm.current = "EnterIDScreen"

    def btn_back(self):
        sm.transition.direction = "right"
        sm.current = "ExScreen"


class HowToScreen(Screen):
    def btn_back(self):
        sm.transition.direction = "right"
        sm.current = "MenuScreen"


class ExScreen(Screen):
    def btn_collect(self):
        sm.transition.direction = "left"
        sm.current = "LoginScreen"

    def btn_donate(self):
        global start_time

        # ReadyScreen.current = access_token + ',' + self.sid
        access_token = 'donate'
        ReadyScreen.current = access_token + ',' + 'donate'
        sm.transition.direction = "left"
        sm.current = "ReadyScreen"

        start_time = get_start_time()

        
    def btn_back(self):
        sm.transition.direction = "right"
        sm.current = "MenuScreen"


class MenuScreen(Screen):
    gennertal_plastic_point = StringProperty(0)
    clear_plastic_point = StringProperty(0)
    caned_point = StringProperty(0)
    unknown_point = StringProperty(0)

    def __init__(self,**kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        names, points = get_data_type()
        
        self.gennertal_plastic_point = names[3] + '\n' + str(points[1]) + ' คะแนน'
        self.clear_plastic_point = names[2] + '\n  ' + str(points[1]) + ' คะแนน'
        self.caned_point = '  ' + names[1] + '\n' + str(points[2]) + ' คะแนน'
        self.unknown_point = names[0] + '\n  '+str(points[3]) + ' คะแนน'

    def btn_ex(self):
        sm.transition.direction = "left"
        sm.current = "ExScreen"

    def btn_howto(self):
        sm.transition.direction = "left"
        sm.current = "HowToScreen"

    def btn_back(self):
        sm.transition.direction = "right"
        sm.current = "HomeScreen"


class HomeScreen(Screen):
    unknown_type_cc_cap = StringProperty()
    canned_cc_cap = StringProperty()
    clear_plastic_cc_cap = StringProperty()
    general_plastic_cc_cap = StringProperty()

    def __init__(self,**kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        # get from bin
        unknown_type_cc = 10
        canned_cc = 50
        clear_plastic_cc = 30
        general_plastic_cc = 40

        # read capacity form sensor
        self.unknown_type_cc_cap = 'ไม่ทราบประเภท '+ str(unknown_type_cc) +' %'
        self.canned_cc_cap = 'กระป๋อง '+ str(canned_cc) +' %'
        self.clear_plastic_cc_cap = 'พลาสติกทั่วไป '+ str(clear_plastic_cc) +' %'
        self.general_plastic_cc_cap = 'พลาสติกใส '+ str(general_plastic_cc) +' %'

        # update Tank capacity
        update_bin(unknown_type_cc, canned_cc, clear_plastic_cc, general_plastic_cc)

    def btn_start(self):
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
            ReadyScreen(name="ReadyScreen"), ProcessScreen(name="ProcessScreen"), 
            PointScreen(name="PointScreen")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "HomeScreen"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()