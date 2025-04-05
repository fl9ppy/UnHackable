from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from screens.login_screen import LoginScreen  # <- We split LoginScreen into its own file

Window.size = (360, 640)

class UnHackableApp(MDApp):
    def build(self):
        self.title = "UnHackable 🌶️"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Dark"

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        return sm

if __name__ == "__main__":
    UnHackableApp().run()
