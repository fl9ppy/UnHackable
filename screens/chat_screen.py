from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
from kivy.animation import Animation

from utils.ai_chat import get_ai_response

KV = '''
<ChatScreen>:
    name: 'chat'

    MDBoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                source: 'assets/bg_level.jpg'
                pos: self.pos
                size: self.size

        MDBoxLayout:
            size_hint_y: None
            height: dp(56)
            md_bg_color: 0.1, 0.1, 0.1, 0.9
            padding: dp(10)

            MDLabel:
                text: '🤖 Cyber Chat'
                halign: 'center'
                font_style: 'H6'
                theme_text_color: 'Custom'
                text_color: 1, 1, 1, 1

        ScrollView:
            MDBoxLayout:
                id: chat_box
                orientation: 'vertical'
                padding: dp(16)
                spacing: dp(12)
                size_hint_y: None
                height: self.minimum_height

        MDBoxLayout:
            size_hint_y: None
            height: dp(70)
            padding: dp(12)
            spacing: dp(10)
            md_bg_color: 0.1, 0.1, 0.1, 0.9

            MDTextField:
                id: message_input
                hint_text: "Ask something..."
                multiline: False
                mode: "rectangle"
                radius: [20, 20, 20, 20]
                size_hint_x: 0.8
                pos_hint: {"center_y": 0.5}
                color_mode: 'custom'
                line_color_focus: 1, 0.3, 0.3, 1
                text_color: 1, 1, 1, 1
                current_hint_text_color: 1, 1, 1, 0.6
                fill_color: 0.2, 0.2, 0.2, 0.9

            MDRaisedButton:
                text: "Send"
                size_hint_x: 0.2
                md_bg_color: 1, 0.2, 0.2, 1
                text_color: 1, 1, 1, 1
                pos_hint: {"center_y": 0.5}
                on_release: root.send_message()
'''

Builder.load_string(KV)

class ChatScreen(Screen):
    def send_message(self):
        user_input = self.ids.message_input.text.strip()
        if not user_input:
            return

        self.add_message(f"You: {user_input}", align='right')
        self.ids.message_input.text = ""

        response = get_ai_response(user_input)
        self.add_message(f"AI: {response}", align='left')

    def add_message(self, text, align='left'):
        label = MDLabel(
            text=text,
            halign=align,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="Body1",
            size_hint_y=None,
            padding=(dp(12), dp(8))
        )
        label.bind(texture_size=lambda instance, value: setattr(label, 'height', value[1] + dp(12)))
        self.ids.chat_box.add_widget(label)

        anim = Animation(opacity=1, d=0.3, t='out_quad')
        label.opacity = 0
        anim.start(label)
