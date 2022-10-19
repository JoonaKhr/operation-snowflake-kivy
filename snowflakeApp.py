from random import uniform
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from mongoConnect import Highscores

#Set the inital window size and the minimum size for computer versions of the game
Window.size = (500, 600)
Window.minimum_width = 500
Window.minimum_height = 600
#Set a nice gray background so it doesn't burn the eyes
Window.clearcolor = (0.3, 0.3, 0.3, 1)





class SettingsScreen(Screen):
    def __init__(self, **kw):
        self.init_resources()
        super().__init__(**kw)
    
    #Init soundfile
    def init_resources(self):
        self.sound_point = SoundLoader.load("resources/Player/footstep.wav")
        self.sound_button = SoundLoader.load("resources/UI/cancel-1.wav")


    def button_click_sound(self):
        self.sound_button.play()


class LeaderboardsScreen(Screen):
    def __init__(self, **kw):
        self.init_resources()
        super().__init__(**kw)

    #Init soundfile
    def init_resources(self):
        self.sound_point = SoundLoader.load("resources/Player/footstep.wav")
        self.sound_button = SoundLoader.load("resources/UI/cancel-1.wav")

    def button_click_sound(self):
        self.sound_button.play()

class OperationSnowflake(Screen):
    score = 0
    scoreText = StringProperty(f"Score: {score}")
    objectsOnScreen = []

    def __init__(self, **kwargs):
        super(OperationSnowflake, self).__init__(**kwargs)
        self.highscores = Highscores()
        self.init_resources()

    #Init soundfile
    def init_resources(self):
        self.sound_point = SoundLoader.load("resources/Player/footstep.wav")
        self.sound_button = SoundLoader.load("resources/UI/cancel-1.wav")

    def button_click_sound(self):
        self.sound_button.play()

<<<<<<< HEAD
    def on_touch_move(self, touch):
        #self.changeVolume()
        return super().on_touch_move(touch)

=======
>>>>>>> ed2e4bfca23d14104182e2fe777881d2df27c6e7
    #Store touch pos in our relative layouts local coordinates and check if it collides with one of the game objects
    def on_touch_down(self, touch):
        touchcoords = self.ids.playArea.to_local(touch.x, touch.y)
        for item in self.objectsOnScreen:
            if item.collide_point(touchcoords[0], touchcoords[1]):
                self.addPoint(item)
        return super().on_touch_down(touch)

    #Actually works, it gives points and removes clicked object from screen
    def addPoint(self, obj):
        self.ids.playArea.remove_widget(obj)
        self.sound_point.play()
        self.score += 1
        self.scoreText = f"Score: {self.score}"
        self.spawnInRandPos()
    
    #Spawn a game object in a random position and check if the game object list equals five in that case delete the earliest one
    def spawnInRandPos(self):
        playObject = Image(source="resources/imgs/a3.png", color=(1,1,1,1))
        playObject.size = playObject.texture_size
        playObject.size_hint = (None, None)
        playObject.pos_hint={"center_x":uniform(.05, .90),"center_y":uniform(.05, .90)}

        self.ids.playArea.add_widget(playObject, 0, self.ids.playArea.canvas.after)
        if len(self.objectsOnScreen) == 5:
            self.ids.playArea.remove_widget(self.objectsOnScreen[0])
            self.objectsOnScreen.pop(0)
            self.objectsOnScreen.append(playObject)
        else:
            self.objectsOnScreen.append(playObject)
    
    #Init the timer event to use for the StartGameToggle 
    def startClock(self):
        self.timerEvent = Clock.schedule_interval(self.timerTick, 1)

    #Reset the game state on the original values
    def resetGameState(self):
        self.ids.startToggle.state = "normal"
        self.ids.startToggle.text = "Start"
        self.ids.ldrbrds_btn.disabled = False
        self.ids.settings_btn.disabled = False
        self.ids.timer.value = 0
        self.score = 0
        self.ids.playArea.clear_widgets()
        self.objectsOnScreen.clear()
        self.timerEvent.cancel()
        self.scoreText = f"Score: {self.score}"

    # Start the game and the clock, also disable the two extra buttons so no accidents happen
    def startGameToggle(self, widget):
        if widget.state == "normal":
            widget.text = "Start"
            self.resetGameState()
        else:
            widget.text = "Stop"
            self.ids.timer.value = 100
            self.ids.ldrbrds_btn.disabled = True
            self.ids.settings_btn.disabled = True
            self.startClock()

    #Tick tock the time goes also spawns one flake on every tick
    def timerTick(self, dt):
        self.ids.timer.value -= 1
        self.spawnInRandPos()
        if self.ids.timer.value == 0:
            self.highscores.insertHighscore("joona", self.score)
            self.resetGameState()
            
class SnowflakeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(OperationSnowflake(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(LeaderboardsScreen(name='leaderboards'))
        return sm

if __name__ == "__main__":
    SnowflakeApp().run()

# kivy course- create python games and mobile apps
# youtube
# You can use kivy's Animation class which is described very nicely by @inclement on youtube.