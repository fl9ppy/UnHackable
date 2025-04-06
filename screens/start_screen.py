from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.metrics import dp

KV = '''
<StartScreen>:
    name: "start"

    FloatLayout:
        Image:
            source: "assets/bg_initial.jpg"
            allow_stretch: True
            keep_ratio: False
            size_hint: 1, 1
            pos_hint: {"center_x": 0.5, "center_y": 0.5}

        MDLabel:
            text: "UnHackable"
            font_style: "H3"
            halign: "center"
            font_name: "Noyh-Regular"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            pos_hint: {"center_x": 0.5, "center_y": 0.72}
            size_hint_y: None
            height: self.texture_size[1]

        MDLabel:
            text: "Spice Up Your Skills. Stay UnHackable"
            font_style: "Subtitle1"
            halign: "center"
            theme_text_color: "Custom"
            font_name: "Noyh-Regular"
            text_color: 1, 1, 1, 1
            pos_hint: {"center_x": 0.5, "center_y": 0.66}
            size_hint_y: None
            height: self.texture_size[1]

        MDRaisedButton:
            text: "Let’s start!"
            md_bg_color: 0.85, 0.15, 0.15, 1
            text_color: 1, 1, 1, 1
            pos_hint: {"center_x": 0.5, "center_y": 0.45}
            size_hint: None, None
            font_name: "Noyh-Regular"
            size: dp(260), dp(56)
            on_release: app.root.current = "login"
            elevation: 10
            # 🛠️ Fixed: Explicitly define all 4 radius values to avoid crash
            border_radius: [24, 24, 24, 24]

        MDLabel:
            text: "by SpicyVoltage"
            font_style: "Caption"
            font_name: "Noyh-Regular"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            pos_hint: {"center_x": 0.5, "y": 0.02}
'''

Builder.load_string(KV)

class StartScreen(Screen):
    pass
