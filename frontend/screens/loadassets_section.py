from threading import Thread

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivymd.uix.dropdownitem import MDDropDownItem, MDDropDownItemText
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.progressindicator import MDLinearProgressIndicator

from resource_downloader import Downloader, DownloadProgress
from util import GeneratorSession

from frontend.ui_components.panels.colored_panel import ColoredPanel
from frontend.ui_components.widgets.banner import Banner
from frontend.ui_components.widgets.dropdown_button import DropdownButton

game_options = {
    'Borderlands 1': 'bl1',
    'Borderlands 2': 'bl2',
    'Borderlands 3': 'bl3',
    'Borderlands TPS': 'bl-tps',
    "Tiny Tina's Wonderlands": 'tt-wl'
}
type_options = {
    'Weapons': 'weapons',
    'Shields': 'shields',
    'Grenades': 'grenade-mods',
    'Relics': 'relics',
    'Class Mods': 'class-mods'
}


class LoadAssetsSection(ColoredPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'

        self.session = None
        self.downloader = None

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
        self.btn_game.set_menu_items(game_options.keys())
        self.add_widget(self.btn_game)

        self.btn_type = DropdownButton('Select Type')
        self.btn_type.set_menu_items(type_options.keys())
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

        # Image and Progress Bar
        self.loadbar = MDLinearProgressIndicator(
            size_hint_x = 0.5,
            value = 0,
            pos_hint = {'center_x': 0.5}
        )
        self.add_widget(self.loadbar)

        # Build Layout
        self.add_widget(Widget())

    def start_load(self, game, item_type):
        self.downloader = Downloader()
        Thread(target=self.downloader.download, args=(game, item_type,), daemon=True).start()
        Clock.schedule_interval(self.update_download_progress, 0.05)

        #self.session = GeneratorSession(self.downloader.download(game, item_type))
        #self.step_load()

    def step_load(self):
        event = self.session.submit(None)

        if isinstance(event, DownloadProgress):
            print(event.currently_at, event.complete_at, event.last_img)
            self.loadbar.value = event.currently_at / event.complete_at * 100
            # TODO: Update loading bar / image
            Clock.schedule_once(lambda dt: self.step_load())  # Give UI time to update
        else:
            print("Done!")
            return

    def on_download(self, *args):
        selected_game = self.btn_game.text
        selected_type = self.btn_type.text

        if selected_game in game_options and selected_type in type_options:
            print(f"Start downloading {selected_type} from {selected_game}!")
            self.start_load(game_options[selected_game], type_options[selected_type])
        else:
            print(f"Select a Game and/or Type from the menu!")

    def update_download_progress(self, *args):
        with self.downloader.lock:
            progress = self.downloader.progress
            is_done = self.downloader.is_done

        self.loadbar.value = progress

        if is_done is True:
            # Unschedule this Clock function / stop updating progressbar
            return False
