from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.config import Config
from kivy.core.image import Image

from frontend.screens.editor_screen import EditorScreen

from file_handling import resource_path


class CardEditorApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.screen = EditorScreen()


    def build(self):
        self.theme_cls.theme_style = 'Dark'

        return self.screen



if __name__ == "__main__":
    Config.set('input', 'mouse', 'mouse,disable_multitouch')  # Disable debug touch markers on desktop
    Window.size = (1200, 800)
    
    # Start the application
    CardEditorApp().run()