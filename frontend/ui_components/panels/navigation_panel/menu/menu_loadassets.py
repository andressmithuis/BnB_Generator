from kivymd.app import MDApp

from AdvancedBnB import Gun, Shield

from frontend.ui_components.panels.navigation_panel.components.menu_category import MenuCategory
from frontend.ui_components.panels.navigation_panel.components.menu_item import MenuItem
from frontend.screens.generator_section import GeneratorSection
from frontend.screens.loadassets_section import LoadAssetsSection


class MenuAssets(MenuCategory):
    def __init__(self):
        super().__init__('Image Assets')
        self.add_item(MenuItem('Load Images', self.on_menu_selection))

    def on_menu_selection(self, *args):
        new_section = LoadAssetsSection()

        screen = MDApp.get_running_app().screen
        screen.reload_main_section(new_section)