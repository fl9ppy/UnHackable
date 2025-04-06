# screens/chat_screen.py

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp

from utils.ai_chat import get_ai_response

KV = '''
<ChatScreen>:
    name: 'chat'

    MDBoxLayout:
        orientation: 'vertical'

        MDBoxLayout:
            size_hint_y: None
            height: dp(56)
            md_bg_color: 0.2, 0.2, 0.2, 1

            MDLabel:
                text: '🤖 Cyber Chat'
                halign: 'center'
                font_style: 'H6'

        ScrollView:
            MDBoxLayout:
                id: chat_box
                orientation: 'vertical'
                padding: dp(12)
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height

        MDBoxLayout:
            size_hint_y: None
            height: dp(60)
            padding: dp(8)
            spacing: dp(10)

            MDTextField:
                id: message_input
                hint_text: "Ask something..."
                multiline: False
                size_hint_x: 0.8

            MDRaisedButton:
                text: "Send"
                size_hint_x: 0.2
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

        # Simulate AI response
        response = get_ai_response(user_input)
        self.add_message(f"AI: {response}", align='left')

    def add_message(self, text, align='left'):
        label = MDLabel(
            text=text,
            halign=align,
            theme_text_color="Primary",
            size_hint_y=None,
            height=self.height/10,
            padding=(dp(8), dp(4))
        )
        self.ids.chat_box.add_widget(label)
