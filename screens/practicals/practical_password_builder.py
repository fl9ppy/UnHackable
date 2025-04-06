from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivymd.toast import toast
from kivy.clock import Clock

from utils.gamification import grant_xp, calculate_xp
from database.db import save_user_progress

Builder.load_string("""
<PracticalPasswordBuilder>:
    orientation: "vertical"
    spacing: dp(16)
    padding: dp(16)

    MDLabel:
        id: description_label
        text: ""
        halign: "center"
        theme_text_color: "Secondary"
        size_hint_y: None
        height: self.texture_size[1] + dp(4)

    MDTextField:
        id: password_input
        hint_text: "Type your password"
        password: True
        mode: "rectangle"
        size_hint_x: 0.9
        pos_hint: {"center_x": 0.5}
        on_text: root.analyze_password(self.text)

    MDProgressBar:
        id: strength_bar
        max: 100
        value: 0
        height: dp(8)
        size_hint_x: 0.8
        pos_hint: {"center_x": 0.5}

    MDLabel:
        id: feedback_label
        text: "Start typing..."
        halign: "center"
        theme_text_color: "Secondary"
        size_hint_y: None
        height: self.texture_size[1] + dp(4)

    Widget:
        size_hint_y: None
        height: dp(-4)

    MDRaisedButton:
        id: continue_btn
        text: "Continue"
        pos_hint: {"center_x": 0.5}
        disabled: True
        size_hint: None, None
        size: dp(160), dp(46)
        md_bg_color: 1, 0.2, 0.2, 1
        on_release: root.finish()
""")

class PracticalPasswordBuilder(BoxLayout):
    def __init__(self, level_screen, on_complete_callback, description="", **kwargs):
        super().__init__(**kwargs)
        self.level_screen = level_screen
        self.on_complete = on_complete_callback
        self.ids.description_label.text = description

    def analyze_password(self, pwd):
        score = 0
        feedback = []

        if len(pwd) >= 10:
            score += 30
        else:
            feedback.append("Too short (10+ characters)")

        if any(c.isupper() for c in pwd):
            score += 20
        else:
            feedback.append("Add uppercase letters")

        if any(c.isdigit() for c in pwd):
            score += 20
        else:
            feedback.append("Add digits")

        if any(c in "!@#$%^&*()-_=+[]{};:,.<>?" for c in pwd):
            score += 30
        else:
            feedback.append("Add special characters")

        self.ids.strength_bar.value = score
        self.ids.continue_btn.disabled = score < 80

        self.ids.feedback_label.text = "✅ Great password!" if score >= 80 else "\n".join(feedback)

    def finish(self):
        screen = self.level_screen
        user_id = screen.user_id
        chapter = screen.chapter_index
        level = screen.level_index

        save_user_progress(user_id, chapter, level)
        grant_xp(user_id, calculate_xp("practical_complete"))
        toast("✅ Password accepted!")

        screen.ids.level_box.clear_widgets()
        Clock.schedule_once(lambda dt: screen.next_level(), 0.01)
