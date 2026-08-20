import time
from threading import Thread
import numpy as np


from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivymd.app import MDApp

from frontend.ui_components.widgets.banner import Banner
from frontend.ui_components.panels.editor_panel import EditorPanel
from frontend.ui_components.panels.card_settings_panel import CardSettingsPanel
from frontend.ui_components.panels.dicerequest_panel.dicerequest_panel import DicerequestPanel

from util import DiceRequest, GenerationEvent, InfoEvent, WarningEvent, Dice, GenerationSession
from AdvancedBnB import Gun

class GeneratorSection(FloatLayout):
    def __init__(self, section_title, equipment_obj, **kwargs):
        super().__init__(**kwargs)

        self.equipment_obj = equipment_obj
        self.session = None
        self.manual_input = False
        self.card_iteration = 0

        self.static_container = BoxLayout(
            orientation = 'vertical',
            size_hint = (1, 1),
            pos_hint = {'x': 0, 'y': 0}
        )

        # Title banner
        self.banner = Banner(
            title_text=section_title,
            size_hint_y=0.07,
            bg_color=(0.4, 0.4, 0.4, 1)
        )

        # Editor Panel
        self.editor_panel = EditorPanel(
            self,
            bg_color=(0.1, 0.1, 0.1, 1)
        )
        self.editor_panel.card_inspection_panel.bind(size = self.resize_dicerequest_panel)

        # Equipment Properties & Mods
        self.properties_panel = CardSettingsPanel(
            size_hint_y=0.3
        )

        # Dice Roll panel
        self.dicerequest_panel = DicerequestPanel(
            size_hint=(None, 1),
            x = Window.width,
            bg_color=(1, 0, 0, 0.3)
        )

        # Build Main Section
        self.static_container.add_widget(self.banner)
        self.static_container.add_widget(self.editor_panel)
        self.static_container.add_widget(self.properties_panel)

        self.add_widget(self.static_container)
        self.add_widget(self.dicerequest_panel)

    def resize_dicerequest_panel(self, *args):
        self.dicerequest_panel.width = self.editor_panel.width - self.editor_panel.card_inspection_panel.width
        self.dicerequest_panel.reposition()

    def step_generation(self, input=None):
        new_event = self.session.submit(input)
        if isinstance(new_event, GenerationEvent):
            self.dicerequest_panel.add_to_log(new_event)

            if isinstance(new_event, DiceRequest):
                if self.manual_input is False:
                    dice = Dice.from_string(new_event.dice)
                    dice_result = dice.roll()
                    self.dicerequest_panel.diceroll_log.content.children[0].resolve_user_input(dice_result)
                    Clock.schedule_once(lambda dt: self.step_generation(dice_result)) # Give UI time to update EventLog
            else:
                Clock.schedule_once(lambda dt: self.step_generation())  # Give UI time to update EventLog

        else:
            # Generation is done, render card image and show in UI
            self.equipment_obj.render_card()
            self.editor_panel.card_inspection_panel.reload_card_image()
            self.editor_panel.equipment_settings.on_card_generated()

    def generate_new_card(self, manual_input:bool=False, *args) -> None:
        # Clear previous generation log
        self.dicerequest_panel.clear_log()

        # Setup new generation session
        self.session = GenerationSession(self.equipment_obj.generator_func)
        self.manual_input = manual_input

        # Begin generation process
        self.step_generation()

    def export_card(self, *args):
        self.equipment_obj.export_generated_card()
