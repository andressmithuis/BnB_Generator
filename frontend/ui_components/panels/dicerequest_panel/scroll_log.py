from copy import deepcopy

from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList

from util import DiceRequest

from .logger_event import LoggerEvent
from frontend.ui_components.ui_theme import UITheme
from frontend.ui_components.panels.colored_panel import ColoredPanel


class ScrollableLog(ColoredPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.list_entries = MDList(
            spacing = dp(5)
        )
        self.list_entries.bind(
            minimum_height = self.list_entries.setter('height')
        )

        self.scroll_view = MDScrollView(
            do_scroll_x = False
        )
        self.scroll_view.add_widget(self.list_entries)

        for i in range(0):
            new_event = DiceRequest('1d6', 'Event occured!')
            tmp_entry = LoggerEvent(
                new_event,
                bg_color = UITheme.Panel.BG_LIGHT,
                size_hint = (1, None),
                height = dp(40)
            )
            self.list_entries.add_widget(tmp_entry)
            self.scroll_view.scroll_y = 0  # Scroll to the bottom of the list to make the most recent event visible.

        self.add_widget(self.scroll_view)

        #Clock.schedule_interval(lambda dt: self.debug_print(), 5)

    def on_touch_down_bu(self, touch):
        print(self)
        # Prevent interactions 'underneath' the DicerequestPanel from activating
        res = super().on_touch_down(touch)
        if self.collide_point(*touch.pos):

            return res

        return super().on_touch_down(touch)

    def debug_print(self, *args):
        print(self.list_entries.height)
        print(self.scroll_view.height)
        print(self.list_entries.minimum_height)
        print(self.scroll_view.do_scroll)
