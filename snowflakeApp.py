from random import uniform
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config

#Set the inital window size and the minimum size for computer versions of the game
Window.size = (500, 600)
Window.minimum_width = 500
Window.minimum_height = 600
#Set a nice gray background so it doesn't burn the eyes
Window.clearcolor = (0.3, 0.3, 0.3, 1)

class SettingsScreen(Screen):
    pass


class LeaderboardsScreen(Screen):
    pass

class OperationSnowflake(Screen):
    score = 0
    scoreText = StringProperty(f"Score: {score}")
    objectsOnScreen = []

    def on_touch_down(self, touch):
        print(touch.pos)
        touchcoords = self.ids.playArea.to_local(touch.x, touch.y)
        print(touchcoords)
        for item in self.objectsOnScreen:
            if item.collide_point(touchcoords[0], touchcoords[1]):
                self.addPoint(item)
        return super().on_touch_down(touch)

    #Actually works, it gives points and removes clicked object from screen
    def addPoint(self, obj):
        self.ids.playArea.remove_widget(obj)
        self.score += 1
        self.scoreText = f"Score: {self.score}"
    
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
        self.ids.playArea.clear_widgets()
        self.objectsOnScreen.clear()
        self.timerEvent.cancel()

    # Start the game and the clock also disable the two extra buttons so no accidents happen
    def startGameToggle(self, widget):
        if widget.state == "normal":
            widget.text = "Start"
            self.resetGameState()
        else:
            widget.text = "Stop"
            self.ids.timer.value = 100
            self.score = 0
            self.ids.ldrbrds_btn.disabled = True
            self.ids.settings_btn.disabled = True
            self.startClock()

    #Tick tock the time goes also spawns one flake on every tick
    def timerTick(self, dt):
        self.ids.timer.value -= 1
        self.spawnInRandPos()
        if self.ids.timer.value == 0:
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