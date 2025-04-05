from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.animation import Animation
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.toast import toast

# === 🔥 REAL BACKEND IMPORT ===
from database.db import login_user

KV = '''
<LoginScreen>:
    MDBoxLayout:
        orientation: "vertical"
        padding: dp(32)
        spacing: dp(24)
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint: 0.85, 0.75

        MDLabel:
            id: title_label
            text: "🌶️ UnHackable Login"
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

        MDRaisedButton:
            text: "Log In"
            md_bg_color: 1, 0.3, 0.3, 1
            pos_hint: {"center_x": 0.5}
            on_release: root.do_login()
'''

Builder.load_string(KV)

class LoginScreen(Screen):
    dialog = None

    def on_enter(self):
        Animation(opacity=1, d=0.6, t='out_quad').start(self.ids.title_label)

    def do_login(self):
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()

        if not username or not password:
            self.show_error_dialog("Please enter both username and password.")
            return

        if login_user(username, password):
            toast("✅ Login successful!")
            # self.manager.current = "home_screen"  # Optional: Navigate to next screen
        else:
            self.show_error_dialog("Invalid username or password.")

    def show_error_dialog(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Login Failed",
                text=message,
                buttons=[
                    MDRaisedButton(text="Retry", on_release=lambda x: self.dialog.dismiss())
                ]
            )
        else:
            self.dialog.text = message
        self.dialog.open()

