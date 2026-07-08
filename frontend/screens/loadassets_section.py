from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivymd.uix.dropdownitem import MDDropDownItem, MDDropDownItemText
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu

from frontend.ui_components.panels.colored_panel import ColoredPanel
from frontend.ui_components.widgets.banner import Banner
from frontend.ui_components.widgets.dropdown_button import DropdownButton

game_options = ['Borderlands 1', 'Borderlands 2', 'Borderlands 3', 'Borderlands TPS', "Tiny Tina's Wonderlands"]
type_options = ['Weapons', 'Shields', 'Grenades', 'Relics', 'Class Mods']


class LoadAssetsSection(ColoredPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'

        # Title banner
        self.banner = Banner(
            title_text = 'Load Images',
            size_hint_y = 0.07,
            bg_color = (0.4, 0.4, 0.4, 1)
        )
        self.add_widget(self.banner)

        # Description / How to use
        self.add_widget(
            MDLabel(
                text = '[b][u]Description[/u][/b]',
                font_style='Headline',
                adaptive_height = True,
                markup = True
            )
        )
        self.add_widget(
            MDLabel(
                text='Download images from the games to use when generating Equipment Cards. Select the <[i]game[/i]> and the item <[i]type[/i]> to load images from. This only needs to be done once.',
                adaptive_height = True,
                markup=True
            )
        )

        # Drop down menus + Load button
        self.btn_game = DropdownButton('Select Game')
        self.btn_game.set_menu_items(game_options)
        self.add_widget(self.btn_game)

        self.btn_type = DropdownButton('Select Type')
        self.btn_type.set_menu_items(type_options)
        self.add_widget(self.btn_type)

        self.btn_submit = MDButton(
            MDButtonText(
                text = 'Download'
            ),
            MDButtonIcon(
                icon = 'download'
            )
        )
        self.add_widget(self.btn_submit)
        self.btn_submit.bind(on_release=self.on_download)

        # Progress Bar

        # Build Layout
        self.add_widget(Widget())

    def on_download(self, *args):
        selected_game = self.btn_game.text
        selected_type = self.btn_type.text

        if selected_game in game_options and selected_type in type_options:
            print(f"Start downloading {selected_type} from {selected_game}!")
        else:
            print(f"Select a Game and/or Type from the menu!")
