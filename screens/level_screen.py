from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.metrics import dp
from kivymd.uix.button import MDRaisedButton
from kivymd.toast import toast
from kivy.uix.scrollview import ScrollView
from pathlib import Path
import json
from database.db import save_user_progress
from data_interface import load_chapters, load_level_data
from utils.gamification import grant_xp, calculate_xp
from utils.logic import check_answer, get_next_level
from kivy.clock import Clock

KV = '''
<LevelScreen>:
    name: "level"

    FloatLayout:
        canvas.before:
            Rectangle:
                source: "assets/bg_level.jpg"
                pos: self.pos
                size: self.size

        ScrollView:
            size_hint: 1, 1
            MDBoxLayout:
                orientation: "vertical"
                spacing: dp(20)
                padding: dp(24), dp(40)
                size_hint_y: None
                height: self.minimum_height

                MDLabel:
                    id: level_title
                    text: ""
                    font_style: "H5"
                    halign: "center"
                    size_hint_y: None
                    height: self.texture_size[1]

                MDBoxLayout:
                    orientation: "horizontal"
                    spacing: dp(12)
                    padding: dp(16)
                    size_hint_y: None
                    height: self.minimum_height
                    md_bg_color: 0.5, 0, 0, 0.7
                    radius: [20, 20, 20, 20]
                    elevation: 6

                    Image:
                        source: "assets/mascot.png"
                        size_hint: None, None
                        size: dp(60), dp(60)
                        allow_stretch: True

                    MDLabel:
                        id: question_label
                        text: ""
                        halign: "left"
                        valign: "middle"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        font_style: "H6"
                        size_hint_y: None
                        height: self.texture_size[1] + dp(48)

                MDBoxLayout:
                    id: option_box
                    orientation: "vertical"
                    spacing: dp(14)
                    size_hint_y: None
                    height: self.minimum_height

                MDBoxLayout:
                    orientation: "horizontal"
                    size_hint_y: None
                    height: dp(50)
                    spacing: dp(10)
                    MDRaisedButton:
                        text: "🏠 Home"
                        size_hint: None, None
                        size: dp(100), dp(40)
                        md_bg_color: 0.2, 0.2, 0.2, 1
                        on_release: root.go_home()

                    MDRaisedButton:
                        text: "← Chapter"
                        size_hint: None, None
                        size: dp(100), dp(40)
                        md_bg_color: 0.2, 0.2, 0.2, 1
                        on_release: root.go_back_to_chapter()

                MDBoxLayout:
                    id: level_box
                    orientation: "vertical"
                    spacing: dp(20)
'''

Builder.load_string(KV)

class LevelScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chapter_index = 0
        self.level_index = 0
        self.user_id = 1

    def on_enter(self):
        self.load_current_level()

    def load_current_level(self):
        self.ids.level_box.clear_widgets()
        self.ids.option_box.clear_widgets()

        chapters = load_chapters().get("chapters", [])
        chapter = chapters[self.chapter_index]
        chapter_file = Path(__file__).parent.parent / chapter["file"]
        with open(chapter_file, encoding="utf-8") as f:
            self.levels = json.load(f)["levels"]

        if self.level_index >= len(self.levels):
            toast("🎉 Done with this chapter!")
            return

        self.current_level = self.levels[self.level_index]
        self.render_level(self.current_level)

    def render_level(self, level):
        self.ids.option_box.clear_widgets()
        self.ids.level_box.clear_widgets()
        self.ids.question_label.text = ""
        self.ids.level_title.text = level["title"]
        Animation(font_size=22, d=0.6, t='out_back').start(self.ids.level_title)

        level_type = level.get("type", "lesson")

        if level_type == "lesson":
            self.display_lesson(level)

    def load_chapter(self, chapter_index, level_index=0, user_id=1):
        self.chapter_index = chapter_index
        self.level_index = level_index
        self.user_id = user_id
        self.load_current_level()

    def display_lesson(self, level):
        cards = level.get("cards", [])
        questions = level.get("questions", [])

        self.current_card_index = 0

        def show_next_card():
            if self.current_card_index < len(cards):
                card_text = cards[self.current_card_index]
                self.ids.question_label.text = card_text
                self.ids.option_box.clear_widgets()
                next_btn = MDRaisedButton(
                    text="Next →" if self.current_card_index < len(cards) - 1 else "Start Questions",
                    size_hint=(None, None), size=(dp(200), dp(48)),
                    md_bg_color=(1, 0.3, 0.2, 1),
                    pos_hint={"center_x": 0.5},
                    on_release=lambda x: show_next_card()
                )
                next_btn.radius = [20, 20, 20, 20]
                self.ids.option_box.add_widget(next_btn)
                self.current_card_index += 1
            else:
                self.current_question_index = 0
                self.show_question(questions)

        show_next_card()

    def show_question(self, questions):
        if self.current_question_index < len(questions):
            question = questions[self.current_question_index]
            self.ids.question_label.text = question["question"]
            self.build_options(question)
        else:
            self.next_level()

    def build_options(self, question):
        correct = question["answer"]
        self.ids.option_box.clear_widgets()
        for i, opt in enumerate(question["options"]):
            btn = MDRaisedButton(text=opt, size_hint=(None, None), size=(dp(320), dp(56)),
                                 pos_hint={"center_x": 0.5},
                                 on_release=lambda x, i=i: self.check_answer(i, correct))
            btn.radius = [32, 32, 32, 32]
            self.ids.option_box.add_widget(btn)

    def check_answer(self, selected, correct):
        if selected == correct:
            toast("✅ Correct!")
            self.current_question_index += 1
            self.show_question(self.current_level.get("questions", []))
        else:
            toast("❌ Try again")

    def next_level(self):
        self.level_index += 1
        self.load_current_level()

    def go_home(self):
        self.manager.current = "home"

    def go_back_to_chapter(self):
        self.manager.current = "chapter"