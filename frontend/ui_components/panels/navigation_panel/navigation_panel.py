from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivymd.app import MDApp

from frontend import PlaceholderPopup, GeneratorSection
from frontend.ui_components.panels.colored_panel import ColoredPanel
from frontend.ui_components.panels.navigation_panel.components.menu_category import MenuCategory
from frontend.ui_components.panels.navigation_panel.menu.menu_abnb import MenuAbnb
from frontend.ui_components.panels.navigation_panel.menu.menu_sbnb import MenuSbnb
from frontend.ui_components.panels.navigation_panel.menu.menu_loadassets import MenuAssets


class NavigationPanel(ColoredPanel):
    def __init__(self,  screen, **kwargs):
        super().__init__(**kwargs)

        self.screen  = screen
        self.orientation = 'vertical'

        self.menu = ColoredPanel(
            orientation = 'vertical',
            size_hint = (1, None),
            spacing = 10,
            padding = 10
        )
        self.menu.bg_color = (0.5, 0.5, 0.5, 1)

        self.menu.bind(
            minimum_height=self.menu.setter('height')
        )
        self.add_widget(self.menu)
        self.add_widget(Widget())  # Spacer at the bottom to push menu to the top

        # --- Menu Content ---
        assets_menu = MenuAssets()
        abnb_menu = MenuAbnb()
        sbnb_menu = MenuSbnb()

        self.menu.add_widget(assets_menu)
        self.menu.add_widget(abnb_menu)
        self.menu.add_widget(sbnb_menu)

    def on_menu_selection(self, new_section):
        if new_section.equipment_obj is not None:
            screen = MDApp.get_running_app().screen
            screen.reload_main_section(new_section)
        else:
            # Menu option not implemented yet!
            popup = PlaceholderPopup()
            popup.open()

    def close_menu(self):
        menu_categories = self.menu.children
        for cat in menu_categories:
            if isinstance(cat, MenuCategory):
                cat.close()


