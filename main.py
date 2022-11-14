from random import uniform
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'multisamples', '0')
Config.write()
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.config import Config
from mongoConnect import Highscores


#Set the initial window size and the minimum size for computer versions of the game
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
    def __init__(self, **kw):
        self.highscores = Highscores()
        self.init_resources()
        super().__init__(**kw)

    #Sorts the leaderboard for only the highest five scores in the whole database
    def default_sorted_leaderboards(self):
        tempList = list(self.highscores.getFiveHighestScores().items())
        rows = [i for i in self.ids.leaderboardsPos.children]
        #Removes the labels and creates a new set
        for row in rows:
            if type(row) == Label:
                self.ids.leaderboardsPos.remove_widget(row)
        for n in range(0, 5):
            l = Label(text=f"{tempList[n][0].capitalize()}: {tempList[n][1]}")
            self.ids.leaderboardsPos.add_widget(l, index=1)

    #Sorts the leaderboard for the selected username's five highest scores in the database
    def name_sorted_leaderboards(self):
        #Removes the labels so names with less than five scores only show as many as they have
        rows = [i for i in self.ids.leaderboardsPos.children]
        for row in rows:
            if type(row) == Label:
                self.ids.leaderboardsPos.remove_widget(row)
        #Set the name to lowercase as that's how they're stored in the data
        name = self.ids.name_input.text.lower()
        #If name found in database get the five highest scores
        if self.highscores.col.find_one({"name": name}):
            for index, value in enumerate(self.highscores.getUserHighestScores(name)):
                if index < 5:
                    l = Label(text=f"{name.capitalize()}: {value}")
                    self.ids.leaderboardsPos.add_widget(l, index=1)
            #Creates empty labels to correct the automatic sizing when selected name has less than five scores
            i = 0
            while i < (5 - len(self.highscores.getUserHighestScores(name))):
                self.ids.leaderboardsPos.add_widget(Label(text=""), index=1)
                i+=1

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

    #It gives points, removes clicked object from screen and spawns a new one
    def add_point(self, obj):
        self.ids.playArea.remove_widget(obj)
        self.objectsOnScreen.remove(obj)
        self.sound_point.play()
        self.score += 1
        self.scoreText = f"Score: {self.score}"
        self.spawn_in_rand_pos()

    #Spawn a game object in a random position and check if the game object list equals five in that case delete the earliest one
    def spawn_in_rand_pos(self):
        #Source zip for kivy to load the images as animation
        playObject = Image(source="resources/imgs/SalmonSnake.zip", color=(1,1,1,1), anim_delay=.1)
        playObject.size = playObject.texture_size
        #Remove size hint so the images aren't the size of the layout they're put on
        playObject.size_hint = (None, None)
        #Randomise position on layout
        playObject.pos_hint={"center_x":uniform(.05, .90),"center_y":uniform(.05, .90)}
        #Add image widget on the layout
        self.ids.playArea.add_widget(playObject, 0, self.ids.playArea.canvas.after)
        #Put the objects in a list it's easier to manage them
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
        #Create screen manager for the different screens in the program
        sm = WindowManager()
        sm.add_widget(OperationSnowflake(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(LeaderboardsScreen(name='leaderboards'))
        return sm

if __name__ == "__main__":
    SnowflakeApp().run()
