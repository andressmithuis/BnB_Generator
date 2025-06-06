class Element:
    def __init__(self, bonus):
        self.name = '<Unknown>'
        self.bonus = bonus
        self.is_fusion = False

    def __repr__(self):
        str = f"{self.name}"
        if self.bonus != 0:
            str += f" (+{self.bonus})"
        return str


# Elements
class Incendiary(Element):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Incendiary'

class Shock(Element):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Shock'

class Corrosive(Element):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Corrosive'

class Explosive(Element):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Explosive'

class Cryo(Element):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Cryo'

class Radiation(Element):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Radiation'

# Torgue Shield Easter Egg
class PsychicMockery(Element):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'PsychicMockery'
