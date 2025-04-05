from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.metrics import dp
from kivymd.uix.button import MDRaisedButton
from kivymd.toast import toast
import random

# Demo lesson format from your JSON (ch1_passwords.json)
demo_lesson = {
    "title": "Why Strong Passwords Matter",
    "cards": [
        "Many cyberattacks begin by guessing or cracking weak passwords.",
        "Attackers use tools like brute-force and dictionary attacks to try thousands of password combinations quickly.",
        "Passwords like '123456', 'admin', or 'password1' are in every attacker’s playbook."
    ],
    "questions": [
        {
            "question": "Why is '123456' a weak password?",
            "options": [
                "It uses numbers",
                "It is commonly used and easy to guess",
                "It is long",
                "It is encrypted"
            ],
            "answer": 1
        }
    ]
}

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
            bold: True

        ScrollView:
            MDBoxLayout:
                id: card_container
                orientation: "vertical"
                spacing: dp(12)
                size_hint_y: None
                height: self.minimum_height

        MDLabel:
            text: "Question:"
            font_style: "Subtitle1"
            halign: "left"
            size_hint_y: None
            height: self.texture_size[1]

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
    def on_enter(self):
        self.load_lesson(demo_lesson)

    def load_lesson(self, lesson):
        self.ids.level_title.text = lesson['title']
        Animation(font_size=22, d=0.6, t='out_back').start(self.ids.level_title)

        self.ids.card_container.clear_widgets()
        for card in lesson['cards']:
            card_btn = MDRaisedButton(
                text=card,
                md_bg_color=(0.2, 0.2, 0.2, 0.9),
                text_color=(1, 1, 1, 1),
                theme_text_color="Custom",
                padding=dp(12),
                size_hint_y=None,
                height=dp(80)
            )
            card_btn.radius = [18, 18, 18, 18]
            self.ids.card_container.add_widget(card_btn)

        question = lesson["questions"][0]
        self.ids.question_label.text = question["question"]
        self.build_options(question)

    def build_options(self, question):
        self.ids.option_box.clear_widgets()
        correct = question["answer"]

        for i, opt in enumerate(question["options"]):
            btn = MDRaisedButton(
                text=opt,
                md_bg_color=(0.9, 0.4, 0.3, 1),
                pos_hint={"center_x": 0.5},
                size_hint=(1, None),
                height=dp(50),
                on_release=lambda btn, idx=i: self.check_answer(idx, correct)
            )
            btn.radius = [30, 30, 30, 30]
            self.ids.option_box.add_widget(btn)

    def check_answer(self, idx, correct):
        if idx == correct:
            toast("✅ Correct!")
        else:
            toast("❌ Try again!")
