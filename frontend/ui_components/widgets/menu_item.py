from kivymd.uix.button import MDFlatButton

class MenuItem(MDFlatButton):

    def __init__(self, text, on_select, **kwargs):
        super().__init__(**kwargs)

        self.text = text
        self.size_hint = (1, None)
        self.height = 35

        self.on_select = on_select
        self.bind(
            on_release = lambda x: print(f"Clicked on Menu Item <{self.text}>")
        )
