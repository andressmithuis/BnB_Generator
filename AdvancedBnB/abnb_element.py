from util.elements import *

# ABnB Basic Element Additions
class Slag(Element):
    name = 'Slag'

# Fusion Elements
class FusionElement(Element):
    is_fusion = True
    fusion_elements = []

    def __repr__(self):
        str = f"{self.name}({'/'.join([f"{el}" for el in self.fusion_elements])})"
        if self.bonus != 0:
            str += f" (+{self.bonus})"

        return str

class Fusion(Element):  # Special class for Elemental Table Rolls
    name = 'Fusion'

# Fusions
class Plasma(FusionElement):
    name = 'Plasma'
    fusion_elements = [Incendiary(), Shock()]

class Napalm(FusionElement):
    name = 'Napalm'
    fusion_elements = [Incendiary(), Corrosive()]

class Blast(FusionElement):
    name = 'Blast'
    fusion_elements = [Incendiary(), Explosive()]

class Chemical(FusionElement):
    name = 'Chemical'
    fusion_elements = [Incendiary(), Slag()]

class Frostburn(FusionElement):
    name = 'FrostBurn'
    fusion_elements = [Incendiary(), Cryo()]

class Solar(FusionElement):
    name = 'Solar'
    fusion_elements = [Incendiary(), Radiation()]

class Virus(FusionElement):
    name = 'Virus'
    fusion_elements = [Shock(), Corrosive()]

class Emp(FusionElement):
    name = 'Emp'
    fusion_elements = [Shock(), Explosive()]

class Quicksilver(FusionElement):
    name = 'Quicksilver'
    fusion_elements = [Shock(), Slag()]

class Frostbyte(FusionElement):
    name = 'FrostByte'
    fusion_elements = [Shock(), Cryo()]

class Energy(FusionElement):
    name = 'Energy'
    fusion_elements = [Shock(), Radiation()]

class Decay(FusionElement):
    name = 'Decay'
    fusion_elements = [Corrosive(), Explosive()]

class Alkali(FusionElement):
    name = 'Alkali'
    fusion_elements = [Corrosive(), Slag()]

class Gangrene(FusionElement):
    name = 'Gangrene'
    fusion_elements = [Corrosive(), Cryo()]

class Fission(FusionElement):
    name = 'Fission'
    fusion_elements = [Corrosive(), Radiation()]

class Tincture(FusionElement):
    name = 'Tincture'
    fusion_elements = [Explosive(), Slag()]

class Void(FusionElement):
    name = 'Void'
    fusion_elements = [Explosive(), Cryo()]

class Nuke(FusionElement):
    name = 'Nuke'
    fusion_elements = [Explosive(), Radiation()]

class Coolant(FusionElement):
    name = 'Coolant'
    fusion_elements = [Slag(), Cryo()]

class Force(FusionElement):
    name = 'Force'
    fusion_elements = [Slag(), Radiation()]

class Entropy(FusionElement):
    name = 'Entropy'
    fusion_elements = [Cryo(), Radiation()]
