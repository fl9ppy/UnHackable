# screens/practicals/practical_email_dissection.py

from kivy.uix.boxlayout import BoxLayout
from kivymd.toast import toast
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivy.clock import Clock
from database.db import save_user_progress
from utils.gamification import grant_xp, calculate_xp


class PracticalEmailDissection(BoxLayout):
    def __init__(self, level_screen, on_complete_callback, description="", **kwargs):
        super().__init__(**kwargs)
        self.level_screen = level_screen
        self.on_complete = on_complete_callback
        self.orientation = "vertical"
        self.spacing = dp(14)
        self.padding = [dp(72), dp(10), dp(24), dp(10)]  # ⬅️ shifted to the right

        self.subject_input = MDTextField(
            hint_text="Subject Line",
            mode="rectangle",
            size_hint=(1, None),
            height=dp(36),
        )

        self.body_input = MDTextField(
            hint_text="Email Body",
            multiline=True,
            mode="rectangle",
            size_hint=(1, None),
            height=dp(100),
        )

        self.tip = MDLabel(
            text="💡 Tip: Make it look urgent or scary, but believable.",
            halign="center",
            theme_text_color="Secondary",
            font_style="Caption",
            size_hint=(1, None),
            height=dp(20)
        )

        self.submit_button = MDRaisedButton(
            text="Submit Email",
            size_hint=(None, None),
            size=(dp(160), dp(44)),
            pos_hint={"center_x": 0.5},
            on_release=self.submit_email
        )
        self.submit_button.radius = [30, 30, 30, 30]

        self.add_widget(self.subject_input)
        self.add_widget(self.body_input)
        self.add_widget(self.tip)
        self.add_widget(self.submit_button)

    def submit_email(self, *args):
        subject = self.subject_input.text.strip()
        body = self.body_input.text.strip()

        if not subject or not body:
            toast("❗ Fill in both subject and body.")
            return

        toast("✅ Submitted!")

        screen = self.level_screen
        user_id = screen.user_id
        chapter = screen.chapter_index
        level = screen.level_index

        save_user_progress(user_id, chapter, level)
        grant_xp(user_id, calculate_xp("practical_complete"))

        screen.ids.level_box.clear_widgets()
        Clock.schedule_once(lambda dt: screen.next_level(), 0.01)
