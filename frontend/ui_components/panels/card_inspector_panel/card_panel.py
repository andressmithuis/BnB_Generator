from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import StringProperty

from file_handling import resource_path
from frontend.ui_components.util import img_to_texture
from frontend.ui_components.ui_theme import UITheme
from frontend.ui_components.widgets.card_region import CardRegion
from frontend.ui_components.panels.colored_panel import ColoredPanel

class CardPanel(FloatLayout):
    img_path = StringProperty(resource_path('img/blank_cards/card_blank_common.webp'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.card_size = self.size
        self.card_pos = self.pos

        self.img_front = None
        self.img_back = None

        # Panel Image
        self.card_image = Image(
            source=self.img_path,
            allow_stretch = True
        )
        self.add_widget(self.card_image)

        self.bind(
            pos=self.update_card_size,
            width=self.update_card_size
        )

        # Card Region
        self.region_name = CardRegion()
        self.region_name.polygon = [
            (0.260, 0.967),
            (0.236, 0.942),
            (0.297, 0.847),
            (0.697, 0.847),
            (0.758, 0.942),
            (0.735, 0.967)
        ]

        #self.add_widget(self.region_name)

    def update_card_size(self, *args):
        card_h = int(self.width * 0.714)

        self.height = card_h
        self.card_size = self.size
        self.card_pos = self.pos

        self.card_image.size = self.card_size
        self.card_image.pos = self.card_pos
        self.region_name.pos = self.card_pos
        self.region_name.size = self.card_size

    def update_card_image(self, new_image):
        self.card_image.texture = img_to_texture(new_image)
