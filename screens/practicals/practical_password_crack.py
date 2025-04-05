# screens/practicals/practical_password_crack.py

from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.toast import toast
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar

Builder.load_string("""
<PracticalPasswordCrackSim>:
    orientation: "vertical"
    padding: dp(24)
    spacing: dp(20)

    MDLabel:
        id: crack_title
        text: "🔓 Cracking password..."
        font_style: "H6"
        halign: "center"

    MDLabel:
        id: password_label
        text: ""
        halign: "center"

    MDProgressBar:
        id: progress_bar
        max: 100
        value: 0
        height: dp(10)

    MDLabel:
        id: result_label
        text: ""
        halign: "center"
        theme_text_color: "Secondary"

    MDRaisedButton:
        id: next_btn
        text: "Next"
        pos_hint: {"center_x": 0.5}
        on_release: root.next_password()
""")

class PracticalPasswordCrackSim(BoxLayout):
    def __init__(self, level_screen, on_complete_callback, **kwargs):
        super().__init__(**kwargs)
        self.level_screen = level_screen
        self.on_complete = on_complete_callback

        self.passwords = [
            ("123456", 1),
            ("qwerty", 2),
            ("password1", 3),
            ("LetMeIn!", 6),
            ("5tr0ng#Pass", 10)
        ]
        self.index = 0
        self.anim_event = None
        self.start_crack()

    def start_crack(self):
        pwd, time_factor = self.passwords[self.index]
        self.ids.password_label.text = f"[ {pwd} ]"
        self.ids.result_label.text = ""
        self.ids.progress_bar.value = 0
        self.ids.next_btn.disabled = True

        self.max_ticks = time_factor * 20
        self.tick = 0

        self.anim_event = Clock.schedule_interval(self.animate_crack, 0.05)

    def animate_crack(self, dt):
        self.tick += 1
        progress = int((self.tick / self.max_ticks) * 100)
        self.ids.progress_bar.value = progress

        if self.tick >= self.max_ticks:
            Clock.unschedule(self.anim_event)
            self.ids.result_label.text = f"⏱ Cracked in {self.max_ticks // 2} seconds"
            self.ids.next_btn.disabled = False

    def next_password(self):
        self.index += 1
        if self.index >= len(self.passwords):
            self.complete()
        else:
            self.start_crack()

    def complete(self):
        from utils.gamification import grant_xp, calculate_xp
        from database.db import save_user_progress

        screen = self.level_screen
        user_id = screen.user_id
        chapter = screen.chapter_index
        level = screen.level_index

        save_user_progress(user_id, chapter, level)
        grant_xp(user_id, calculate_xp("practical_complete"))

        toast("✅ Simulation complete!")
        self.on_complete()

