from kivy.clock import Clock
from kivy.tools.pep8checker.pep8 import maximum_line_length
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp

from frontend.ui_components.ui_theme import UITheme
from frontend.ui_components.panels.colored_panel import ColoredPanel

class AdaptiveLabel(MDLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint_y = None
        self.halign = 'left'
        self.valign = 'center'

        self.bind(texture_size = self._update_height)

    def _update_height(self, *args):
        self.height = self.texture_size[1]


class EventBubble(ColoredPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_x = None
        self.size_hint_y = None
        self.adaptive_height = True
        self.orientation = 'vertical'
        self.padding = 10

        self.label = AdaptiveLabel()
        self.add_widget(self.label)
        self.add_widget(
            MDBoxLayout(
                MDTextField(
                    mode = 'filled',
                    size_hint_x = None,
                    pos_hint = {'center_y': 0.5}
                ),
                MDButton(
                    MDButtonText(
                        text='Submit'
                    ),
                    pos_hint = {'center_y': 0.5}
                ),
                size_hint = (1, None),
                pos_hint = {'center_x': 0.5}
            )
        )

        Clock.schedule_once(self._bind_parent)

    def set_text(self, text):
        self.label.text = text
        Clock.schedule_once(lambda dt: self._update_width())

    def _bind_parent(self, *args):
        if self.parent:
            self.parent.bind(size=self._update_width)
            self._update_width()

    def _update_width(self, *args):
        if not self.parent:
            return

        max_width = self.parent.width * 0.9

        # Raw size
        self.label.text_size = (None, None)
        self.label.texture_update()
        raw_width = self.label.texture_size[0]

        target_width = min(raw_width, max_width)
        self.width = target_width

        # Enable text wrapping
        self.label.text_size = (self.width, None)
        self.label.texture_update()


class LoggerEvent(AnchorLayout):
    def __init__(self, dice_request, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (1, None)

        # Event 'Bubble'
        self.bubble = EventBubble(
            bg_color = UITheme.Panel.BG_LIGHT,
        )
        #self.bubble.set_text("Super duper long extraordinary text of longness and many letterness My GAWD this text is LOOONG")
        self.bubble.set_text(dice_request.prompt)

        # Prompt

        # Input field
        # Submit button

        # Build layout
        #self.bubble.add_widget(self.prompt)
        self.add_widget(self.bubble)

