from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty
from kivy.core.window import Window

# A custom button that acts like an image button
class PlayPauseButton(ButtonBehavior, Image):
    pass

# A custom button that acts like an image button
class RefreshButton(ButtonBehavior, Image):
    pass

# A custom button that acts like an image button
class NextButton(ButtonBehavior, Image):
    pass

# Define a custom widget that will be used in your KV file.
class PomodoroScreen(MDBoxLayout):

    timer_text = StringProperty("25:00")
    break_text = StringProperty("5:00")
    cycle_label = StringProperty("Press play to begin!!")
    is_running = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total_time = 25 * 60
        self.remaining_time = self.total_time
        self.timer_event = None

    def on_play_pause_button_pressed(self):
        print("Play button pressed!")
        if not self.is_running:
            print("Starting Timer")
            self.cycle_label = "Working"
            self.is_running = True
            self.start_timer()

        else:
            print("Pausing Timer")
            self.is_running = False
            self.pause_timer()


    def start_timer(self):
        if self.timer_event:
           self.timer_event.cancel()
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def pause_timer(self):
        if self.timer_event:
            self.timer_event.cancel()
            self.cycle_label = "Paused"


    def update_timer(self, dt):
        if self.remaining_time >0:
            self.remaining_time -=1
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            self.timer_text = f"{minutes:02d}:{seconds:02d}"
        else:
            print("Timer complete")
            self.timer_text = "Time's up!"
            self.is_running = False
            Clock.unschedule(self.update_timer)

    def on_refresh_button_pressed(self):
        print("refresh button pressed!")
        if self.timer_event:
            self.timer_event.cancel()
        self.is_running = False
        self.remaining_time = self.total_time
        self.timer_text = "25:00"


    def on_next_button_pressed(self):
        print("next button pressed!")

class Pomodoro(MDApp):
    def build(self):
        Window.size = (400, 650)
        # When you use a KV file with the same name as your app (pomodoro.kv),
        # it loads automatically. You just need to return the root widget.
        return PomodoroScreen()

if __name__ =="__main__":
    Pomodoro().run()