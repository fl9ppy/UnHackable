# screens/practicals/practical_iot_checklist_builder.py

from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.toast import toast
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.metrics import dp

from database.db import save_user_progress
from utils.gamification import grant_xp, calculate_xp

Builder.load_string("""
<PracticalIotChecklistBuilder>:
    orientation: "vertical"
    padding: dp(24)
    spacing: dp(16)

    MDLabel:
        text: "📋 IoT Security Checklist"
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
            id: checklist_box
            orientation: "vertical"
            spacing: dp(10)
            size_hint_y: None
            height: self.minimum_height

    MDRaisedButton:
        text: "✅ Submit Checklist"
        pos_hint: {"center_x": 0.5}
        on_release: root.evaluate_selection()
""")

class PracticalIotChecklistBuilder(BoxLayout):
    def __init__(self, level_screen, on_complete_callback, description="", **kwargs):
        super().__init__(**kwargs)
        self.level_screen = level_screen
        self.on_complete = on_complete_callback
        self.description = description

        # True = good practice, False = bad
        self.practices = [
            ("Use default admin credentials", False),
            ("Regularly update firmware", True),
            ("Allow remote access by default", False),
            ("Segment IoT from main WiFi", True),
            ("Disable device firewalls", False),
            ("Change passwords on setup", True),
            ("Install apps from unofficial sources", False),
            ("Enable two-factor authentication", True),
        ]

        self.checkboxes = {}

        # Wait a tick to build the UI, so self.ids is populated
        Clock.schedule_once(self.build_ui, 0.01)

    def build_ui(self, dt):
        self.ids.description_label.text = self.description

        for text, _ in self.practices:
            box = BoxLayout(orientation="horizontal", spacing=dp(8), size_hint_y=None, height=dp(48))
            checkbox = MDCheckbox(size_hint=(None, None), size=(dp(32), dp(32)))
            label = MDLabel(text=text, halign="left")
            box.add_widget(checkbox)
            box.add_widget(label)
            self.ids.checklist_box.add_widget(box)
            self.checkboxes[text] = checkbox

    def evaluate_selection(self):
        score = 0
        total = len(self.practices)

        for text, is_good in self.practices:
            selected = self.checkboxes[text].active
            if selected == is_good:
                score += 1

        toast(f"🧠 You selected {score}/{total} correctly.")

        if score >= total * 0.7:
            screen = self.level_screen
            save_user_progress(screen.user_id, screen.chapter_index, screen.level_index)
            grant_xp(screen.user_id, calculate_xp("practical_complete"))
            screen.ids.level_box.clear_widgets()
            Clock.schedule_once(lambda dt: screen.next_level(), 0.01)
        else:
            toast("❌ Try again – at least 70% needed.")
