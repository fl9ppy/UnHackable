# screens/practicals/practical_phishing_detector.py

from kivy.uix.boxlayout import BoxLayout
from kivymd.toast import toast
from kivy.clock import Clock
from kivymd.uix.button import MDRaisedButton
from kivy.metrics import dp
from kivy.uix.label import Label
from database.db import save_user_progress
from utils.gamification import grant_xp, calculate_xp


class PracticalPhishingDetector(BoxLayout):
    def __init__(self, level_screen, on_complete_callback, description="", **kwargs):
        super().__init__(**kwargs)
        self.level_screen = level_screen
        self.on_complete = on_complete_callback

        self.orientation = "vertical"
        self.spacing = dp(16)
        self.padding = dp(12)

        self.emails = [
            ("""[b]from:[/b] support@paypol.com\n[b]subject:[/b] [action required] verify your account now\n\n⚠️ [color=ffaaaa]dear user, your paypal account has been flagged.[/color]\nclick the link below to verify your account or it will be suspended.""", "phishing"),
            ("""[b]from:[/b] orders@amazon.com\n[b]subject:[/b] your amazon order #112-1234567-1234567\n\nthanks for your purchase!\nyour item will arrive on friday, april 7. track it here:\n https://www.amazon.com/your-orders""", "legit"),
            ("""[b]from:[/b] info@netflx-support.net\n[b]subject:[/b] your netflix subscription is about to expire\n\nwe couldn’t process your latest payment.\nplease update your billing info immediately to avoid interruption.""", "phishing"),
            ("""[b]from:[/b] no-reply@google.com\n[b]subject:[/b] new sign-in on your account\n\nhi,\nwe noticed a new sign-in to your Google Account from Chrome on Windows.\nWas this you?\n Check activity: https://myaccount.google.com/security""", "legit"),
            ("""[b]from:[/b] hr@yourcompany.com\n[b]subject:[/b] 🧑‍💼 Upcoming performance review\n\nHi [Your Name],\nJust a heads up that your quarterly performance review is scheduled next Monday at 10am.\nLet me know if you have a conflict.""", "legit"),
        ]

        self.index = 0
        self.score = 0
        self.show_email()

    def show_email(self):
        if self.index < len(self.emails):
            # Inject formatted message into the question card
            qlabel = self.level_screen.ids.question_label
            qlabel.markup = True
            qlabel.text = self.emails[self.index][0]
            qlabel.valign = "middle"
            qlabel.halign = "center"
            qlabel.text_size = (self.level_screen.width * 0.8, None)
            qlabel.size_hint_y = None
            qlabel.height = dp(100)  # Increased box height here

            # Clear option area
            self.level_screen.ids.option_box.clear_widgets()

            # Add spacing below the red box
            self.level_screen.ids.option_box.add_widget(Label(size_hint_y=None, height=dp(12)))

            # Legit button
            btn_legit = MDRaisedButton(
                text="✅ Legit",
                size_hint=(None, None),
                size=(dp(160), dp(48)),
                pos_hint={"center_x": 0.5},
                md_bg_color=(0.2, 0.2, 0.2, 1),
                on_release=lambda x: self.check_answer("legit")
            )

            # Phishing button
            btn_phishing = MDRaisedButton(
                text="🎯 Phishing",
                size_hint=(None, None),
                size=(dp(160), dp(48)),
                pos_hint={"center_x": 0.5},
                md_bg_color=(1, 0.2, 0.2, 1),
                on_release=lambda x: self.check_answer("phishing")
            )

            # Style
            btn_legit.radius = [30, 30, 30, 30]
            btn_phishing.radius = [30, 30, 30, 30]

            # Add buttons
            self.level_screen.ids.option_box.add_widget(btn_legit)
            self.level_screen.ids.option_box.add_widget(btn_phishing)
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
        screen = self.level_screen
        user_id = screen.user_id
        chapter = screen.chapter_index
        level = screen.level_index

        save_user_progress(user_id, chapter, level)
        grant_xp(user_id, calculate_xp("practical_complete"))
        toast(f"🎉 Done! Score: {self.score}/{len(self.emails)}")

        screen.ids.level_box.clear_widgets()
        Clock.schedule_once(lambda dt: screen.next_level(), 0.01)
