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

        try:
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

        except Exception as e:
            toast(f"❌ Failed to load level: {e}")
            print(f"[ERROR] {e}")

    def render_level(self, level):
        self.ids.option_box.clear_widgets()
        self.ids.level_box.clear_widgets()
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
        questions = level.get("questions", [])
        if questions:
            self.ids.question_label.text = questions[0]["question"]
            self.build_options(questions[0])

    def display_practical(self, level):
        from screens.practicals import practical_password_builder, practical_password_crack, practical_phishing_detector, practical_email_dissection, practical_iot_fix_setup, practical_iot_checklist_builder

        self.ids.option_box.clear_widgets()
        self.ids.level_box.clear_widgets()
        self.ids.question_label.text = ""

        exercise_type = level.get("exercise_type", "")
        description = level.get("description", "")

        widget = None

        if exercise_type in ["password_builder", "password_builder_lab"]:
            widget = practical_password_builder.PracticalPasswordBuilder(
                level_screen=self,
                on_complete_callback=self.next_level,
                description=description
            )
        elif exercise_type == "password_crack_sim":
            widget = practical_password_crack.PracticalPasswordCrackSim(
                level_screen=self,
                on_complete_callback=self.next_level,
                description=description
            )
        elif exercise_type == "phishing_detector_sim":
            widget = practical_phishing_detector.PracticalPhishingDetector(
                level_screen=self,
                on_complete_callback=self.next_level,
                description=description
            )
        elif exercise_type == "email_dissection_tool":
            widget = practical_email_dissection.PracticalEmailDissection(
                level_screen=self,
                on_complete_callback=self.next_level,
                description=description
            )
        elif exercise_type == "iot_fix_bad_setup":
            widget = practical_iot_fix_setup.PracticalIotFixSetup(
                level_screen=self,
                on_complete_callback=self.next_level,
                description=description
            )
        elif exercise_type == "iot_checklist_builder_tiered":
            widget = practical_iot_checklist_builder.PracticalIotChecklistBuilder(
                level_screen=self,
                on_complete_callback=self.next_level,
                description=description
            )

        if widget:
            self.ids.level_box.clear_widgets()
            self.ids.level_box.add_widget(widget)
        else:
            toast("⚠ Unknown practical type")

    def display_master(self, level):
        qlist = level.get("questions", [])
        if not qlist:
            self.ids.question_label.text = "No questions in this master level"
            return

        self.ids.question_label.text = qlist[0]["question"]
        self.build_options(qlist[0])

    def build_options(self, question):
        correct = question["answer"]

        def make_callback(index):
            return lambda btn: self.check_answer(index, correct)

        for i, opt in enumerate(question["options"]):
            btn = MDRaisedButton(
                text=opt,
                md_bg_color=(1, 0.2, 0.2, 1),
                text_color=(1, 1, 1, 1),
                font_size=dp(18),
                size_hint=(None, None),
                size=(dp(320), dp(56)),
                pos_hint={"center_x": 0.5},
                on_release=make_callback(i)
            )
            btn.radius = [32, 32, 32, 32]
            self.ids.option_box.add_widget(btn)

    def check_answer(self, selected, correct):
        if check_answer(correct, selected):
            toast("✅ Correct!")
            grant_xp(self.user_id, calculate_xp("quiz_correct"))
            save_user_progress(self.user_id, self.chapter_index, self.level_index)
            self.next_level()
        else:
            toast("❌ Try again")
            grant_xp(self.user_id, calculate_xp("quiz_wrong"))

    def next_level(self):
        if self.level_index + 1 < len(self.levels):
            self.level_index += 1
            self.load_current_level()
        else:
            master_screen = self.manager.get_screen("master")
            master_screen.set_user_context(self.user_id, self.chapter_index)
            Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'master'), 0.01)

    def load_chapter(self, chapter_index, level_index=0, user_id=1):
        self.chapter_index = chapter_index
        self.level_index = level_index
        self.user_id = user_id
        self.load_current_level()

    def go_home(self):
        self.manager.current = "home"

    def go_back_to_chapter(self):
        chapter_screen = self.manager.get_screen("chapter")
        chapter_screen.set_chapter(self.chapter_index, self.user_id)
        self.manager.current = "chapter"

    def on_leave(self):
        self.ids.option_box.clear_widgets()
        self.ids.level_box.clear_widgets()
