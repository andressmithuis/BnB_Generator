import time
from threading import Thread
import numpy as np


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

    def export_card(self, *args):
        self.equipment_obj.export_generated_card()
        print(f"Saved Card to filesystem!")

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
        Clock.schedule_once(lambda dt: self.editor_panel.card_inspection_panel.reload_card_image())

        print(self.equipment_obj)
