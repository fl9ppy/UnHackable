from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.animation import Animation
from kivymd.uix.button import MDRaisedButton
from kivymd.toast import toast
from kivy.properties import NumericProperty

KV = '''
<MasterScreen>:
    name: "master"

    MDBoxLayout:
        orientation: "vertical"
        padding: dp(24)
        spacing: dp(20)
        md_bg_color: 0.05, 0.05, 0.05, 1

        MDLabel:
            id: title_label
            text: "🧠 Master Test"
            font_style: "H5"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 0.2, 0.2, 1
            size_hint_y: None
            height: self.texture_size[1]

        MDLabel:
            id: question_label
            text: ""
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            font_style: "Subtitle1"
            size_hint_y: None
            height: self.texture_size[1]

        MDBoxLayout:
            id: option_box
            orientation: "vertical"
            spacing: dp(10)
            size_hint_y: None
            height: self.minimum_height

        MDRaisedButton:
            id: next_btn
            text: "Next"
            size_hint_x: 0.5
            size_hint_y: None
            height: dp(50)
            pos_hint: {"center_x": 0.5}
            md_bg_color: 1, 0.2, 0.2, 1
            on_release: root.next_question()
'''

Builder.load_string(KV)

class MasterScreen(Screen):
    current_q = NumericProperty(0)

    def on_enter(self):
        self.questions = [
            {
                "question": "What makes a password strong?",
                "options": ["Only numbers", "Same characters", "Mix of letters/symbols", "Your name"],
                "answer": 2
            },
            {
                "question": "What is phishing?",
                "options": ["Firewall config", "Fake message to steal info", "Antivirus", "Secure login"],
                "answer": 1
            },
            {
                "question": "How can you protect against phishing?",
                "options": ["Click links to test", "Reply fast", "Verify sources", "Ignore updates"],
                "answer": 2
            }
        ]
        self.current_q = 0
        self.correct_answers = 0
        self.load_question()

    def load_question(self):
        self.ids.option_box.clear_widgets()

        q = self.questions[self.current_q]
        self.ids.question_label.text = q["question"]

        for i, opt in enumerate(q["options"]):
            btn = MDRaisedButton(
                text=opt,
                md_bg_color=(0.2, 0.2, 0.2, 1),
                text_color=(1, 1, 1, 1),
                size_hint=(1, None),
                height=dp(50),
                pos_hint={"center_x": 0.5},
                on_release=lambda btn, idx=i: self.check_answer(idx)
            )
            btn.radius = [24, 24, 24, 24]
            self.ids.option_box.add_widget(btn)

        self.ids.question_label.opacity = 0
        Animation(opacity=1, d=0.4, t="out_quad").start(self.ids.question_label)

    def check_answer(self, selected_idx):
        correct_idx = self.questions[self.current_q]["answer"]
        if selected_idx == correct_idx:
            toast("✅ Correct!")
            self.correct_answers += 1
        else:
            toast("❌ Incorrect!")

    def next_question(self):
        if self.current_q + 1 < len(self.questions):
            self.current_q += 1
            self.load_question()
        else:
            toast(f"🎉 Done! {self.correct_answers}/{len(self.questions)} correct!")
            # TODO: Add XP update, DB save, or transition
