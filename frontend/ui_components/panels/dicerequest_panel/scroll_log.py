from kivy.metrics import dp
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout

from frontend.ui_components.panels.colored_panel import ColoredPanel


class ScrollableLog(ColoredPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.scroll_view = MDScrollView(
            do_scroll_x = False
        )

        self.content = MDBoxLayout(
            orientation = 'vertical',
            adaptive_height = True,
            spacing = dp(10),
            padding = dp(10)
        )
        self.scroll_view.add_widget(self.content)
        self.add_widget(self.scroll_view)
