from kivy.uix.boxlayout import BoxLayout

from frontend.ui_components.widgets.banner import Banner
from frontend.ui_components.panels.navigation_panel import NavigationPanel
from frontend.ui_components.panels.preview_panel import PreviewPanel
from frontend.ui_components.panels.editor_panel import EditorPanel
from frontend.ui_components.panels.card_settings_panel import CardSettingsPanel

class EditorScreen(BoxLayout):
    def __init__(self):
        super().__init__()

        self.orientation = 'horizontal'

        # Main menu
        self.main_menu = NavigationPanel(
            self,
            size_hint_x = 0.1
        )
        self.main_menu.bg_color = (0.4, 0.4, 0.4, 1)
        self.add_widget(self.main_menu)

        # Main section
        main_section = BoxLayout(
            orientation = 'vertical'
        )

        # Title banner
        self.banner = Banner(
            title_text = 'Banner Title',
            size_hint_y = 0.07,
            bg_color = (0.4, 0.4, 0.4, 1)
        )

        # Editor Panel
        editor_panel = EditorPanel(
            size_hint_y = 0.6,
            bg_color = (0.1, 0.1, 0.1, 1)
        )

        # Equipment Properties & Mods
        properties_panel = CardSettingsPanel(
            size_hint_y=0.2
        )

        # Build Main Section
        main_section.add_widget(self.banner)
        main_section.add_widget(editor_panel)
        main_section.add_widget(properties_panel)

        self.add_widget(main_section)

    def generate_card(self):
        print(f"Poof! A wild card appears!")


