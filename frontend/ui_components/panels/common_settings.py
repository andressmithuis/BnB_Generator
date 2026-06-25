from kivymd.uix.label import MDLabel

from frontend.ui_components.panels.colored_panel import ColoredPanel


class CommonSettingsPanel(ColoredPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        placeholder_label = MDLabel(
            text = 'Common Settings',
            halign = 'center'
        )
        self.add_widget(placeholder_label)