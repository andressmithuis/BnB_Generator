from kivymd.app import MDApp

from AdvancedBnB import Gun, Shield

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
        section_title = f"{category.text} - {menu_item.text}"

        equipment_obj = None
        if menu_item.text == 'Gun Card':
            equipment_obj = Gun()
        elif menu_item.text == 'Shield Card':
            equipment_obj = Shield()

        new_section = GeneratorSection(section_title, equipment_obj)

        screen = MDApp.get_running_app().screen
        screen.reload_main_section(new_section)
