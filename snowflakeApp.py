from random import uniform
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ObjectProperty
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
        self.username = ""
        super().__init__(**kw)
    
    #Init soundfile
    def init_resources(self):
        self.sound_point = SoundLoader.load("resources/Player/footstep.wav")
        self.sound_button = SoundLoader.load("resources/UI/cancel-1.wav")
    #Checks the database if there is already the given name and displays a warning if it is in
    def validate_name(self, value):
        self.username = value
        if self.username in self.highscores.get_names():
            self.ids.name_in_use.text = "Name already in use,\n you might interfere \n with someone elses leaderboards"
        print(self.username)
    #Gets the username
    def get_username(self):
        return self.username
    #Button sound when you click button
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

    #Sorts the leaderboard for only the highest five scores in the whole database
    def default_sorted_leaderboards(self):
        tempList = list(self.highscores.getFiveHighestScores().items())
        self.first_place = f"{tempList[0][0].capitalize()}: {tempList[0][1]}"
        self.second_place = f"{tempList[1][0].capitalize()}: {tempList[1][1]}"
        self.third_place = f"{tempList[2][0].capitalize()}: {tempList[2][1]}"
        self.fourth_place = f"{tempList[3][0].capitalize()}: {tempList[3][1]}"
        self.fifth_place = f"{tempList[4][0].capitalize()}: {tempList[4][1]}"

    #Sorts the leaderboard for the selected username's five highest scores in the database
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
    #Button sound effect for clicking on button
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
        
    #Init soundfile
    def init_resources(self):
        self.sound_point = SoundLoader.load("resources/Player/footstep.wav")
        self.sound_button = SoundLoader.load("resources/UI/cancel-1.wav")
    
    #Play soundfile when you click a menu button
    def button_click_sound(self):
        self.sound_button.play()

    #Store touch pos in our relative layouts local coordinates and check if it collides with one of the game objects
    def on_touch_down(self, touch):
        touchcoords = self.ids.playArea.to_local(touch.x, touch.y)
        for item in self.objectsOnScreen:
            if item.collide_point(touchcoords[0], touchcoords[1]):
                self.add_point(item)
        return super().on_touch_down(touch)

    #Actually works, it gives points and removes clicked object from screen
    def add_point(self, obj):
        self.ids.playArea.remove_widget(obj)
        self.sound_point.play()
        self.score += 1
        self.scoreText = f"Score: {self.score}"
        self.spawn_in_rand_pos()
    
    #Spawn a game object in a random position and check if the game object list equals five in that case delete the earliest one
    def spawn_in_rand_pos(self):
        playObject = Image(source="resources/imgs/imgs.zip", color=(1,1,1,1), anim_delay=0.1)
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
    
    #Init the timer event to use for the start_game_toggle 
    def start_clock(self):
        self.timerEvent = Clock.schedule_interval(self.timer_tick, 1)

    #Reset the game state on the original values
    def reset_game_state(self):
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
    def start_game_toggle(self, widget):
        if widget.state == "normal":
            widget.text = "Start"
            self.reset_game_state()
        else:
            widget.text = "Stop"
            self.ids.timer.value = 100
            self.ids.ldrbrds_btn.disabled = True
            self.ids.settings_btn.disabled = True
            self.start_clock()

    #Tick tock the time goes and calls a function to spawn a game object on every tick
    def timer_tick(self, dt):
        self.ids.timer.value -= 1
        self.spawn_in_rand_pos()
        if self.ids.timer.value == 0:
            if App.get_running_app().root.get_screen('settings').get_username():
                self.highscores.insertHighscore(App.get_running_app().root.get_screen('settings').get_username(), self.score)
            self.reset_game_state()


class WindowManager(ScreenManager):
    pass

class SnowflakeApp(App):
    def build(self):
        sm = WindowManager()
        sm.add_widget(OperationSnowflake(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(LeaderboardsScreen(name='leaderboards'))
        return sm

if __name__ == "__main__":
    SnowflakeApp().run()