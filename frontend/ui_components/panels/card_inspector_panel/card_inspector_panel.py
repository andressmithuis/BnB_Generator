from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from .card_panel import CardPanel
from ...ui_theme import UITheme


class CardInspectorPanel(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.card_panel = CardPanel(
            size_hint = (1, None),
            pos_hint = {'center_y': 0.5}
        )
        self.add_widget(self.card_panel)
