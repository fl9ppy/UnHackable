from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.animation import Animation
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.toast import toast

# Import the real backend function from mock_db or db.py
from database.mock_db import create_user  # You can later switch to: from database.db import create_user

KV = '''
<SignupScreen>:
    name: "signup"

    MDBoxLayout:
        orientation: "vertical"
        padding: dp(32)
        spacing: dp(24)
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint: 0.85, 0.75

        MDLabel:
            id: title_label
            text: "🧑‍💻 Create Your Account"
            font_style: "H4"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            opacity: 0

        MDTextField:
            id: username
            hint_text: "Username"
            icon_right: "account"
            mode: "rectangle"
            size_hint_y: None
            height: dp(56)

        MDTextField:
            id: password
            hint_text: "Password"
            icon_right: "lock"
            password: True
            mode: "rectangle"
            size_hint_y: None
            height: dp(56)

        MDTextField:
            id: confirm_password
            hint_text: "Confirm Password"
            icon_right: "lock-check"
            password: True
            mode: "rectangle"
            size_hint_y: None
            height: dp(56)

        MDRaisedButton:
            text: "Sign Up"
            md_bg_color: 0.9, 0.2, 0.3, 1
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
