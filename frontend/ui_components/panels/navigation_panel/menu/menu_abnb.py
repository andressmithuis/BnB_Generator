from kivymd.app import MDApp

from AdvancedBnB import Gun, Shield

from frontend.ui_components.panels.navigation_panel.components.menu_category import MenuCategory
from frontend.ui_components.panels.navigation_panel.components.menu_item import MenuItem
from frontend.screens.generator_section import GeneratorSection
from frontend.ui_components.widgets.placeholder_bubble import PlaceholderPopup


class MenuAbnb(MenuCategory):
    def __init__(self):
        super().__init__('Advanced BnB')
        self.add_item(MenuItem('Gun Card', self.on_menu_selection))
        self.add_item(MenuItem('Shield Card', self.on_menu_selection))
        self.add_item(MenuItem('Grenade Card', self.on_menu_selection))
        self.add_item(MenuItem('Relic Card', self.on_menu_selection))
        self.add_item(MenuItem('Class Mod Card', self.on_menu_selection))

    def on_menu_selection(self,  menu_item):
        category = menu_item.get_parent_category()
        section_title = f"{category.text} - {menu_item.text}"

        equipment_obj = None
        if menu_item.text == 'Gun Card':
            equipment_obj = Gun()

        navigation_panel = self.get_navigation_panel()

        # Open Generator Page with equipment generator
        new_section = GeneratorSection(section_title, equipment_obj)
        navigation_panel.on_menu_selection(new_section)


