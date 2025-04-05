from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.animation import Animation
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivy.clock import Clock

KV = '''
<HomeScreen>:
    name: "home"

    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 0.05, 0.05, 0.05, 1  # dark background

        # Top status bar
        MDBoxLayout:
            size_hint_y: None
            height: dp(64)
            padding: dp(12)
            spacing: dp(16)
            md_bg_color: 0.1, 0.1, 0.1, 1

            MDIconButton:
                icon: "fire"
                theme_text_color: "Custom"
                text_color: 1, 0.2, 0.2, 1

            MDLabel:
                text: "🔥 5-day streak"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1

            MDLabel:
                text: "💎 320 XP"
                halign: "right"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1

            MDLabel:
                text: "❤️ 3"
                halign: "right"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1

        # Scrollable level trail
        ScrollView:
            MDBoxLayout:
                id: trail
                orientation: "vertical"
                spacing: dp(28)
                padding: dp(32)
                size_hint_y: None
                height: self.minimum_height
                md_bg_color: 0.05, 0.05, 0.05, 1

        # Bottom navbar
        MDBoxLayout:
            size_hint_y: None
            height: dp(64)
            padding: dp(8)
            spacing: dp(16)
            md_bg_color: 0.1, 0.1, 0.1, 1

            MDIconButton:
                icon: "home"
                theme_text_color: "Custom"
                text_color: 1, 0.2, 0.2, 1

            MDIconButton:
                icon: "school"
                theme_text_color: "Custom"
                text_color: 0.8, 0.8, 0.8, 1

            MDIconButton:
                icon: "account"
                theme_text_color: "Custom"
                text_color: 0.8, 0.8, 0.8, 1
'''

Builder.load_string(KV)

class HomeScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(lambda dt: self.load_bubbles(), 0.1)

    def load_bubbles(self):
        self.ids.trail.clear_widgets()

        level_titles = [
            ("Intro to Phishing", True),
            ("Password Power", True),
            ("Social Engineering", True),
            ("Crack the Code", False),
            ("Final Boss: Master", False)
        ]

        for i, (title, unlocked) in enumerate(level_titles):
            btn = MDRaisedButton(
                text=title,
                size_hint=(None, None),
                size=(dp(240), dp(0)),
                elevation=12,
                font_size=dp(16),
                pos_hint={"center_x": 0.5},
                md_bg_color=(1, 0.2, 0.2, 1) if unlocked else (0.2, 0.2, 0.2, 1),
                text_color=(1, 1, 1, 1)
            )
            btn.radius = [30, 30, 30, 30]

            # Optional: Lock icon
            if not unlocked:
                btn.text += " 🔒"

            btn.opacity = 0
            self.ids.trail.add_widget(btn)

            anim = Animation(opacity=1, size=(dp(240), dp(60)), d=0.5 + i * 0.05, t="out_back")
            anim.start(btn)
