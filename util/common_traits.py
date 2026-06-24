from util import EquipmentProperty


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
