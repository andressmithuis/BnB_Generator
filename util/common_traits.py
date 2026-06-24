from . import mod_is_elemental
from .equipment import EquipmentProperty
from .common_modifiers import *


class trait_is_elemental(EquipmentProperty):
    name = 'Forced Elemental'
    effect = 'Equipment cannot be without an Element'

    def load_modifiers(self):
        self.attach_modifiers([mod_is_elemental()])


class trait_elemental(EquipmentProperty):
    name = 'Elemental'
    effect = 'Equipment has an Element'
    type = 'Unknown'

    @property
    def name(self):
        return f"Elemental ({self.type})"

    @property
    def effect(self):
        return f"Equipment has a {self.type} Element."


class trait_forced_element(EquipmentProperty):
    name = 'Forced Element'
    effect = 'Equipment Element can only be of a specific kind'
    type = None

    @property
    def name(self):
        if self.type is not None:
            return f"Forced Element ({self.type.name})"

        return f"Forced Element ('ERROR')"

    @property
    def effect(self):
        if self.type is not None:
            return f"Equipment will have a {self.type.name} Element."

        return f"Equipment will have a <UNKOWN> Element."

    def load_modifiers(self):
        forced_element = mod_forced_element()
        forced_element.type = self.type
        self.attach_modifiers([forced_element])

