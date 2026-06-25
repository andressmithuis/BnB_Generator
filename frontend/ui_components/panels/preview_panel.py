from kivymd.uix.label import MDLabel

from .colored_panel import ColoredPanel


class PreviewPanel(ColoredPanel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'

        self.label = MDLabel(
            text = 'Generate a Card',
            halign='center'
        )

        self.add_widget(self.label)
