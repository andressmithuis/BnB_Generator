from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.uix.widget import Widget

from frontend.ui_components.panels.colored_panel import ColoredPanel
from frontend.ui_components.widgets.menu_category import MenuCategory
from frontend.ui_components.widgets.menu_item import MenuItem


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
        self.add_widget(Widget())  # Spacer at the bottom

        # --- Menu Content ---
        abnb_menu = MenuCategory('Advanced BnB')
        abnb_menu.add_item(MenuItem('Gun Card', self.menu_selection))
        abnb_menu.add_item(MenuItem('Shield Card', self.menu_selection))

        sbnb_menu = MenuCategory('Standard BnB')
        sbnb_menu.add_item(MenuItem('Gun Card', self.menu_selection))
        sbnb_menu.add_item(MenuItem('Shield Card', self.menu_selection))
        sbnb_menu.add_item(MenuItem('Potion Card', self.menu_selection))

        self.menu.add_widget(abnb_menu)
        self.menu.add_widget(sbnb_menu)

    def selected_gun_cards(self, *args):
        print(f"Clicked on <Gun Cards>!")

    def selected_shield_cards(self, *args):
        print(f"Clicked on <Shield Cards>!")

    def menu_selection(self,  rule_name):
        print(f"Selected: {rule_name}")


