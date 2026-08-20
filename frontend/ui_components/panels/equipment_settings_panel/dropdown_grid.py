from dataclasses import dataclass

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.button import MDButton, MDButtonText
from kivy.properties import BooleanProperty
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.divider import MDDivider
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogContentContainer, MDDialogButtonContainer
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivymd.uix.scrollview import MDScrollView


from file_handling import resource_path

from frontend.ui_components.ui_theme import UITheme

@dataclass
class DropdownGridItemData:
    text : str = ''
    source : str = ''

class DropdownGridItem(MDCard, ButtonBehavior):
    selected = BooleanProperty(False)

    def __init__(self, item_data: DropdownGridItemData, **kwargs) -> None:
        super().__init__(**kwargs)

        self.state_press = 0
        self.size_hint = (None, None)
        self.padding = dp(10)

        self.parent_grid: DropdownGrid | None = None

        self.theme_bg_color = 'Custom'
        self.md_bg_color = UITheme.colors.TINY_TINA_PURPLE

        self.add_widget(
            MDBoxLayout(
                Image(
                    source=resource_path(item_data.source),
                    allow_stretch=True
                ),
                MDDivider(),
                MDLabel(
                    text=item_data.text,
                    halign='center',
                    adaptive_height=True,
                    theme_text_color='Custom',
                    text_color=UITheme.Panel.BG_GRAY,
                    theme_font_name='Custom',
                    font_name=UITheme.fonts.CARD_TITLE
                ),
                orientation='vertical',
                spacing = dp(5)
            )
        )

        self.bind(on_release=self.on_selection)
        self.bind(selected=self.on_selected)

    def set_parent(self, parent) -> None:
        self.parent_grid = parent

    def on_selection(self, *args):
        if self.parent_grid is not None:
            self.parent_grid.select_item(self)

    def on_selected(self, *args) -> None:
        if self.selected is True:
            self.md_bg_color = UITheme.colors.TINY_TINA_PINK
        else:
            self.md_bg_color = UITheme.colors.TINY_TINA_PURPLE


class DropdownGrid(BoxLayout):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.current_selection: DropdownGridItem | None = None

        self.button = MDButton(
            MDButtonText(
                text=f"Choose option..."
            ),
            on_release = self.open_dialog
        )

        self.dialog = DropdownGridDialog()
        self.add_widget(self.button)

    def add_item(self, item: DropdownGridItem) -> None:
        item.set_parent(self)
        self.dialog.grid.add_widget(item)
        self.dialog.resize_items()

    def select_item(self, item):
        if self.current_selection is not None:
            self.current_selection.selected = False

        item.selected = True
        self.current_selection = item

    def open_dialog(self, *args) -> None:
        self.dialog.open()

    def close_dialog(self) -> None:
        self.dialog.close()


class DropdownGridDialog(MDDialog):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.state_press = 0

        self.theme_bg_color = 'Custom'
        self.md_bg_color = UITheme.Panel.BG_BORDER

        # Dialog header text
        self.add_widget(
            MDDialogHeadlineText(
                text="Select a Manufacturer"
            )
        )

        # Dialog content
        self.grid = MDGridLayout(
            cols=4,
            size_hint_y = None,
            spacing=dp(8),
            padding=dp(8),
        )
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.grid.bind(size=self.resize_items)

        scroll = MDScrollView(
            size_hint_y=None,
            height=dp(400),
            do_scroll_x = False,
            md_bg_color=UITheme.Panel.BG_DARK
        )
        scroll.add_widget(self.grid)

        self.content = MDDialogContentContainer(
            MDDivider(),
            scroll,
            MDDivider(),
            orientation='vertical',
            spacing=dp(10),
        )
        self.add_widget(self.content)

        # Dialog buttons
        self.add_widget(
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(
                        text='Cancel'
                    )
                ),
                MDButton(
                    MDButtonText(
                        text='Accept'
                    )
                ),
                spacing = dp(10)
            )
        )

    def resize_items(self, *args) -> None:
        spacing = self.grid.spacing[0]
        padding = self.grid.padding[0] * 2

        col_w = (
            self.grid.width
            - padding
            - spacing * (self.grid.cols - 1)
        ) / self.grid.cols

        for child in self.grid.children:
            child.size = (col_w, col_w)

