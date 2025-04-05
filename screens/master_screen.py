from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.button import MDRaisedButton
from kivymd.toast import toast
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivy.clock import Clock
import random

from data_interface import load_chapters, load_level_data
from database.db import save_user_progress
from utils.gamification import grant_xp, calculate_xp

PASSING_SCORE = 70

KV = '''
<MasterScreen>:
    name: "master"

    MDBoxLayout:
        id: master_box
        orientation: "vertical"
        padding: dp(24)
        spacing: dp(20)

        MDBoxLayout:
            size_hint_y: None
            height: dp(40)

            MDRaisedButton:
                text: "⬅ Back"
                on_release: root.go_back()
                size_hint_x: None
                width: dp(100)

            MDLabel:
                text: "🎓 Master Test"
                font_style: "H6"
                halign: "center"

        ScrollView:
            MDBoxLayout:
                id: question_container
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(16)

        MDRaisedButton:
            text: "Submit"
            pos_hint: {"center_x": 0.5}
            on_release: root.submit_answers()
'''

Builder.load_string(KV)

class MasterScreen(Screen):
    def on_pre_enter(self):
        self.ids.question_container.clear_widgets()
        self.correct_answers = {}
        self.load_questions()

    def load_questions(self):
        chapters = load_chapters()["chapters"]
        chapter_data = load_level_data(chapters[self.chapter_index]["file"])
        self.levels = chapter_data["levels"]

        # Gather all questions from lessons
        all_questions = []
        for level in self.levels:
            if level.get("type") == "lesson":
                all_questions.extend(level.get("questions", []))

        # Pick a subset (e.g. 5 questions)
        self.questions = random.sample(all_questions, min(5, len(all_questions)))

        for i, q in enumerate(self.questions):
            q_label = MDLabel(
                text=f"{i+1}. {q['question']}",
                theme_text_color="Primary",
                size_hint_y=None,
                height=dp(24)
            )
            self.ids.question_container.add_widget(q_label)

            for j, opt in enumerate(q["options"]):
                btn = MDRaisedButton(
                    text=opt,
                    size_hint=(1, None),
                    height=dp(40),
                    on_release=lambda btn, qi=i, oj=j: self.mark_answer(qi, oj, btn)
                )
                self.ids.question_container.add_widget(btn)

    def mark_answer(self, q_index, option_index, button):
        self.correct_answers[q_index] = option_index
        toast(f"✅ Selected option {option_index+1} for Q{q_index+1}")

    def submit_answers(self):
        score = 0
        for i, q in enumerate(self.questions):
            if self.correct_answers.get(i) == q["answer"]:
                score += 1

        score_percent = int((score / len(self.questions)) * 100)

        if score_percent >= PASSING_SCORE:
            save_user_progress(self.user_id, self.chapter_index, level_id=len(self.levels))
            grant_xp(self.user_id, calculate_xp("master_complete"))
            toast(f"🏆 Passed! Score: {score_percent}%")
            Clock.schedule_once(lambda dt: self.go_back(), 1)
        else:
            toast(f"❌ Failed! Score: {score_percent}%. Try again.")

    def go_back(self):
        self.manager.current = "chapter"

    def set_user_context(self, user_id, chapter_index):
        self.user_id = user_id
        self.chapter_index = chapter_index
