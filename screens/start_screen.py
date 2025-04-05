from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

KV = '''
<StartScreen>:
    name: "start"

    MDFloatLayout:
        MDRaisedButton:
            text: "🔥 Let's Start"
            font_style: "H5"
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            md_bg_color: 1, 0.2, 0.2, 1
            on_release: app.root.current = "login"
'''

Builder.load_string(KV)

class StartScreen(Screen):
    pass
