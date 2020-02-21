#importing packages
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.animation import Animation 
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label

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
        
    def stoprecording(self):
        print("Stop recording button is working")
    
    def animate(self, instance):
        # create an animation object. This object could be stored 
        # and reused each call or reused across different widgets. 
        # += is a sequential step, while &= is in parallel 
        animation = Animation(pos =(100, 100))#, t ='out_bounce') 
        animation += Animation(pos =(200, 100))#, t ='out_bounce') 
        animation &= Animation(size =(500, 500)) 
        animation += Animation(size =(100, 50)) 
        animation.repeat = True
  
        # apply the animation on the button, passed in the "instance" argument 
        # Notice that default 'click' animation (changing the button 
        # color while the mouse is down) is unchanged. 
        animation.start(self.ids.ball)     
        print("Ran animation function")

    #Clock.schedule_once(animate(self.ids.ball), 20)

#host chooses player amount
class HostPlayersChoiceWindow(Screen):
    def choosenum(self, totplayers):
        print(totplayers)
        kv.switch_to(screens[2], direction = 'left')

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