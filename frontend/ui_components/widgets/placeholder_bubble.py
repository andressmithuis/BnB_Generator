from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText


class PlaceholderPopup(MDSnackbar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        text_msg = MDSnackbarText(
            text = "Not yet implemented!"
        )

        self.add_widget(text_msg)
