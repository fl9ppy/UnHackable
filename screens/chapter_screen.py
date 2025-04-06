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
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

KV = '''
<ChapterScreen>:
    name: "chapter"

    FloatLayout:
        canvas.before:
            Rectangle:
                source: "assets/bg_level.jpg"
                pos: self.pos
                size: self.size

        MDBoxLayout:
            orientation: "vertical"
            spacing: dp(12)
            padding: dp(16)
            size_hint: 1, 1

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
                orientation: "vertical"
                size_hint_y: None
                height: dp(60)
                padding: dp(16)
                spacing: dp(8)

                MDBoxLayout:
                    id: progress_bar_container
                    size_hint_y: None
                    height: dp(20)
                    size_hint_x: 1
                    pos_hint: {"center_x": 0.5}

                MDLabel:
                    id: progress_label
                    text: "Progress: 0/0"
                    halign: "center"
                    theme_text_color: "Primary"
                    size_hint_y: None
                    height: dp(20)

            ScrollView:
                do_scroll_x: False
                do_scroll_y: True
                MDBoxLayout:
                    id: level_list
                    orientation: "vertical"
                    spacing: dp(48)
                    padding: dp(24)
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

        is_left = True
        for i, level in enumerate(level_data):
            level_container = FloatLayout(size_hint=(1, None), height=dp(120))
            icon_path = f"assets/level_icons/{i+1}.png"
            icon = Image(source=icon_path, size_hint=(None, None), size=(dp(100), dp(100)))
            icon.pos_hint = {"center_x": 0.25 if is_left else 0.75, "center_y": 0.5}
            icon.allow_stretch = True
            icon.keep_ratio = True

            btn = MDRaisedButton(
                text=f"{level['title']}",
                size_hint=(None, None),
                size=(dp(160), dp(50)),
                pos_hint={"center_x": 0.25 if is_left else 0.75, "y": 0.05},
                md_bg_color=(1, 0, 0, 1),  # Stronger red
                text_color=(1, 1, 1, 1),
                on_release=lambda btn, lvl=i: self.start_level(lvl)
            )
            btn.radius = [50, 50, 50, 50]  # 🟢 More pill-like shape
            btn.elevation = 4  # Optional: adds shadow for style

            level_container.add_widget(icon)
            level_container.add_widget(btn)
            self.ids.level_list.add_widget(level_container)

            is_left = not is_left

    def start_level(self, level_index):
        sm = self.manager
        level_screen = sm.get_screen("level")
        level_screen.load_chapter(self.chapter_index, level_index, self.user_id)
        sm.current = "level"

    def update_progress_bar(self, total_levels: int):
        from kivymd.uix.progressbar import MDProgressBar
        try:
            user_progress = get_user_progress(self.user_id)
            completed = len(user_progress.get(self.chapter_index, {}))
            percent = int((completed / total_levels) * 100) if total_levels > 0 else 0
            self.ids.progress_label.text = f"Progress: {completed}/{total_levels}"

            container = self.ids.progress_bar_container
            container.clear_widgets()
            bar = MDProgressBar(
                max=100,
                value=percent,
                size_hint_x=1,
                color=(1, 0, 0, 1)
            )
            container.add_widget(bar)
        except Exception as e:
            print(f"[ERROR] updating progress bar: {e}")
            self.ids.progress_label.text = "Progress: 0/0"
            self.ids.progress_bar_container.clear_widgets()
            self.ids.progress_bar_container.add_widget(MDProgressBar(max=100, value=0))

    def go_home(self):
        self.manager.current = "home"
