from .modifier import Modifier, AdditiveModifier
from .elements import Explosive

# --- Common Modifiers ---
class mod_template(Modifier):
    def __init__(self, name, effect):
        super().__init__()
        self.name = name
        self.effect = effect


class mod_non_elemental(Modifier):
    name = 'Non Elemental'
    effect = "This Equipment can't be Elemental."
    hidden = True


class mod_is_elemental(Modifier):
    name = 'Forced Elemental'
    effect = "This Equipment will be Elemental."
    hidden = True


class mod_forced_element(Modifier):
    name = 'Forced Element (UNKNOWN)'
    effect = "This Equipment will be of Element <UNKNOWN>"
    type = None
    hidden = True

    @property
    def name(self):
        if self.type is not None:
            return f"Forced Element ({self.type.name})"

        return f"Forced Element (UNKNOWN)"

    @property
    def effect(self):
        if self.type is not None:
            return f"Equipment will have a {self.type.name} Element."

        return f"Equipment will have a <UNKOWN> Element."


class mod_blacklisted_element(Modifier):
    name = 'Blacklisted Element'
    effect = "This Equipment can't have a specific Element."
    hidden = True
    type = None

    def __init__(self, type):
        super().__init__()
        self.type = type

    @property
    def effect(self):
        return f"Equipment can't have the {self.type.name} Element"


class mod_elemental_roll_number(AdditiveModifier):
    name = "Elemental rolls"
    effect = "Determines number of Elemental rolls when generating Equipment."
    hidden = True

    @property
    def effect(self):
        return f"During Equipment generation, allow for {self.value} Elemental roll(s)."


class mod_elemental_roll_bonus(AdditiveModifier):
    name = "Elemental Roll Bonus"
    effect = "Add a bonus when rolling to apply Elemental Damage."
    hidden = True

    @property
    def effect(self):
        return f"Add +{self.value}% when rolling to apply Elemental Damage."
