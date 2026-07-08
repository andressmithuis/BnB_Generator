from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from frontend.ui_components.panels.colored_panel import ColoredPanel
from frontend.ui_components.panels.navigation_panel.components.menu_category import MenuCategory
from frontend.ui_components.panels.navigation_panel.components.menu_item import MenuItem
from frontend.ui_components.panels.navigation_panel.menu.menu_abnb import MenuAbnb
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

        sbnb_menu = MenuCategory('Standard BnB')
        sbnb_menu.add_item(MenuItem('Gun Card', self.on_menu_selection))
        sbnb_menu.add_item(MenuItem('Shield Card', self.on_menu_selection))
        sbnb_menu.add_item(MenuItem('Potion Card', self.on_menu_selection))

        self.menu.add_widget(assets_menu)
        self.menu.add_widget(abnb_menu)
        self.menu.add_widget(sbnb_menu)

    def on_menu_selection(self,  menu_item):
        category = menu_item.get_parent_category()
        print(f"Selected: {category.text}/{menu_item.text}")
        self.screen.main_section.change_main_section(menu_item)


