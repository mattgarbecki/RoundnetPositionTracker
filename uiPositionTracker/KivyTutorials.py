#importing packages
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

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
        #sm.current = 'second'

class SecondWindow(Screen):
    '''this function responds to the finish game button, will hook to back end to
    stop collecting data'''
    def stoprecording(self):
        print("Stop recording button is working")



class WindowManager(ScreenManager):
    pass

#this loads the kivy code file with the GUI customizations
kv = Builder.load_file("my.kv")
#sm = ScreenManager(transition = SwapTransition())
screens = [OpeningScreen(name="opening"), MainWindow(name="main"),
           SecondWindow(name="second")]
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