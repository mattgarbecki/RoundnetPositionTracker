#importing packages
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.animation import Animation 
from kivy.clock import Clock


class OpeningScreen(Screen):
    pass

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
            kv.current = 'playeramountchoice'
        else:
            kv.current = 'recording'                
    

class RecordingWindow(Screen):
    '''this function responds to the finish game button, will hook to back end to
    stop collecting data'''
    
    #recording.add_widget(Image(source='ballimage.png'))
    
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
        kv.current = 'recording'

class WindowManager(ScreenManager):
    pass

#this loads the kivy code file with the GUI customizations
kv = Builder.load_file("my.kv")
#sm = ScreenManager(transition = SwapTransition())
screens = [OpeningScreen(name="opening"), MainWindow(name="main"),
           RecordingWindow(name="recording"),
           HostPlayersChoiceWindow(name="playeramountchoice")]
for screen in screens:
    kv.add_widget(screen)
    


#sets first screen to open
kv.current = "opening"

#complies app
class MyMainApp(App):
    def build(self):
        return kv
        


if __name__ == "__main__":
    MyMainApp().run()