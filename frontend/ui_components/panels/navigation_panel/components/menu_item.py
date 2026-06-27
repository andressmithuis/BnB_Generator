from kivymd.uix.button import MDFlatButton

from frontend.ui_components.panels.navigation_panel.components.menu_category import MenuCategory


class MenuItem(MDFlatButton):

    def __init__(self, text, on_select, **kwargs):
        super().__init__(**kwargs)

        self.text = text
        self.size_hint = (1, None)
        self.height = 35

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

