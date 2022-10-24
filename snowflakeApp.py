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
        self.highscores = Highscores()
        self.name = ""
        super().__init__(**kw)
    
    #Init soundfile
    def init_resources(self):
        self.sound_point = SoundLoader.load("resources/Player/footstep.wav")
        self.sound_button = SoundLoader.load("resources/UI/cancel-1.wav")

    def validate_name(self, value):
        self.name = value
        if self.name in self.highscores.get_names():
            self.ids.name_in_use.text = "Name already in use,\n you might interfere \n with someone elses leaderboards"
        print(self.name)

    def get_name(self):
        return self.name

    def button_click_sound(self):
        self.sound_button.play()


class LeaderboardsScreen(Screen):
    first_place = StringProperty("")
    second_place = StringProperty("")
    third_place = StringProperty("")
    fourth_place = StringProperty("")
    fifth_place = StringProperty("")
    def __init__(self, **kw):
        self.highscores = Highscores()
        
        self.init_resources()
        self.default_sorted_leaderboards()
        super().__init__(**kw)

    def default_sorted_leaderboards(self):
        tempList = list(self.highscores.getFiveHighestScores().items())
        self.first_place = f"{tempList[0][0].capitalize()}: {tempList[0][1]}"
        self.second_place = f"{tempList[1][0].capitalize()}: {tempList[1][1]}"
        self.third_place = f"{tempList[2][0].capitalize()}: {tempList[2][1]}"
        self.fourth_place = f"{tempList[3][0].capitalize()}: {tempList[3][1]}"
        self.fifth_place = f"{tempList[4][0].capitalize()}: {tempList[4][1]}"

    def name_sorted_leaderboards(self):
        name = self.ids.name_input.text
        if self.highscores.col.find_one({"name": name}):
            tempList = list(self.highscores.getUserHighestScores(name).items())
            for key, value in tempList:
                if len(value) >= 5:
                    #listaan ja vertaa indeksejä tai jotain ?
                    self.first_place = f"{name.capitalize()}: {value[0]}"
                    self.second_place = f"{name.capitalize()}: {value[1]}"
                    self.third_place = f"{name.capitalize()}: {value[2]}"
                    self.fourth_place = f"{name.capitalize()}: {value[3]}"
                    self.fifth_place = f"{name.capitalize()}: {value[4]}"
            

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
        self.highscores.getFiveHighestScores()
        #print(self.)

    #Init soundfile
    def init_resources(self):
        self.sound_point = SoundLoader.load("resources/Player/footstep.wav")
        self.sound_button = SoundLoader.load("resources/UI/cancel-1.wav")

    def button_click_sound(self):
        self.sound_button.play()

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
        playObject = Image(source="resources/imgs/A1.png", color=(1,1,1,1))
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