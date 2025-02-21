from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from kivy.properties import ObjectProperty

WORK_MIN = 25
timer = None

# A custom button that acts like an image button
class PlayButton(ButtonBehavior, Image):
    pass

# A custom button that acts like an image button
class RefreshButton(ButtonBehavior, Image):
    pass

# A custom button that acts like an image button
class NextButton(ButtonBehavior, Image):
    pass

# Define a custom widget that will be used in your KV file.
class PomodoroScreen(MDBoxLayout):
    play_button = ObjectProperty(None)

    def on_play_button_pressed(self):
        print("Play button pressed!")

    def on_refresh_button_pressed(self):
        print("refresh button pressed!")

    def on_next_button_pressed(self):
        print("next button pressed!")

class Pomodoro(MDApp):
    def build(self):
        # When you use a KV file with the same name as your app (pomodoro.kv),
        # it loads automatically. You just need to return the root widget.
        return PomodoroScreen()

if __name__ =="__main__":
    Pomodoro().run()