
# screens/practicals/practical_email_dissection.py

from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivymd.toast import toast
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivy.clock import Clock

from database.db import save_user_progress
from utils.gamification import grant_xp, calculate_xp

Builder.load_string("""
<PracticalEmailDissection>:
    orientation: "vertical"
    padding: dp(24)
    spacing: dp(16)

    MDLabel:
        text: "✍️ Compose a Phishing Email"
        font_style: "H6"
        halign: "center"

    MDLabel:
        id: description_label
        text: ""
        halign: "center"
        theme_text_color: "Secondary"
        size_hint_y: None
        height: self.texture_size[1] + dp(4)

    MDTextField:
        id: subject_input
        hint_text: "Subject Line"
        mode: "rectangle"
        size_hint_y: None
        height: dp(48)

    MDTextField:
        id: body_input
        hint_text: "Email Body"
        multiline: True
        mode: "rectangle"
        size_hint_y: None
        height: dp(160)

    MDLabel:
        text: "💡 Tip: Make it look urgent or scary, but believable."
        theme_text_color: "Secondary"
        halign: "center"
        font_style: "Caption"

    MDRaisedButton:
        text: "Submit Email"
        pos_hint: {"center_x": 0.5}
        on_release: root.submit_email()
""")

class PracticalEmailDissection(BoxLayout):
    def __init__(self, level_screen, on_complete_callback, description="", **kwargs):
        super().__init__(**kwargs)
        self.level_screen = level_screen
        self.on_complete = on_complete_callback
        self.ids.description_label.text = description

    def submit_email(self):
        subject = self.ids.subject_input.text.strip()
        body = self.ids.body_input.text.strip()

        if not subject or not body:
            toast("❗ Fill in both subject and body.")
            return

        # Optional: You could scan body/subject here for keywords, realism, etc.
        toast("✅ Submitted!")

        screen = self.level_screen
        user_id = screen.user_id
        chapter = screen.chapter_index
        level = screen.level_index

        save_user_progress(user_id, chapter, level)
        grant_xp(user_id, calculate_xp("practical_complete"))

        screen.ids.level_box.clear_widgets()
        Clock.schedule_once(lambda dt: screen.next_level(), 0.01)
