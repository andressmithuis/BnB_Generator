from util import EquipmentProperty
from .abnb_modifiers import *


class trait_high_calibre(EquipmentProperty):
    name = 'High Calibre'
    effect = 'Add additional Dice to your Equipment Damage'
    n_dice = 1

    def load_modifiers(self):
        self.attach_modifiers([mod_high_calibre(self.n_dice)])
