from functools import partial

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock, mainthread
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivymd.uix.label import MDLabel

from util import DiceRequest, GenerationSession, GenerationEvent

from frontend.ui_components.ui_theme import UITheme
from frontend.ui_components.panels.colored_panel import ColoredPanel
from .scroll_log import ScrollableLog
from .logger_event import LoggerEventLayout

class DicerequestPanel(ColoredPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.is_opened = False
        self.session = None

        # Panel header
        self.header = ColoredPanel(
            size_hint_y = 0.2,
            bg_color = UITheme.Panel.BG_BORDER,
        )
        header_label = MDLabel(
            text='Equipment Generation Log',
            halign='center',
            theme_text_color = 'Custom',
            text_color = 'black',
            font_style = 'Headline'
        )
        self.header.add_widget(header_label)
        # Diceroll log
        self.diceroll_log = ScrollableLog(
            bg_color=UITheme.Panel.BG_DARK
        )

        # Buttons
        self.button_section = ColoredPanel(
            size_hint = (1, 0.1),
            bg_color = UITheme.Panel.BG_LIGHT,
            spacing = dp(10)
        )
        # - Reset button
        self.btn_new = MDButton(
            MDButtonText(
                text = 'New'
            ),
            MDButtonIcon(icon='dice-6'),
            pos_hint = {'center_y': 0.5}
        )
        # - Return button
        self.btn_exit = MDButton(
            MDButtonText(
                text='Exit'
            ),
            MDButtonIcon(icon='arrow-left-bold'),
            pos_hint={'center_y': 0.5}
        )
        self.button_section.add_widget(Widget())
        self.button_section.add_widget(self.btn_new)
        self.button_section.add_widget(self.btn_exit)
        self.button_section.add_widget(Widget())

        # Build Layout
        self.add_widget(self.header)
        self.add_widget(self.diceroll_log)
        self.add_widget(self.button_section)

        self.btn_exit.bind(on_release=lambda x: self.close_panel())

        # Hide (close) the panel on launch
        Clock.schedule_once(partial(self.close_panel, 0),0)

    def reposition(self, *args):
        if self.is_opened is True:
            self.open_panel(0)
        else:
            self.close_panel(0)

    def open_panel(self, duration=0.25):
        # Set up a generation session if not yet started
        current_session = MDApp.get_running_app().screen.main_section.session
        if current_session is None:
            MDApp.get_running_app().screen.main_section.start_generation(True)

        self.is_opened = True
        self.animation = Animation(
            x = Window.width - self.width,
            d = duration
        ).start(self)

    def close_panel(self, duration=0.25, *args):
        self.is_opened = False
        self.animation = Animation(
            x = Window.width,
            d = duration
        ).start(self)

    def toggle_panel(self, *args):
        self.is_opened = not self.is_opened

        if self.is_opened is True:
            self.open_panel()
        else:
            self.close_panel()

    def add_to_log(self, event: GenerationEvent):
        new_event = LoggerEventLayout(event)
        self.diceroll_log.content.add_widget(new_event)
        self.diceroll_log.scroll_view.scroll_y = 0  # Scroll to the bottom of the list to make the most recent event visible.

    def clear_log(self):
        self.diceroll_log.content.clear_widgets()
        self.diceroll_log.scroll_view.scroll_y = 0

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # Process touch for the ScrollableLog (MDScrollView) and claim touch afterwards
            super().on_touch_down(touch)
            return True

        return super().on_touch_down(touch)

