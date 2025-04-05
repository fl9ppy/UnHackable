from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager


from screens.login_screen import LoginScreen  # <- Login screen module
from screens.signup_screen import SignupScreen
from database.db import init_db  # 🔥 Real DB initialization

Window.size = (360, 640)

class UnHackableApp(MDApp):
    def build(self):
        self.title = "UnHackable 🌶️"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Dark"

        init_db()  # 🔧 Create tables if not already created

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(SignupScreen(name='signup'))
        return sm

if __name__ == "__main__":
    UnHackableApp().run()

