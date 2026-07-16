from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp, sp
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText

from frontend.ui_components.ui_theme import UITheme


class MenuCategory(BoxLayout):

    def __init__(self, title, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.size_hint = (1, None)

        self.title = title

        self.bind(
            minimum_height = self.setter('height')
        )

        self.expanded = False

        self.item_container = GridLayout(
            cols = 1,
            size_hint_y = None,
        )

        # Category Button
        self.headertext = MDButtonText(
            text = self.title,
            #theme_font_size = 'Custom',
            #font_size = min(self.width / max(len(self.title), 1) * 1.6, sp(16)),
            halign = 'center',
            theme_text_color = 'Custom',
            text_color = UITheme.Panel.BG_GRAY,
            theme_font_name = 'Custom',
            font_name = UITheme.fonts.CARD_TITLE,
        )
        self.headericon = MDButtonIcon(
            icon='plus',
            theme_icon_color = 'Custom',
            icon_color = UITheme.Panel.BG_GRAY
        )
        self.header = MDButton(
            self.headericon,
            self.headertext,
            theme_width = 'Custom',
            size_hint = (1, None),
            height = dp(30),
            radius = [0, 0, 0, 0],
            theme_bg_color = 'Custom',
            md_bg_color = UITheme.colors.TINY_TINA_PURPLE
        )
        self.header.bind(
            on_release = self.toggle
        )

        self.add_widget(self.header)
        self.add_widget(self.item_container)

        #self.header.bind(size = self.on_resize)

    def add_item(self, item):
        self.item_container.add_widget(item)
        self.reload_menu()

    def toggle(self, *args):
        if self.expanded is True:
            self.close()
        else:
            nav_panel = self.get_navigation_panel()
            nav_panel.close_menu()
            self.expanded = True
            self.reload_menu()

    def close(self):
        self.expanded = False
        self.reload_menu()

    def reload_menu(self):
        if self.expanded:
            self.headericon.icon = 'minus-circle-outline'
            self.item_container.height = sum([child.height for child in self.item_container.children])
            self.item_container.opacity = 1
        else:
            self.headericon.icon = 'plus-circle-outline'
            self.item_container.height = 0
            self.item_container.opacity = 0

    def get_navigation_panel(self):
        return self.parent.parent

    def on_resize(self, *args):
        maximum_width = (
            self.header.right
            - self.headericon.right
        )
        print(self.header.width, maximum_width, (self.header.right, self.headericon.right))
        self.headertext.width = maximum_width
        self.headertext.text_size = self.headertext.width, None
        # TODO: Cleanup text size calculation. Get rid of the 'magic number'. Possible to get maximum Label width?
        #self.headertext.font_size = min(self.header.width * 0.55 / max(len(self.title), 1) * 1.6, self.header.height * 0.8)


    @property
    def text(self):
        return self.title
