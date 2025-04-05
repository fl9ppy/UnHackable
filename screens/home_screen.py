from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.button import MDRaisedButton
from data_interface import load_chapters

KV = '''
<HomeScreen>:
    name: "home"

    ScrollView:
        MDBoxLayout:
            id: trail
            orientation: "vertical"
            spacing: dp(24)
            padding: dp(32)
            size_hint_y: None
            height: self.minimum_height
'''

Builder.load_string(KV)

class HomeScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(lambda dt: self.load_bubbles(), 0.1)

    def load_bubbles(self):
        self.ids.trail.clear_widgets()
        chapters = load_chapters().get("chapters", [])

        for i, chapter in enumerate(chapters):
            btn = MDRaisedButton(
                text=chapter["title"],
                size_hint=(None, None),
                size=(dp(240), dp(0)),
                elevation=12,
                font_size=dp(16),
                pos_hint={"center_x": 0.5},
                md_bg_color=(1, 0.2, 0.2, 1),
                text_color=(1, 1, 1, 1)
            )
            btn.radius = [30, 30, 30, 30]
            btn.opacity = 0

            btn.bind(on_release=lambda btn, idx=i: self.go_to_chapter(idx))
            self.ids.trail.add_widget(btn)

            anim = Animation(opacity=1, size=(dp(240), dp(60)), d=0.5 + i * 0.05, t="out_back")
            anim.start(btn)

    def go_to_chapter(self, index):
        level_screen = self.manager.get_screen("level")
        level_screen.load_chapter(index, 0)
        self.manager.current = "level"
