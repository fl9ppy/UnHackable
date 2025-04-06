from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from screens.login_screen import LoginScreen  # <- Login screen module
from screens.signup_screen import SignupScreen
from screens.level_screen import LevelScreen
from screens.home_screen import HomeScreen
from screens.master_screen import MasterScreen
from database.db import init_db  # 🔥 Real DB initialization
from screens.chapter_screen import ChapterScreen
from screens.start_screen import StartScreen
from kivy.core.text import LabelBase

Window.size = (360, 640)

class UnHackableApp(MDApp):
    def build(self):
        self.title = "UnHackable 🌶️"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Dark"
        LabelBase.register(name="Noyh-Regular", fn_regular="assets/fonts/Noyh-Regular.ttf")

        init_db()  # 🔧 Create tables if not already created

        sm = ScreenManager()
        sm.add_widget(StartScreen(name="start"))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(LevelScreen(name='level'))
        sm.add_widget(MasterScreen(name="master"))
        sm.add_widget(ChapterScreen(name="chapter"))
        sm.current = "start"
        return sm

if __name__ == "__main__":
    UnHackableApp().run()
