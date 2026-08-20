class Modifier:
    name = '<Item Modifier>'
    effect = '<Changes the Stats of an Item.>'
    situational = False  # Effects need a specific situation to occur before taking effect (effects don't get applied and modifier has a special section on the card).
    hidden = False  # Used to hide this modifier in the 'Mods & Checks' table on the card.

    def __init__(self):
        self.linked_property = None

    def attach(self, property):
        self.linked_property = property
        property.active_mods.append(self)

    def detach(self):
        self.linked_property.active_mods.remove(self)
        self.linked_property = None

    def apply_to_equipment(self, equipment):
        pass

    def revert_from_equipment(self, equipment):
        pass

    def get_linked_equipment(self):
        return self.linked_property.linked_equipment




class AdditiveModifier(Modifier):
    value = 0
    type = ''

    def __init__(self, mod_value):
        super().__init__()
        self.value = mod_value

    @property
    def effect(self):
        return f"{self.name} {'+' if self.value > 0 else ''}{self.value}"

    def __add__(self, other):
        if isinstance(other, type(self)):
            self.value += other.value

            return self

    def __sub__(self, other):
        if isinstance(other, type(self)):
            self.value -= other.value

            return self