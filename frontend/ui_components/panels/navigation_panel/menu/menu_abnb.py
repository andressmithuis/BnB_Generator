from kivymd.app import MDApp

from AdvancedBnB import Gun

from frontend.ui_components.panels.navigation_panel.components.menu_category import MenuCategory
from frontend.ui_components.panels.navigation_panel.components.menu_item import MenuItem
from frontend.screens.generator_section import GeneratorSection


class MenuAbnb(MenuCategory):
    def __init__(self):
        super().__init__('Advanced BnB')
        self.add_item(MenuItem('Gun Card', self.on_menu_selection))
        self.add_item(MenuItem('Shield Card', self.on_menu_selection))

    def on_menu_selection(self,  menu_item):
        category = menu_item.get_parent_category()
        print(f"Selected: {category.text}/{menu_item.text}")

        section_title = f"{category.text} - {menu_item.text}"
        new_section = GeneratorSection(section_title, Gun())

        screen = MDApp.get_running_app().root
        screen.reload_main_section(new_section)

