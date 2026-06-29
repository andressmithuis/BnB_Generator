from kivymd.app import MDApp
from kivy.core.window import Window

from screens.editor_screen import EditorScreen



class CardEditorApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.screen = EditorScreen()


    def build(self):
        self.theme_cls.theme_style = 'Dark'

        return self.screen



if __name__ == "__main__":
    Window.size = (1200, 800)
    
    # Start the application
    CardEditorApp().run()