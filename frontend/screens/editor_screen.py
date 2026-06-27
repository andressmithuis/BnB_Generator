from kivy.uix.boxlayout import BoxLayout

from frontend.ui_components.widgets.banner import Banner
from frontend.ui_components.panels.navigation_panel.navigation_panel import NavigationPanel
from frontend.ui_components.panels.editor_panel import EditorPanel
from frontend.ui_components.panels.card_settings_panel import CardSettingsPanel
from frontend.screens.generator_section import GeneratorSection

class EditorScreen(BoxLayout):
    def __init__(self):
        super().__init__()

        self.orientation = 'horizontal'

        # Navigation menu
        self.main_menu = NavigationPanel(
            self,
            size_hint_x = 0.1
        )
        self.main_menu.bg_color = (0.4, 0.4, 0.4, 1)
        self.add_widget(self.main_menu)

        # Main section
        self.main_section = GeneratorSection('???', None)
        self.add_widget(self.main_section)

    def reload_main_section(self, new_section):
        self.remove_widget(self.main_section)
        self.main_section = new_section
        self.add_widget(self.main_section)
