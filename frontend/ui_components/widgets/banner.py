from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivymd.uix.button import MDButton
from kivymd.uix.label import MDLabel

from frontend.ui_components.panels.colored_panel import ColoredPanel
from frontend import UITheme


class Banner(ColoredPanel):

    def __init__(self, title_text, **kwargs):
        super().__init__(**kwargs)

        orientation = 'horizontal'

        # Banner Text
        self.label = MDLabel(
            text=f"{title_text}",
            halign='center',
            font_style='Headline',
            theme_font_name='Custom',
            font_name=UITheme.fonts.CARD_TITLE,
        )
        self.add_widget(self.label)
