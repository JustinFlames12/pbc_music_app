from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from kivy.uix.actionbar import ActionBar

class MusicApp(App):
    def build(self):
        # set background color
        Window.clearcolor = (0.71, 0.79, 0.79, 0.5)

        # color for buttons
        button_clr = (0.08, 0.54, 0.58, 0.5)

        # create variables
        self.current_song = ""
        self.current_song_prompt = Label(text = f"Current song:\n{self.current_song}", color = (0.2, 0.2, 0.2, 1))
        self.first_layout = GridLayout(cols = 2)
        self.play_button = Button(text = 'Play', background_color = button_clr, on_release = self.on_off_cycle)

        # create a dropdown with 10 buttons
        self.dropdown = DropDown()
        for index in range(10):
            # When adding widgets, we need to specify the height manually
            # (disabling the size_hint_y) so the dropdown can calculate
            # the area it needs.

            self.song_btn = Button(text='Song %d' % index, size_hint_y=None, height=30)
            
            # for each button, attach a callback that will call the select() method
            # on the dropdown. We'll pass the text of the button as the data of the
            # selection.
            self.song_btn.bind(on_release=lambda btn: self.change_song(btn, btn.text))

            # then add the button inside the dropdown
            self.dropdown.add_widget(self.song_btn)

        # create a big main button
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

        self.first_layout.add_widget(self.current_song_prompt)
        self.first_layout.add_widget(self.play_button)
        self.first_layout.add_widget(self.mainbutton)
        self.first_layout.add_widget(self.stop_button)
        return self.first_layout
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_off_cycle(self, instance):
        if self.play_button.disabled == True:
            self.stop_button.disabled = True
            self.play_button.disabled = False
        else:
            self.play_button.disabled = True
            self.stop_button.disabled = False

    def change_song(self, instance, text):
        self.current_song_prompt.text = f"Current song:\n{text}"
        self.dropdown.select(text)
        if self.play_button.disabled == True:
            self.on_off_cycle(self.stop_button)

if __name__ == '__main__':
    MusicApp().run()