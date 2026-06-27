import time
from threading import Thread
import numpy as np

from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

from frontend.ui_components.widgets.banner import Banner
from frontend.ui_components.panels.editor_panel import EditorPanel
from frontend.ui_components.panels.card_settings_panel import CardSettingsPanel

from AdvancedBnB import Gun

class GeneratorSection(BoxLayout):
    def __init__(self, section_title, equipment_obj, **kwargs):
        super().__init__(**kwargs)

        self.equipment_obj = equipment_obj
        self.card_iteration = 0

        self.orientation = 'vertical'

        # Title banner
        self.banner = Banner(
            title_text=section_title,
            size_hint_y=0.07,
            bg_color=(0.4, 0.4, 0.4, 1)
        )

        # Editor Panel
        self.editor_panel = EditorPanel(
            self,
            size_hint_y=0.6,
            bg_color=(0.1, 0.1, 0.1, 1)
        )

        # Equipment Properties & Mods
        properties_panel = CardSettingsPanel(
            size_hint_y=0.2
        )

        # Build Main Section
        self.add_widget(self.banner)
        self.add_widget(self.editor_panel)
        self.add_widget(properties_panel)

    def generate_new_card(self, *args):
        Thread(target = self.generator_worker, daemon=True).start()

    def generator_worker(self):
        print(f"Starting to generate Equipment Card! <{id(self.equipment_obj)}>")
        t_start = time.time()
        self.equipment_obj.generate()
        t_now = time.time()
        print(f"Equipment generated in {t_now - t_start}s")
        t_start = t_now
        self.equipment_obj.generate_card()
        t_now = time.time()
        print(f"Card rendered in {t_now - t_start}s")

        # Send result back to UI thread
        Clock.schedule_once(lambda dt: self.reload_card_image())

    def reload_card_image(self):
        t_start = time.time()
        self.editor_panel.card_inspection_panel.card_panel.replace_image_texture(img_to_texture(self.equipment_obj.generated_card[0]))
        print(f"Card loaded in UI in {time.time() - t_start}s")


def img_to_texture(pil_image):
    pil_image = pil_image.convert('RGBA')
    w, h = pil_image.size
    data = np.frombuffer(pil_image.tobytes(), dtype=np.uint8)

    texture = Texture.create(size=(w, h), colorfmt='rgba')
    texture.blit_buffer(data.tobytes(), colorfmt='rgba', bufferfmt='ubyte')
    texture.flip_vertical()

    return texture