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

    def apply_to_equipment(self, equipment):
        equipment.forced_non_elemental = True

    def revert_from_equipment(self, equipment):
        equipment.forced_non_elemental = False


class mod_is_elemental(Modifier):
    name = 'Forced Elemental'
    effect = "This Equipment will be Elemental."
    hidden = True

    def apply_to_equipment(self, equipment):
        equipment.forced_elemental = True

    def revert_from_equipment(self, equipment):
        equipment.forced_elemental = False


class mod_non_explosive(Modifier):
    name = 'Non Explosive'
    effect = "This Equipment can't have the Explosive Element."
    hidden = True

    def apply_to_equipment(self, equipment):
        is_present = False
        for element in equipment.disabled_elements:
            if isinstance(element, Explosive):
                is_present = True
                break

        if is_present is False:
            equipment.disabled_elements.append(Explosive())

    def revert_from_equipment(self, equipment):
        for element in equipment.disabled_elements:
            if isinstance(element, Explosive):
                equipment.disabled_elements.remove(element)


class mod_elements_min(AdditiveModifier):
    name = "Minimum Elements"
    effect = "Equipment has at least a number of Elements."
    hidden = True

    @property
    def effect(self):
        return f"Equipment has at least {self.value} Elements."


class mod_elemental_roll_bonus(AdditiveModifier):
    name = "Elemental Roll Bonus"
    effect = "Add a bonus when rolling to apply Elemental Damage."
    hidden = True

    @property
    def effect(self):
        return f"Add +{self.value}% when rolling to apply Elemental Damage."
