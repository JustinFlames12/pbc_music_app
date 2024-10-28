# Import kivy libraries
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from kivy.uix.actionbar import ActionBar
from kivy.core.audio import SoundLoader
from kivy.utils import platform

# Import python libraries
import os

# Run android logic for requesting permissions (only applicable when running app on android)
try: 
    from android.permissions import request_permissions, Permission
    from android.storage import primary_external_storage_path
    request_permissions([
        # Permission.READ_MEDIA_AUDIO,
        # Permission.INTERNET,
        Permission.WRITE_EXTERNAL_STORAGE, 
        Permission.READ_EXTERNAL_STORAGE
    ])
except Exception as e:
    print(f'INFO: Skipping android library since app is not running on android\n{e}')

class MusicApp(App):
    def build(self):
        # set background color
        Window.clearcolor = (0.71, 0.79, 0.79, 0.5)

        # color for buttons
        button_clr = (0.08, 0.54, 0.58, 0.5)

        # create variables
        self.current_song = ""
        self.current_song_prompt = Label(text = f"Current song:\n{self.current_song}", color = (0.2, 0.2, 0.2, 1))
        self.main_layout = BoxLayout(orientation="vertical")
        self.first_layout = GridLayout(cols = 2, size_hint_y = 0.3)
        self.second_layout = BoxLayout(size_hint_y = 0.7)
        self.play_control_layout = GridLayout(cols = 2, size_hint_y = 0.4)
        self.play_button = Button(text = 'Play', background_color = button_clr, on_release = self.on_off_cycle)
        self.play_button.disabled = True

        if platform == 'ios':
            if platform == "ios":
                app = App.get_running_app()
                self.ios_user_data_dir = app.user_data_dir
                self.ios_dir = app.directory
                print(f'iOS User Data Directory: {self.ios_user_data_dir}')
                print(f"iOS App Directory : {self.ios_dir}")

        # create a dropdown with 10 buttons
        self.dropdown = DropDown()
        # for index in range(10):
        if platform == 'win':
            for song in os.listdir('.\soundtrack'):
                # When adding widgets, we need to specify the height manually
                # (disabling the size_hint_y) so the dropdown can calculate
                # the area it needs.
                self.song_btn = Button(text=song[:-4], size_hint_y=None, height=30)
                # for each button, attach a callback that will call the select() method
                # on the dropdown. We'll pass the text of the button as the data of the
                # selection.
                self.song_btn.bind(on_release=lambda btn: self.change_song(btn, btn.text))
                # then add the button inside the dropdown
                self.dropdown.add_widget(self.song_btn)
        elif platform == 'ios':
            for song in os.listdir(self.ios_dir + '/soundtrack'):
                # When adding widgets, we need to specify the height manually
                # (disabling the size_hint_y) so the dropdown can calculate
                # the area it needs.
                self.song_btn = Button(text=song[:-4], size_hint_y=None, height=100)
                # for each button, attach a callback that will call the select() method
                # on the dropdown. We'll pass the text of the button as the data of the
                # selection.
                self.song_btn.bind(on_release=lambda btn: self.change_song(btn, btn.text))
                # then add the button inside the dropdown
                self.dropdown.add_widget(self.song_btn)
        else:
            for song in os.listdir('soundtrack'):
                # When adding widgets, we need to specify the height manually
                # (disabling the size_hint_y) so the dropdown can calculate
                # the area it needs.
                self.song_btn = Button(text=song[:-4], size_hint_y=None, height=30)
                # for each button, attach a callback that will call the select() method
                # on the dropdown. We'll pass the text of the button as the data of the
                # selection.
                self.song_btn.bind(on_release=lambda btn: self.change_song(btn, btn.text))
                # then add the button inside the dropdown
                self.dropdown.add_widget(self.song_btn)

        # create a big main button
        if platform == 'ios':
            self.mainbutton = Button(text='All songs', size_hint=(1, None), 
                            background_color = button_clr, height = 200)
        else:
            self.mainbutton = Button(text='All songs', size_hint=(1, None), background_color = button_clr)

        # show the dropdown menu when the main button is released
        # note: all the bind() calls pass the instance of the caller (here, the
        # mainbutton instance) as the first argument of the callback (here,
        # dropdown.open.).
        self.mainbutton.bind(on_release=self.dropdown.open)

        # one last thing, listen for the selection in the dropdown list and
        # assign the data to the button text.
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))
        self.stop_button = Button(text='Stop', background_color = button_clr, on_release = self.on_off_cycle)
        self.stop_button.disabled = True

        self.play_control_layout.add_widget(self.play_button)
        self.play_control_layout.add_widget(self.stop_button)
        self.first_layout.add_widget(self.current_song_prompt)
        self.first_layout.add_widget(self.play_control_layout)
        # self.first_layout.add_widget(self.play_button)
        self.second_layout.add_widget(self.mainbutton)

        self.main_layout.add_widget(self.first_layout)
        self.main_layout.add_widget(self.second_layout)
        # self.first_layout.add_widget(self.stop_button)
        # return self.first_layout
        return self.main_layout
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_off_cycle(self, instance):
        if self.play_button.disabled == True:
            self.sound.stop()
            self.stop_button.disabled = True
            self.play_button.disabled = False
        else:
            self.sound.play()
            self.play_button.disabled = True
            self.stop_button.disabled = False

    def change_song(self, instance, text):
        try:
            self.sound.stop()
        except Exception as e:
            print(f'There was no playing song to stop. Error Message: {e}')
        self.current_song_prompt.text = f"Current song:\n{text}"
        self.dropdown.select(text)
        # if (self.play_button.disabled == True and self.stop_button.disabled == False):
        #     self.on_off_cycle(self.stop_button)
        #     # self.sound.stop()
        # elif (self.play_button.disabled == True and self.stop_button.disabled == True):
        #     self.stop_button.disabled = False
        # elif (self.play_button.disabled == False and self.stop_button.disabled == True):
        #     self.stop_button.disabled = False
        #     self.play_button.disabled = True
        self.stop_button.disabled = False
        self.play_button.disabled = True
        if platform == 'win':
            self.sound = SoundLoader.load(f".\soundtrack\{text}.wav")
            self.sound.play()
        elif platform == 'ios':
            self.sound = SoundLoader.load(f"{self.ios_dir}/soundtrack/{text}.wav")
            self.sound.play()
        else:
            self.sound = SoundLoader.load(f"soundtrack/{text}.wav")
            self.sound.play()

if __name__ == '__main__':
    MusicApp().run()