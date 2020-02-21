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
import random

#first screen and transition
class OpeningScreen(Screen):
    def change_screen(self):
        kv.switch_to(screens[1], direction = 'down')

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
            kv.switch_to(screens[2], direction = 'left')
            #screens[2].animate()
        else:
            popup = Popup(title='Player Selection Error',
                content = Label(text='Please select your player type'),
                size_hint = (0.4, 0.4))    
            popup.open()
    

class RecordingWindow(Screen):
    '''this function responds to the finish game button, will hook to back end to
    stop collecting data'''
        
    #recording.add_widget(Image(source='ballimage.png'))
    def goback(self):
        kv.switch_to(screens[1], direction = 'right')
    
    def startrecording(self):
        if self.ids.recordbutton.text == "Start Recording Positions":
            self.ids.recordbutton.text = "Stop Recording Position Data"
            self.ids.recordinglabel.text = "Recording Data Now!"
            screens[2].animate()
        else:
            self.ids.recordbutton.text = "Finished Game!"
            self.ids.recordinglabel.text = "Finished Game! Waiting for other's data to send!"
            self.ids.recordbutton.disabled = True
        
    def stoprecording(self):
        animate(ballobj)
        print("Stop recording button is working")
    
    def animate(self):
        #ball animation
        ballx = 0.475
        bally = 0.5
        bounce_time = 0.5
        hcorr = 0.3
        tcorr = 0.6
        height = 0.2
        bounces = 10
        self.ids.ball.pos_hint = {"x":ballx, "top":bally}
        
        animation = Animation(pos_hint ={"top":bally + height}, duration = bounce_time)
        for i in range(bounces):
            bounce_time *= tcorr
            height *= hcorr
            animation += Animation(pos_hint ={"top":bally}, duration = bounce_time)  
            animation += Animation(pos_hint ={"top":bally + height}, duration = bounce_time) 
            
        animation.repeat = True
        animation.start(self.ids.ball) 
        
#host chooses player amount
class HostPlayersChoiceWindow(Screen):
    def choosenum(self, totplayers):
        print(totplayers)
        kv.switch_to(screens[2], direction = 'left')
        #screens[2].animate()
        

class WindowManager(ScreenManager):
    pass

#this loads the kivy code file with the GUI customizations
loading = Builder.load_file("my.kv")
screens = [OpeningScreen(name="opening"), MainWindow(name="main"),
           RecordingWindow(name="recording"),
           HostPlayersChoiceWindow(name="playeramountchoice")]
    
kv = ScreenManager(transition=SwapTransition())

#sets first screen to open
kv.switch_to(screens[0])

#complies app
class MyMainApp(App):
    def build(self):
        return kv
        


if __name__ == "__main__":
    MyMainApp().run()