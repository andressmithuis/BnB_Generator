from .modifier import Modifier

class Element(Modifier):
    name = '<Unknown Element>'
    hidden = True
    bonus = 0
    is_fusion = False

    def __init__(self, bonus=0):
        self.bonus = bonus

    def apply_to_equipment(self, equipment):
        already_applied = False
        for element in equipment.elements:
            if isinstance(element, type(self)):
                already_applied = True
                break

        if already_applied is False:
            equipment.elements.append(self)

    def revert_from_equipment(self, equipment):
        for element in equipment.elements:
            if isinstance(element, type(self)):
                equipment.elements.remove(self)

    @property
    def effect(self):
        return self.name

    def __repr__(self):
        str = f"{self.name}"
        if self.bonus != 0:
            str += f" (+{self.bonus})"
        return str


# Elements
class Incendiary(Element):
    name = 'Incendiary'

class Shock(Element):
    name = 'Shock'

class Corrosive(Element):
    name = 'Corrosive'

class Explosive(Element):
    name = 'Explosive'

class Cryo(Element):
    name = 'Cryo'

class Radiation(Element):
    name = 'Radiation'

# Torgue Shield Easter Egg
class PsychicMockery(Element):
    name = 'PsychicMockery'
