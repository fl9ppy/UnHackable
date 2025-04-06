# screens/practicals/practical_iot_fix_setup.py

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
<PracticalIotFixSetup>:
    orientation: "vertical"
    padding: dp(24)
    spacing: dp(16)

    MDLabel:
        text: "🏠 Fix the Dumb Smart Home"
        font_style: "H6"
        halign: "center"

    MDLabel:
        id: description_label
        text: ""
        halign: "center"
        theme_text_color: "Secondary"
        size_hint_y: None
        height: self.texture_size[1] + dp(8)

    ScrollView:
        MDBoxLayout:
            id: problems_box
            orientation: "vertical"
            spacing: dp(12)
            size_hint_y: None
            height: self.minimum_height
""")

class PracticalIotFixSetup(BoxLayout):
    def __init__(self, level_screen, on_complete_callback, description="", **kwargs):
        super().__init__(**kwargs)
        self.level_screen = level_screen
        self.on_complete = on_complete_callback
        self.ids.description_label.text = description

        self.problems = {
            "Default password: admin / 1234": False,
            "Remote access enabled by default": False,
            "Outdated firmware": False,
            "All devices on main network": False
        }

        for issue in self.problems:
            btn = MDRaisedButton(
                text=issue,
                size_hint=(1, None),
                height=dp(48),
                on_release=lambda btn, issue=issue: self.fix_issue(issue, btn)
            )
            self.ids.problems_box.add_widget(btn)

    def fix_issue(self, issue, btn):
        if not self.problems[issue]:
            self.problems[issue] = True
            btn.text = f"✅ Fixed: {issue}"
            btn.md_bg_color = (0.2, 0.7, 0.3, 1)
        if all(self.problems.values()):
            self.finish()

    def finish(self):
        toast("🏁 All problems fixed!")
        screen = self.level_screen
        save_user_progress(screen.user_id, screen.chapter_index, screen.level_index)
        grant_xp(screen.user_id, calculate_xp("practical_complete"))
        screen.ids.level_box.clear_widgets()
        Clock.schedule_once(lambda dt: screen.next_level(), 0.01)
