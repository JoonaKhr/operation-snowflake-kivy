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


Window.size = (500, 600)
Window.minimum_width = 500
Window.minimum_height = 600

Window.clearcolor = (0.3, 0.3, 0.3, 1)

class SettingsScreen(Screen):
    pass


class LeaderboardsScreen(Screen):
    pass

class OperationSnowflake(Screen):
    score = 0
    scoreText = StringProperty(f"Score: {score}")
    
    def addPoint(self):
        self.score += 1
        self.scoreText = f"Score: {self.score}"
    
    def spawnInRandPos(self):
        self.ids.playArea.add_widget(Image(source="resources/imgs/a3.png", pos_hint={"center_x":uniform(.05, .90),"center_y":uniform(.05, .90)}, color=(1,1,1,1)), 0, self.ids.playArea.canvas.after)

    def openSettings(self):
        pass
    
    def startClock(self):
        self.timerEvent = Clock.schedule_interval(self.timerTick, 1)

    def stopClock(self):
        self.timerEvent.cancel()

    def startGameToggle(self, widget):
        if widget.state == "normal":
            widget.text = "Start"
            self.ids.timer.value = 0
            self.stopClock()
        else:
            widget.text = "Stop"
            self.ids.timer.value = 100
            self.score = 0
            self.ids.ldrbrds_btn.disabled = True
            self.ids.settings_btn.disabled = True
            self.startClock()

    def timerTick(self, dt):
        self.ids.timer.value -= 1
        self.spawnInRandPos()
        if self.ids.timer.value == 0:
            self.stopClock()
            self.startToggle.state = "normal"
            self.startToggle.text = "Start"


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