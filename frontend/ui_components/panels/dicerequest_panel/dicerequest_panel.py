from functools import partial

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel

from util import DiceRequest, GenerationSession

from frontend.ui_components.ui_theme import UITheme
from frontend.ui_components.panels.colored_panel import ColoredPanel
from .scroll_log import ScrollableLog
from .logger_event import LoggerEvent

class DicerequestPanel(ColoredPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.is_opened = False
        self.session = None

        # Panel header
        self.header = ColoredPanel(
            size_hint_y = 0.2,
            bg_color = UITheme.Panel.BG_BORDER
        )
        # Diceroll log
        self.diceroll_log = ScrollableLog(
            bg_color=UITheme.Panel.BG_DARK
        )

        # Buttons
        self.button_section = ColoredPanel(
            size_hint_y = 0.1,
            bg_color = UITheme.Panel.BG_LIGHT
        )
        # - Reset button
        self.button_section.add_widget(
            MDButton(
                MDButtonText(
                    text = 'Reset'
                ),
                pos_hint = {'center_y': 0.5}
            )
        )
        # - Return button
        self.button_section.add_widget(
            MDButton(
                MDButtonText(
                    text='Return'
                ),
                pos_hint={'center_y': 0.5}
            )
        )

        # Build Layout
        self.add_widget(self.header)
        self.add_widget(self.diceroll_log)
        self.add_widget(self.button_section)

        # Hide (close) the panel on launch
        Clock.schedule_once(partial(self.close_panel, 0),0)

    def reposition(self, *args):
        if self.is_opened is True:
            self.open_panel(0)
        else:
            self.close_panel(0)

    def open_panel(self, duration=0.25):
        # Set up a generation session if not yet started
        if self.session is None:
            self.start_generation()

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

    def start_generation(self):
        equipment_obj = MDApp.get_running_app().screen.main_section.equipment_obj
        self.session = equipment_obj.new_generation_session(True)
        new_event = self.session.start()
        if isinstance(new_event, DiceRequest):
            self.add_to_log(new_event)

    def add_to_log(self, event: DiceRequest):
        new_event = LoggerEvent(
            event,
            anchor_x = 'left',
        )
        self.diceroll_log.list_entries.add_widget(new_event)
        self.diceroll_log.scroll_view.scroll_y = 0  # Scroll to the bottom of the list to make the most recent event visible.

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # Process touch for the ScrollableLog (MDScrollView) and claim touch afterwards
            super().on_touch_down(touch)
            return True

        return super().on_touch_down(touch)

