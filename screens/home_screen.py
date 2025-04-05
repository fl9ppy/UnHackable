from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.button import MDRaisedButton
from data_interface import load_chapters
from utils.gamification import get_user_xp
from kivymd.toast import toast

KV = '''
<HomeScreen>:
    name: "home"

    MDBoxLayout:
        orientation: "vertical"
        padding: dp(16)
        spacing: dp(12)

        MDBoxLayout:
            size_hint_y: None
            height: dp(60)
            padding: dp(8)
            spacing: dp(16)

            MDLabel:
                id: welcome_label
                text: "Welcome!"
                font_style: "H6"
                halign: "left"
                size_hint_x: 0.7

            MDLabel:
                id: xp_label
                text: "XP: 0 | Lv. 1"
                halign: "right"
                size_hint_x: 0.3

            MDRaisedButton:
                text: "⚙"
                size_hint: None, None
                size: dp(48), dp(48)
                md_bg_color: 0.2, 0.2, 0.2, 1
                on_release: root.open_options()

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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username = "Guest"
        self.user_id = 1  # Temporary fixed ID

    def set_user(self, username: str, user_id: int):
        self.username = username
        self.user_id = user_id

    def on_enter(self):
        self.ids.welcome_label.text = f"Welcome, {self.username}!"
        xp = get_user_xp(self.user_id)
        level = self.calculate_level(xp)
        self.ids.xp_label.text = f"XP: {xp} | Lv. {level}"
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
        chapter_screen = self.manager.get_screen("chapter")
        chapter_screen.set_chapter(index, self.user_id)
        self.manager.current = "chapter"

    def open_options(self):
        toast("⚙ Options menu not implemented yet")

    def calculate_level(self, xp: int) -> int:
        if xp >= 1500:
            return 6
        elif xp >= 1000:
            return 5
        elif xp >= 500:
            return 4
        elif xp >= 250:
            return 3
        elif xp >= 100:
            return 2
        return 1
