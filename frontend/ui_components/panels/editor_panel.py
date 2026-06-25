from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel

from frontend.ui_components.panels.colored_panel import ColoredPanel
from frontend.ui_components.panels.common_settings import CommonSettingsPanel


class EditorPanel(ColoredPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Card Inspector Panel
        card_inspection_panel = BoxLayout()
        card_inspection_panel.add_widget(
            MDLabel(
                text='Card Image',
                halign='center'
            )
        )

        # Editor Menu
        editor_menu = ColoredPanel(
            size_hint_x = 0.3,
            bg_color = (0.3, 0.3, 0.3, 1)
        )
        editor_menu.add_widget(
            MDLabel(
                text = 'Editor Buttons',
                halign = 'center'
            )
        )

        # Card Settings
        settings_panel = BoxLayout(
            orientation = 'vertical',
            size_hint_x = 0.5
        )

        settings_panel.add_widget(
            CommonSettingsPanel(
                size_hint_y = 0.5
            )
        )
        settings_panel.add_widget(
            CommonSettingsPanel(
                size_hint_y=0.5
            )
        )

        # Build Panel Widgets
        self.add_widget(card_inspection_panel)
        self.add_widget(editor_menu)
        self.add_widget(settings_panel)