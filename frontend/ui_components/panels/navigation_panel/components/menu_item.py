from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from frontend.ui_components.panels.navigation_panel.components.menu_category import MenuCategory
from frontend.ui_components.ui_theme import UITheme


class MenuItem(MDButton):

    def __init__(self, text, on_select, **kwargs):
        super().__init__(**kwargs)

        self.theme_width = 'Custom'
        self.size_hint = (1, None)
        self.height = dp(25)
        self.radius = [0, 0, 0, 0]

        self.theme_bg_color = 'Custom'
        self.md_bg_color = UITheme.Panel.BG_GRAY

        self.text = text
        self.enabled = False

        self.add_widget(
            MDButtonText(
                text = text,
                pos_hint = {'right': 0.95, 'center_y': 0.5},
                theme_text_color = 'Custom',
                text_color = UITheme.colors.TINY_TINA_PINK,
                theme_font_name = 'Custom',
                font_name = UITheme.fonts.CARD_TITLE
            )
        )

        self.on_select_cb = on_select
        self.bind(
            on_release = lambda x: self.on_select()
        )

    def on_select(self):
        # Prevent clicking on collapsed menu items
        if self.enabled is True:
            self.on_select_cb(self)

    def get_parent_category(self):
        cur_item = self
        while cur_item.parent is not None:
            if isinstance(cur_item.parent, MenuCategory):
                return cur_item.parent

            cur_item = cur_item.parent

        return None

