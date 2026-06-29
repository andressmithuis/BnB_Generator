from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText


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
            theme_text_color = 'Custom',
            text_color = (1, 0, 0, 1)
        )
        self.headericon = MDButtonIcon(icon='plus')
        self.header = MDButton(
            self.headericon,
            self.headertext,
            theme_width = 'Custom',
            size_hint = (1, None),
            height = dp(30)
        )
        self.header.bind(
            on_release = self.toggle
        )

        self.add_widget(self.header)
        self.add_widget(self.item_container)

    def add_item(self, item):
        self.item_container.add_widget(item)
        self.reload_menu()

    def toggle(self, *args):
        self.expanded = not self.expanded
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

    @property
    def text(self):
        return self.title
