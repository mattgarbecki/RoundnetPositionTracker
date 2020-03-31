__version__ = "1.1.3"
#importing packages
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.animation import Animation 
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
#from kivy.utils import platform
from plyer import accelerometer
import os.path, json

# Global Variables
user_data = json.loads(open(os.path.dirname(__file__) + '../data.json').read())

#first screen and transition
class OpeningScreen(Screen):
    def change_screen(self):
        kv.switch_to(screens[1], direction = 'down')
    def font_size(self, size, h, w, text):
        num = len(text)
        print(size, h, w, num)
        first = size[0] * h - size[0] * num
        second = size[1] * w - size[1] * num
        if first < second:
            return first
        else:
            return second    

#controls back end of the main opening window
class MainWindow(Screen):
    #changes window background
    Window.clearcolor = (0.156, 0.249, 0.127, 1)
    #imports variables from the kviy file from MainWindow screen in GUI
    username = ObjectProperty(None)
    game = ObjectProperty(None)
    email = ObjectProperty(None)

    #player type represents if they are host, 1 is host and 0 is player
    playertype = ObjectProperty(None)
    #controls what the submit button will do
    def submit(self):
        print("Name:", self.username.text, "\nemail:", self.email.text,
              "\nGame:", self.game.text, "\nHost? ", self.playertype)
        self.username.text = ""
        self.email.text = "" 
        self.game.text = ""
        print(self.playertype)
        #allows host to choose number of players from correct screen
        if self.playertype == 1:
            kv.switch_to(screens[3], direction = 'left')
        elif self.playertype == 0:
            kv.switch_to(screens[4], direction = 'left')
            #screens[2].animate()
        else:
            popup = Popup(title='Player Selection Error',
                content = Label(text='Please select your player type'),
                size_hint = (0.4, 0.4))    
            popup.open()
    
    def font_size(self, size, h, w):
        first = size[0] * h
        second = size[1] * w
        if first < second:
            return first
        else:
            return second
    

class RecordingWindow(Screen):
    '''this function responds to the finish game button, will hook to back end to
    stop collecting data'''

    gameData = {0.0:[0, 0, 0]}
    elapsed_time = 0.0
    
    def return_data(self):
        return self.gameData

    def get_data(self):
        self.ids.acceldata.text = accelerometer.acceleration
        
    #recording.add_widget(Image(source='ballimage.png'))
    def goback(self):
        kv.switch_to(screens[1], direction = 'right')

    
    def startrecording(self):
        popup = Popup(content = Label(text='Make sure to center your phone on the net before continuing'),
                size_hint = (0.4, 0.4)) 
        popup.open()
        if self.ids.recordbutton.text == "Start Recording Positions":
            #collecting accelerometer data
            accelerometer.enable()
            Clock.schedule_interval(self.get_acceleration, 1 / 20.)
            
            self.ids.recordbutton.text = "Stop Recording Position Data"
            self.ids.recordinglabel.text = "Recording Data Now!"
            screens[2].animate()
        else:
            accelerometer.disable()
            Clock.unschedule(self.get_acceleration)
            
            self.ids.recordbutton.text = "Finished Game!"
            self.ids.recordinglabel.text = "Finished Game! Waiting for other's data to send!"
            self.ids.recordbutton.disabled = True
            
    def get_acceleration(self, dt):

        acceleration = accelerometer.acceleration[:3]

        gameData_prev = self.gameData[self.elapsed_time]
        gameData_curr = []

        if not acceleration == (None, None, None):

            gameData_curr.append(gameData_prev[0] + (0.0025 * acceleration[0]))
            gameData_curr.append(gameData_prev[1] + (0.0025 * acceleration[1]))
            gameData_curr.append(gameData_prev[2] + (0.0025 * acceleration[2]))

            self.ids.acceldatax.text = "X: " + str(gameData_curr[0])
            self.ids.acceldatay.text = "Y: " + str(gameData_curr[1])
            self.ids.acceldataz.text = "Z: " + str(gameData_curr[2])

            self.ids.xaccellab.text = "X: " + str(acceleration[0])
            self.ids.yaccellab.text = "Y: " + str(acceleration[1])
            self.ids.zaccellab.text = "Z: " + str(acceleration[2])

        self.elapsed_time += 0.20
        self.gameData[self.elapsed_time] = gameData_curr
        
    def stoprecording(self):
        animate(ballobj)
        print("Stop recording button is working")
    
    def animate(self):        
        #ball bounce animation
        height = 0.2
        bally = 0.5
        anim2 = Animation(pos_hint ={"top":bally + height}, duration = 0.5)
        anim2 += Animation(pos_hint ={"top":bally}, t='out_bounce')          
        anim2.repeat = True        
        anim2.start(self.ids.ball) 
    
    def font_size(self, size, h, w, text):
        first = size[0] * h
        second = size[1] * w
        if first < second:
            return first
        else:
            return second  
    
    def long_font(self, size, h, w, text):
        num = len(text)
        print(num)
        num = num ** (1 / 2) * (1 / 2)
        first = size[0] * h / num
        second = size[1] * w / num
        if first < second:
            return first
        else:
            return second          
        
#host chooses player amount
class HostPlayersChoiceWindow(Screen):
    def continue_on(self):
        kv.switch_to(screens[4], direction = 'right')
        
    def update_spinners(self):
        #figure out what sport is being played
        if self.ids.sportdrop.text == 'Roundnet':
            val = 2
        elif self.ids.sportdrop.text == 'Basketball':
            val = 5
        elif self.ids.sportdrop.text == 'Soccer':
            val = 11
        elif self.ids.sportdrop.text == 'Football':
            val = 11
        elif self.ids.sportdrop.text == 'Tennis':
            val = 2
        elif self.ids.sportdrop.text == 'Swimming':
            val = 1
        elif self.ids.sportdrop.text == 'Hockey':
            val = 6
        #update spinners with appropriate amount of players
        arr = [0] * val
        for i in range(val):
            arr[i] = str(i)
        self.ids.offensedrop.values = arr
        self.ids.offensedrop.text = str(val)
        self.ids.defensedrop.values = arr
        self.ids.defensedrop.text = str(val)        
        

    def font_size(self, size, h, w, text):
        first = size[0] * h
        second = size[1] * w
        if first < second:
            return first
        else:
            return second    

class TeamChoiceWindow(Screen):
    def continue_on(self):
        kv.switch_to(screens[2], direction = 'left')
    
    def font_size(self, size, h, w, text):
        first = size[0] * h
        second = size[1] * w
        if first < second:
            return first
        else:
            return second    
        

class WindowManager(ScreenManager):
    pass

#this loads the kivy code file with the GUI customizations
loading = Builder.load_file("my.kv")
screens = [OpeningScreen(name="opening"), 
           MainWindow(name="main"),
           RecordingWindow(name="recording"),
           HostPlayersChoiceWindow(name="playeramountchoice"),
           TeamChoiceWindow(name='teamchoice')]
    
kv = ScreenManager(transition=SwapTransition())

#sets first screen to open
kv.switch_to(screens[0])

#complies app
class MyMainApp(App):
    def build(self):
        return kv
        


if __name__ == "__main__":
    MyMainApp().run()