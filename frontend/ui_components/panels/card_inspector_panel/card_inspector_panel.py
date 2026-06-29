
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.segmentedbutton import MDSegmentedButton, MDSegmentedButtonItem, MDSegmentButtonLabel, MDSegmentButtonIcon
from kivymd.uix.selectioncontrol import MDSwitch

from .card_panel import CardPanel
from ...ui_theme import UITheme


class CardInspectorPanel(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.selected_cardface = 0
        self.toggle_initialized = False

        # Card Image
        self.card_panel = CardPanel(
            size_hint = (1, None),
            pos_hint = {'x': 0, 'center_y': 0.5}
        )
        self.add_widget(self.card_panel)

        # Face selection button
        self.selection_front = MDSegmentedButtonItem(
            MDSegmentButtonLabel(
                text='front'
            ),
            on_release=Clock.schedule_once(lambda dt: self.on_cardface_selection(0))
        )
        self.cardface_toggle = MDSegmentedButton(
            self.selection_front,
            MDSegmentedButtonItem(
                MDSegmentButtonLabel(
                    text='back'
                ),
                on_release = Clock.schedule_once(lambda dt: self.on_cardface_selection(1))
            ),
            size_hint_x = 0.25,
            pos_hint={'center_x': 0.5, 'y': 0},
        )
        self.add_widget(self.cardface_toggle)
        Clock.schedule_once(lambda dt: self.initialize_cardface_toggle())

    def initialize_cardface_toggle(self, *args):
        # Sets the rounded corners of the Segments. Otherwise they stay square!
        self.cardface_toggle.adjust_segment_radius()
        # Selects the 'front' face as default
        self.cardface_toggle.mark_item(self.selection_front)

        self.toggle_initialized = True


    def on_cardface_selection(self, cardface, *args):
        if self.toggle_initialized is True:
            if cardface != self.selected_cardface:
                print(f"Triggered card face selection ({'front' if cardface == 0 else 'back'})")
                self.selected_cardface = cardface
                self.reload_card_image()

    def reload_card_image(self, *args):
        app = MDApp.get_running_app()
        if hasattr(app, 'screen'):
            equipment_obj = app.screen.main_section.equipment_obj
            if equipment_obj is not None:
                card_img = equipment_obj.generated_card
                if len(card_img) != 0:
                    img = card_img[self.selected_cardface]
                    self.card_panel.update_card_image(img)


