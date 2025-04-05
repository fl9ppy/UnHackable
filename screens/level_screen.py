from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.metrics import dp
from kivymd.uix.button import MDRaisedButton
from kivymd.toast import toast
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from pathlib import Path
import json

from data_interface import load_chapters
from utils.gamification import grant_xp, calculate_xp
from utils.logic import check_answer, get_next_level

KV = '''
<LevelScreen>:
    name: "level"

    MDBoxLayout:
        orientation: "vertical"
        padding: dp(24)
        spacing: dp(16)
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint: 0.9, 0.95

        MDLabel:
            id: level_title
            text: ""
            font_style: "H5"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]

        ScrollView:
            MDBoxLayout:
                id: card_container
                orientation: "vertical"
                spacing: dp(12)
                size_hint_y: None
                height: self.minimum_height

        MDLabel:
            id: question_label
            text: ""
            halign: "center"
            theme_text_color: "Secondary"
            size_hint_y: None
            height: self.texture_size[1]

        MDBoxLayout:
            id: option_box
            orientation: "vertical"
            spacing: dp(10)
            size_hint_y: None
            height: self.minimum_height
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
        try:
            chapters = load_chapters().get("chapters", [])
            chapter = chapters[self.chapter_index]
            chapter_file = Path(__file__).parent.parent / chapter["file"]
            with open(chapter_file, encoding="utf-8") as f:
                levels = json.load(f)["levels"]

            if self.level_index >= len(levels):
                toast("🎉 Done with this chapter!")
                return

            self.current_level = levels[self.level_index]
            self.render_level(self.current_level)

        except Exception as e:
            toast(f"❌ Failed to load level: {e}")
            print(f"[ERROR] {e}")

    def render_level(self, level):
        self.ids.card_container.clear_widgets()
        self.ids.option_box.clear_widgets()
        self.ids.question_label.text = ""
        self.ids.level_title.text = level["title"]

        Animation(font_size=22, d=0.6, t='out_back').start(self.ids.level_title)

        level_type = level.get("type", "lesson")

        if level_type == "lesson":
            self.display_lesson(level)
        elif level_type == "practical":
            self.display_practical(level)
        elif level_type == "master":
            self.display_master(level)
        else:
            toast("❓ Unknown level type")

    def display_lesson(self, level):
        for card in level.get("cards", []):
            btn = MDRaisedButton(
                text=card,
                size_hint_y=None,
                height=dp(80),
                md_bg_color=(0.2, 0.2, 0.2, 0.9),
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )
            btn.radius = [20, 20, 20, 20]
            self.ids.card_container.add_widget(btn)

        questions = level.get("questions", [])
        if questions:
            self.ids.question_label.text = questions[0]["question"]
            self.build_options(questions[0])

    def display_practical(self, level):
        self.ids.question_label.text = level.get("description", "")
        btn = MDRaisedButton(
            text="▶ Launch Simulation",
            on_release=lambda x: toast("🚧 Simulation placeholder"),
            size_hint=(1, None),
            height=dp(60),
            md_bg_color=(0.3, 0.7, 0.3, 1)
        )
        btn.radius = [24, 24, 24, 24]
        self.ids.option_box.add_widget(btn)

    def display_master(self, level):
        qlist = level.get("questions", [])
        if not qlist:
            self.ids.question_label.text = "No questions in this master level"
            return

        self.ids.card_container.add_widget(MDLabel(
            text="🧠 Master Quiz", halign="center", size_hint_y=None, height=dp(40)
        ))
        self.ids.question_label.text = qlist[0]["question"]
        self.build_options(qlist[0])

        if "practical" in level:
            btn = MDRaisedButton(
                text="▶ Practical Challenge",
                on_release=lambda x: toast("🚧 Master practical placeholder"),
                size_hint=(1, None),
                height=dp(60),
                md_bg_color=(0.2, 0.6, 0.9, 1)
            )
            btn.radius = [24, 24, 24, 24]
            self.ids.option_box.add_widget(btn)

    def build_options(self, question):
        correct = question["answer"]
        for i, opt in enumerate(question["options"]):
            btn = MDRaisedButton(
                text=opt,
                md_bg_color=(0.9, 0.4, 0.3, 1),
                size_hint=(1, None),
                height=dp(50),
                on_release=lambda btn, idx=i: self.check_answer(idx, correct)
            )
            btn.radius = [30, 30, 30, 30]
            self.ids.option_box.add_widget(btn)

    def check_answer(self, selected, correct):
        if check_answer(correct, selected):
            toast("✅ Correct!")
            grant_xp(self.user_id, calculate_xp("quiz_correct"))
            self.next_level()
        else:
            toast("❌ Try again")
            grant_xp(self.user_id, calculate_xp("quiz_wrong"))

    def next_level(self):
        next_level = get_next_level({
            "chapter": self.chapter_index,
            "level": self.level_index
        })
        if next_level:
            self.chapter_index = next_level["chapter"]
            self.level_index = next_level["level"]
            self.load_current_level()
        else:
            toast("🏁 You've completed all levels!")

    def load_chapter(self, chapter_index: int, level_index: int = 0):
        self.chapter_index = chapter_index
        self.level_index = level_index
        self.load_current_level()
