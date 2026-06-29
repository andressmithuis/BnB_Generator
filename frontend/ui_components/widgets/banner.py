from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivymd.uix.button import MDButton
from kivymd.uix.label import MDLabel

from frontend.ui_components.panels.colored_panel import ColoredPanel


class Banner(ColoredPanel):

    def __init__(self, title_text, **kwargs):
        super().__init__(**kwargs)

        orientation = 'horizontal'

        # Banner Text
        self.label = MDLabel(
            text=f"{title_text}",
            halign='center'
        )
        self.add_widget(self.label)
