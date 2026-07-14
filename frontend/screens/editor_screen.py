import sys

from kivy.core.image import ImageLoader
from kivy.uix.boxlayout import BoxLayout

from file_handling import resource_path
from frontend.ui_components.ui_theme import UITheme
from frontend.ui_components.panels.navigation_panel.navigation_panel import NavigationPanel
from frontend.ui_components.panels.colored_panel import ColoredPanel

class EditorScreen(BoxLayout):
    def __init__(self):
        super().__init__()

        self.orientation = 'horizontal'

        # Navigation menu
        self.main_menu = NavigationPanel(
            self,
            size_hint_x = 0.15,
            bg_color = (0.4, 0.4, 0.4, 1)
        )

        # Main section
        self.main_section = ColoredPanel(
            size_hint = (1, 1),
            bg_color = UITheme.Panel.BG_DARK
        )

        # Build Page
        self.add_widget(self.main_menu)
        self.add_widget(self.main_section)

    def reload_main_section(self, new_section):
        self.remove_widget(self.main_section)
        self.main_section = new_section
        self.add_widget(self.main_section)
