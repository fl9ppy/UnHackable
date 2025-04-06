from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.animation import Animation
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.toast import toast
from kivy.metrics import dp
from database.db import get_user_id, login_user

KV = '''
<LoginScreen>:
    name: "login"

    FloatLayout:
        Image:
            source: "assets/bg_login1.jpg"
            allow_stretch: True
            keep_ratio: False
            size_hint: 1, 1
            pos_hint: {"center_x": 0.5, "center_y": 0.5}

        MDBoxLayout:
            orientation: "vertical"
            padding: dp(32)
            spacing: dp(20)
            size_hint: 0.85, None
            height: self.minimum_height
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            md_bg_color: 0, 0, 0, 0

            MDLabel:
                id: title_label
                text: "Login 🌶"
                font_style: "H4"
                halign: "center"
                font_name: "assets/fonts/Noyh-Regular.ttf"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                size_hint_y: None
                height: self.texture_size[1]
                opacity: 0

            MDTextField:
                id: username
                hint_text: "Username"
                icon_right: "account"
                mode: "fill"
                font_name: "assets/fonts/Noyh-Regular.ttf"
                fill_color: 0.1, 0.1, 0.1, 1
                text_color: 1, 0, 0, 1  # 🔥 red text
                icon_right_color: 1, 0, 0, 1  # 🔥 red icon
                radius: [12, 12, 12, 12]
                padding: [dp(12), dp(14), dp(12), dp(14)]
                multiline: False
                max_text_length: 30
                helper_text_mode: "on_focus"
                helper_text: ""
                size_hint_y: None
                height: dp(56)

            MDTextField:
                id: password
                hint_text: "Password"
                icon_right: "lock"
                password: True
                mode: "fill"
                font_name: "assets/fonts/Noyh-Regular.ttf"
                fill_color: 0.1, 0.1, 0.1, 1
                text_color: 1, 0, 0, 1  # 🔥 red text
                icon_right_color: 1, 0, 0, 1  # 🔥 red icon
                radius: [12, 12, 12, 12]
                padding: [dp(12), dp(14), dp(12), dp(14)]
                multiline: False
                max_text_length: 30
                helper_text_mode: "on_focus"
                helper_text: ""
                size_hint_y: None
                height: dp(56)

            MDRaisedButton:
                id: login_button
                text: "Continue"
                font_name: "assets/fonts/Noyh-Regular.ttf"
                md_bg_color: 1, 0.2, 0.2, 1
                text_color: 1, 1, 1, 1
                size_hint: None, None
                size: dp(180), dp(44)
                pos_hint: {"center_x": 0.5}
                on_release: root.do_login()

            MDRaisedButton:
                id: signup_button
                text: "Sign Up"
                md_bg_color: 1, 0.2, 0.2, 1
                text_color: 1, 1, 1, 1
                font_name: "assets/fonts/Noyh-Regular.ttf"
                size_hint: None, None
                size: dp(180), dp(44)
                pos_hint: {"center_x": 0.5}
                on_release: root.go_to_signup()
'''

Builder.load_string(KV)

class LoginScreen(Screen):
    dialog = None

    def on_enter(self):
        Animation(opacity=1, d=0.6, t='out_quad').start(self.ids.title_label)
        self.ids.login_button.radius = [22, 22, 22, 22]
        self.ids.signup_button.radius = [22, 22, 22, 22]

    def do_login(self):
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()

        if not username or not password:
            self.show_error_dialog("Please enter both username and password.")
            return

        if login_user(username, password):
            user_id = get_user_id(username)
            if user_id == -1:
                self.show_error_dialog("Login failed. User not found.")
                return

            home = self.manager.get_screen("home")
            home.set_user(username, user_id)
            toast("✅ Login successful!")
            self.manager.current = "home"
        else:
            self.show_error_dialog("Invalid username or password.")

    def show_error_dialog(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Login Failed",
                text=message,
                buttons=[
                    MDRaisedButton(
                        text="Retry",
                        on_release=lambda x: self.dialog.dismiss()
                    )
                ]
            )
        else:
            self.dialog.text = message
        self.dialog.open()

    def go_to_signup(self):
        self.manager.current = "signup"
