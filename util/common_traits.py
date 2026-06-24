from .equipment import EquipmentProperty


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

