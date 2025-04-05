from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.button import MDRaisedButton
from kivy.animation import Animation
from kivymd.toast import toast
import json
from pathlib import Path
from database.db import get_user_progress
from data_interface import load_chapters
from kivy.clock import Clock
from screens.level_screen import LevelScreen

KV = '''
<ChapterScreen>:
    name: "chapter"

    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(12)
        padding: dp(16)

        MDBoxLayout:
            size_hint_y: None
            height: dp(48)
            padding: dp(8)
            MDLabel:
                id: chapter_title
                text: "Chapter"
                font_style: "H5"
                halign: "center"

            MDRaisedButton:
                text: "🏠 Home"
                size_hint: None, None
                size: dp(100), dp(40)
                pos_hint: {"right": 1}
                md_bg_color: 0.2, 0.2, 0.2, 1
                on_release: root.go_home()

        MDBoxLayout:
            orientation: "horizontal"
            size_hint_y: None
            height: dp(32)
            spacing: dp(8)
            padding: dp(8)

            MDLabel:
                id: progress_label
                text: "Progress:"
                size_hint_x: 0.3
                halign: "left"

            MDBoxLayout:
                id: progress_bar_container
                orientation: "horizontal"
                size_hint_y: None
                height: dp(24)
                spacing: dp(8)
                size_hint_x: 0.7

        ScrollView:
            MDBoxLayout:
                id: level_list
                orientation: "vertical"
                spacing: dp(16)
                padding: dp(12)
                size_hint_y: None
                height: self.minimum_height
'''

Builder.load_string(KV)

class ChapterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chapter_index = 0
        self.user_id = 1

    def set_chapter(self, chapter_index: int, user_id: int = 1):
        self.chapter_index = chapter_index
        self.user_id = user_id

    def on_enter(self):
        self.load_chapter_levels()

    def load_chapter_levels(self):
        self.ids.level_list.clear_widgets()
        chapters = load_chapters().get("chapters", [])
        if self.chapter_index >= len(chapters):
            toast("Invalid chapter index")
            return

        chapter = chapters[self.chapter_index]
        self.ids.chapter_title.text = chapter["title"]

        chapter_path = Path(__file__).parent.parent / chapter["file"]
        try:
            with open(chapter_path, encoding="utf-8") as f:
                level_data = json.load(f)["levels"]
        except Exception as e:
            toast("Failed to load chapter levels")
            print(f"[ERROR] {e}")
            return

        self.update_progress_bar(len(level_data))

        for i, level in enumerate(level_data):
            btn = MDRaisedButton(
                text=f"Level {i+1}: {level['title']}",
                size_hint=(None, None),
                size=(dp(260), dp(56)),
                pos_hint={"center_x": 0.5},
                md_bg_color=(0.9, 0.2, 0.2, 1),
                text_color=(1, 1, 1, 1),
                on_release=lambda btn, lvl=i: self.start_level(lvl)  # ⬅️ this calls the method above
            )
            btn.radius = [30, 30, 30, 30]
            anim = Animation(opacity=1, d=0.4, t="out_back")
            anim.start(btn)
            self.ids.level_list.add_widget(btn)

    def start_level(self, level_index):
        sm = self.manager
        level_screen = sm.get_screen("level")

        # ✅ IMPORTANT: actually call load_chapter so self.levels is set
        level_screen.load_chapter(self.chapter_index, level_index, self.user_id)

        sm.current = "level"
    def update_progress_bar(self, total_levels: int):
        from database.db import get_user_progress
        from kivymd.uix.progressbar import MDProgressBar

        try:
            user_progress = get_user_progress(self.user_id)
            completed = len(user_progress.get(self.chapter_index, {}))

            percent = int((completed / total_levels) * 100) if total_levels > 0 else 0
            self.ids.progress_label.text = f"Progress: {completed}/{total_levels}"

            # 🔥 Remove old progress bar
            container = self.ids.progress_bar_container
            container.clear_widgets()

            # ✅ Create new one with updated fill
            bar = MDProgressBar(
                max=100,
                value=percent,
                size_hint_x=1,
                color=(1, 0, 0, 1)
            )
            container.add_widget(bar)

            print(f"[DEBUG] {completed}/{total_levels} → {percent}% for user {self.user_id} in chapter {self.chapter_index}")

        except Exception as e:
            print(f"[ERROR] updating progress bar: {e}")
            self.ids.progress_label.text = "Progress: 0/0"
            self.ids.progress_bar_container.clear_widgets()
            self.ids.progress_bar_container.add_widget(MDProgressBar(max=100, value=0))

    def _finalize_progress(self, completed, total):
        self.ids.progress_bar.max = total
        self.ids.progress_bar.value = completed

    def go_home(self):
        self.manager.current = "home"
