from kivymd.uix.label import MDLabel

from .colored_panel import ColoredPanel


class PlaceholderPanel(ColoredPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'

        placeholder_label = MDLabel(
            text='<Placeholder>',
            halign='center'
        )
        self.add_widget(placeholder_label)
