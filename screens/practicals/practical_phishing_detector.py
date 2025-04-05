
# screens/practicals/practical_phishing_detector.py

from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.toast import toast
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp

from database.db import save_user_progress
from utils.gamification import grant_xp, calculate_xp

Builder.load_string("""
<PracticalPhishingDetector>:
    orientation: "vertical"
    padding: dp(24)
    spacing: dp(16)

    MDLabel:
        text: "🎣 Spot the Phish"
        font_style: "H6"
        halign: "center"

    MDLabel:
        id: description_label
        text: ""
        halign: "center"
        theme_text_color: "Secondary"
        size_hint_y: None
        height: self.texture_size[1] + dp(4)

    MDLabel:
        id: message_label
        text: ""
        halign: "left"
        theme_text_color: "Primary" 
        size_hint_y: None
        height: self.texture_size[1] + dp(32)
        markup: True

    MDBoxLayout:
        spacing: dp(12)
        size_hint_y: None
        height: dp(48)

        MDRaisedButton:
            text: "✅ Legit"
            on_release: root.check_answer("legit")

        MDRaisedButton:
            text: "🎯 Phishing"
            on_release: root.check_answer("phishing")
""")

class PracticalPhishingDetector(BoxLayout):
    def __init__(self, level_screen, on_complete_callback, description="", **kwargs):
        super().__init__(**kwargs)
        self.level_screen = level_screen
        self.on_complete = on_complete_callback

        self.ids.description_label.text = description

        self.emails = [
            ("""from: support@paypol.com
        subject: [action required] verify your account now

        dear user, your paypal account has been flagged.  
        click the link below to verify your account or it will be suspended.

        👉 http://secure-paypol-verification.com""", "phishing"),

            ("""from: orders@amazon.com
        subject: your amazon order #112-1234567-1234567

        thanks for your purchase!  
        your item will arrive on friday, april 7. track it here:
        👉 https://www.amazon.com/your-orders""", "legit"),

            ("""from: info@netflx-support.net
        subject: your netflix subscription is about to expire

        we couldn’t process your latest payment.  
        please update your billing info immediately to avoid interruption.

        👉 https://netflix-billing-update.net""", "phishing"),

            ("""from: no-reply@google.com
        subject: new sign-in on your account

        hi,  
        We noticed a new sign-in to your Google Account from Chrome on Windows.  
        Was this you?

        👉 Check activity: https://myaccount.google.com/security""", "legit"),

            ("""From: hr@yourcompany.com
        Subject: 🧑‍💼 Upcoming performance review

        Hi [Your Name],  
        Just a heads up that your quarterly performance review is scheduled next Monday at 10am.  
        Let me know if you have a conflict.

        Thanks,  
        – HR""", "legit"),
        ]
        self.index = 0
        self.score = 0

        self.show_email()

    def show_email(self):
        if self.index < len(self.emails):
            self.ids.message_label.text = self.emails[self.index][0]
        else:
            self.finish()

    def check_answer(self, answer):
        actual = self.emails[self.index][1]
        if answer == actual:
            self.score += 1
            toast("✅ Correct!")
        else:
            toast("❌ Nope!")

        self.index += 1
        Clock.schedule_once(lambda dt: self.show_email(), 0.4)

    def finish(self):
        from screens.level_screen import LevelScreen  # avoid circular import

        screen = self.level_screen
        user_id = screen.user_id
        chapter = screen.chapter_index
        level = screen.level_index

        save_user_progress(user_id, chapter, level)
        grant_xp(user_id, calculate_xp("practical_complete"))
        toast(f"🎉 Done! Score: {self.score}/{len(self.emails)}")

        screen.ids.level_box.clear_widgets()
        Clock.schedule_once(lambda dt: screen.next_level(), 0.01)
