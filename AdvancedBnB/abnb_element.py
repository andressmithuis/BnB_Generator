from util.elements import *

# ABnB Basic Element Additions
class Slag(Element):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Slag'

# Fusion Elements
class FusionElement(Element):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.is_fusion = True
        self.fusion_elements = []

    def __repr__(self):
        str = f"{self.name}({'/'.join([f"{el}" for el in self.fusion_elements])})"
        if self.bonus != 0:
            str += f" (+{self.bonus})"

        return str

class Fusion(Element):  # Special class for Elemental Table Rolls
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Fusion'
        self.fusion_elements = []

# Fusions
class Plasma(FusionElement):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Plasma'
        self.fusion_elements = [Incendiary(), Shock()]

class Napalm(FusionElement):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Napalm'
        self.fusion_elements = [Incendiary(), Corrosive()]

class Blast(FusionElement):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Blast'
        self.fusion_elements = [Incendiary(), Explosive()]

class Chemical(FusionElement):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Chemical'
        self.fusion_elements = [Incendiary(), Slag()]

class Frostburn(FusionElement):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'FrostBurn'
        self.fusion_elements = [Incendiary(), Cryo()]

class Solar(FusionElement):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Solar'
        self.fusion_elements = [Incendiary(), Radiation()]

class Virus(FusionElement):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Virus'
        self.fusion_elements = [Shock(), Corrosive()]

class Emp(FusionElement):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Emp'
        self.fusion_elements = [Shock(), Explosive()]

class Quicksilver(FusionElement):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Quicksilver'
        self.fusion_elements = [Shock(), Slag()]

class Frostbyte(FusionElement):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'FrostByte'
        self.fusion_elements = [Shock(), Cryo()]

class Energy(FusionElement):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Energy'
        self.fusion_elements = [Shock(), Radiation()]

class Decay(FusionElement):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Decay'
        self.fusion_elements = [Corrosive(), Explosive()]

class Alkali(FusionElement):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Alkali'
        self.fusion_elements = [Corrosive(), Slag()]

class Gangrene(FusionElement):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Gangrene'
        self.fusion_elements = [Corrosive(), Cryo()]

class Fission(FusionElement):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Fission'
        self.fusion_elements = [Corrosive(), Radiation()]

class Tincture(FusionElement):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Tincture'
        self.fusion_elements = [Explosive(), Slag()]

class Void(FusionElement):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Void'
        self.fusion_elements = [Explosive(), Cryo()]

class Nuke(FusionElement):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Nuke'
        self.fusion_elements = [Explosive(), Radiation()]

class Coolant(FusionElement):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Coolant'
        self.fusion_elements = [Slag(), Cryo()]

class Force(FusionElement):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Force'
        self.fusion_elements = [Slag(), Radiation()]

class Entropy(FusionElement):
    def __init__(self, bonus=0):
        super().__init__(bonus)
        self.name = 'Entropy'
        self.fusion_elements = [Cryo(), Radiation()]

