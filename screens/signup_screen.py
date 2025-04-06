from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.animation import Animation
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.toast import toast

# Import the real backend function from mock_db or db.py
from database.db import create_user

KV = '''
<SignupScreen>:
    name: "signup"

    FloatLayout:
        Image:
            source: "assets/bg_register1.jpg"  # ✅ Replace with your background
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
                text: "Create your account"
                font_style: "H4"
                font_name: "assets/fonts/Noyh-Regular.ttf"
                halign: "center"
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
                text_color: 1, 0.4, 0.2, 1  # orange
                icon_right_color: 1, 0.4, 0.2, 1
                radius: [20, 20, 20, 20]
                padding: [dp(12), dp(14), dp(12), dp(14)]
                size_hint_y: None
                height: dp(56)
                max_text_length: 30
                multiline: False
                helper_text_mode: "on_focus"
                helper_text: ""

            MDTextField:
                id: password
                hint_text: "Password"
                icon_right: "lock"
                password: True
                mode: "fill"
                font_name: "assets/fonts/Noyh-Regular.ttf"
                fill_color: 0.1, 0.1, 0.1, 1
                text_color: 1, 0.4, 0.2, 1
                icon_right_color: 1, 0.4, 0.2, 1
                radius: [20, 20, 20, 20]
                padding: [dp(12), dp(14), dp(12), dp(14)]
                size_hint_y: None
                height: dp(56)
                max_text_length: 30
                multiline: False
                helper_text_mode: "on_focus"
                helper_text: ""

            MDTextField:
                id: confirm_password
                hint_text: "Confirm Password"
                icon_right: "lock-check"
                password: True
                mode: "fill"
                font_name: "assets/fonts/Noyh-Regular.ttf"
                fill_color: 0.1, 0.1, 0.1, 1
                text_color: 1, 0.4, 0.2, 1
                icon_right_color: 1, 0.4, 0.2, 1
                radius: [20, 20, 20, 20]
                padding: [dp(12), dp(14), dp(12), dp(14)]
                size_hint_y: None
                height: dp(56)
                max_text_length: 30
                multiline: False
                helper_text_mode: "on_focus"
                helper_text: ""

            MDRaisedButton:
                id: signup_btn
                text: "Sign Up"
                md_bg_color: 1, 0.1, 0.1, 1  # 🔥 intense red
                text_color: 1, 1, 1, 1
                size_hint: None, None
                size: dp(200), dp(48)
                pos_hint: {"center_x": 0.5}
                on_release: root.do_signup()
'''

Builder.load_string(KV)

class SignupScreen(Screen):
    dialog = None

    def on_enter(self):
        Animation(opacity=1, d=0.6, t='out_back').start(self.ids.title_label)

    def do_signup(self):
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()
        confirm = self.ids.confirm_password.text.strip()

        if not username or not password or not confirm:
            self.show_error("Please fill in all fields.")
            return

        if password != confirm:
            self.show_error("Passwords do not match.")
            return

        if create_user(username, password):
            toast("🎉 Account created! Welcome, " + username)
            self.manager.current = "login"
        else:
            self.show_error("Username already exists.")

    def show_error(self, message):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            title="Signup Error",
            text=message,
            buttons=[
                MDRaisedButton(text="OK", on_release=lambda x: self.dialog.dismiss())
            ]
        )
        self.dialog.open()
