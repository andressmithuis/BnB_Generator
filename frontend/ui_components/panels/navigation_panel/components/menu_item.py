from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from frontend.ui_components.panels.navigation_panel.components.menu_category import MenuCategory


class MenuItem(MDButton):

    def __init__(self, text, on_select, **kwargs):
        super().__init__(**kwargs)

        self.theme_width = 'Custom'
        self.size_hint = (1, None)
        self.height = dp(25)

        self.text = text

        self.add_widget(
            MDButtonText(
                text = text,
                pos_hint = {'right': 0.95, 'center_y': 0.5}
            )
        )

        self.on_select = on_select
        self.bind(
            on_release = lambda x: self.on_select(self)
        )


    def get_parent_category(self):
        cur_item = self
        while cur_item.parent is not None:
            if isinstance(cur_item.parent, MenuCategory):
                return cur_item.parent

            cur_item = cur_item.parent

        return None

