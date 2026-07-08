from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivymd.uix.menu import MDDropdownMenu


class DropdownButton(MDButton):
    def __init__(self, button_text, **kwargs):
        super().__init__(**kwargs)

        self.radius = [0, 0, 0, 0]

        # Construct Widget
        self.text_label = MDButtonText(
            text = button_text
        )
        self.add_widget(self.text_label)

        icon = MDButtonIcon(
            icon = 'menu-down'
        )
        self.add_widget(icon)

        self.menu = MDDropdownMenu(
            caller = self,
            items = []
        )

        self.bind(on_release=lambda x: self.menu.open())

    def set_menu_items(self, items):
        menu_items = [
            {
                'text': item,
                'on_release': lambda x=item: self.on_item_select(x)
            }
            for item in items
        ]

        self.menu.items = menu_items

    def on_item_select(self, selection):
        self.text = selection
        self.menu.dismiss()

    @property
    def text(self):
        return self.text_label.text

    @text.setter
    def text(self, value):
        self.text_label.text = value


