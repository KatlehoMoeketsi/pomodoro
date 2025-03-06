from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.core.window import Window
from plyer import notification

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

    timer_text = StringProperty("00:05")
    break_text = StringProperty("00:05")
    cycle_label = StringProperty("Press play to begin!!")
    session = StringProperty("Work")
    is_running = BooleanProperty(False)
    is_work_session = True
    session_count = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total_time = 5 #25 minute work period
        self.short_break_time = 5 # 5 minute breaks
        self.long_break_time = 15 * 60 #long break after 4 cycles
        self.remaining_time = self.total_time
        self.timer_event = None

        #Load sound files
        self.work_sound = SoundLoader.load("assets/work_start.mp3")
        self.break_sound = SoundLoader.load("assets/break_start.mp3")

    def on_play_pause_button_pressed(self):
        print("Play button pressed!")
        if not self.is_running:
            print("Starting Timer")
            self.is_running = True
            self.start_timer()

        else:
            print("Pausing Timer")
            self.is_running = False
            self.pause_timer()


    def play_sound(self, sound):
        if sound:
            sound.play()

    def start_timer(self):
        if self.timer_event:
           self.timer_event.cancel()
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def pause_timer(self):
        if self.timer_event:
            self.timer_event.cancel()
            self.cycle_label = "Paused"


    def update_timer(self, dt):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            self.timer_text = f"{minutes:02d}:{seconds:02d}"
        else:
            print("Timer complete")
            self.timer_text = "Time's up!"
            self.is_running = False
            Clock.unschedule(self.update_timer)
            self.switch_session()

    def on_refresh_button_pressed(self):
        print("refresh button pressed!")
        if self.timer_event:
            self.timer_event.cancel()
        self.is_running = False
        self.remaining_time = self.total_time
        self.timer_text = "25:00"
        self.is_work_session = True
        self.session_count = 0  # Reset cycle count


    def switch_session(self):
        """Switches between work and breaks"""
        if self.is_work_session:
            self.session_count+=1 #increment completed pomodoro cycles
            if self.session_count % 4 == 0:
                self.remaining_time = self.long_break_time # Long break after 4 cycles
                self.session = "Long Break"
                message = "Time for a long break!"
                print("Long Break Cycle")
            else:
                self.remaining_time = self.short_break_time # Regular break time
                self.session = "Short Break"
                message = "Time for a short break!"
                print("Short Break started")
            self.play_sound(self.break_sound)
        else:
            self.remaining_time = self.total_time
            print("Back to work")
            message = "Back to work!"
            self.session = "Work"
            self.play_sound(self.work_sound)

        #Show notifications using plyer
        notification.notify(
            title= "Pomodoro Timer",
            message = message,
            app_name = "Pomodoro App",
            timeout= 5
        )

        self.is_work_session = not self.is_work_session
        self.timer_text = f"{self.remaining_time // 60:02d}:00"
        self.on_play_pause_button_pressed()


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