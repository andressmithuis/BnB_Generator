from .modifier import Modifier

class Element(Modifier):
    name = '<Unknown Element>'
    hidden = True
    bonus = 0
    is_fusion = False

    def __init__(self, bonus=0):
        super().__init__()
        self.bonus = bonus

    @property
    def effect(self):
        bonus_str = f" +{self.bonus}"
        return f"{self.name}{bonus_str if self.bonus != 0 else ''}"


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
