from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.animation import Animation
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.toast import toast

# === MOCK LOGIN FUNCTION DIRECTLY HERE ===
def login_user(username, password) -> bool:
    print(f"[MOCK] login_user({username}, {password})")
    return username == "test" and password == "1234"

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
        username = self.ids.username.text
        password = self.ids.password.text

        if login_user(username, password):
            toast("✅ Login successful!")
        else:
            self.show_error_dialog()

    def show_error_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Login Failed",
                text="Invalid username or password.",
                buttons=[
                    MDRaisedButton(text="Retry", on_release=lambda x: self.dialog.dismiss())
                ]
            )
        self.dialog.open()
