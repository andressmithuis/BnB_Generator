from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRaisedButton

from frontend.ui_components.panels.common_settings import CommonSettingsPanel


class CardSettingsPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Common Settings Panel
        common_panel = CommonSettingsPanel(
            size_hint_x = 0.5,
            bg_color = (0.2, 0.2, 0.2, 1)
        )

        # Equipment Specific Panel
        specific_panel = CommonSettingsPanel(
            size_hint_x = 0.5,
            bg_color=(0.2, 0.2, 0.2, 1)
        )

        self.add_widget(common_panel)
        self.add_widget(specific_panel)