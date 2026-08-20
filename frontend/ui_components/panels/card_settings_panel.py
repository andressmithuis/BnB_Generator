from kivy.uix.boxlayout import BoxLayout

from frontend.ui_components.panels.placeholder_panel import PlaceholderPanel


class CardSettingsPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Common Settings Panel
        common_panel = PlaceholderPanel(
            size_hint_x = 0.5,
            bg_color = (0.2, 0.2, 0.2, 1)
        )

        # Equipment Specific Panel
        specific_panel = PlaceholderPanel(
            size_hint_x = 0.5,
            bg_color=(0.2, 0.2, 0.2, 1)
        )

        self.add_widget(common_panel)
        self.add_widget(specific_panel)