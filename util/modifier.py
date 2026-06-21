from .elements import Explosive

class Modifier:
    name = '<Item Modifier>'
    effect = '<Changes the Stats of an Item.>'
    situational = False  # Effects need a specific situation to occur before taking effect (effects don't get applied and modifier has a special section on the card).
    additive = False  # Same property effects can be summed up
    hidden = False  # Used to hide this modifier in the 'Mods & Checks' table on the card.

    def apply_to_equipment(self, equipment):
        pass

    def revert_from_equipment(self, equipment):
        pass


# --- Common Modifiers ---
class mod_template(Modifier):
    def __init__(self, name, effect):
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
    name = 'Elemental'
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


class mod_elements_min(Modifier):
    name = "Minimum Elements"
    effect = "Equipment has at least a number of Elements."
    hidden = True
    n_elements = 0

    def __init__(self, n_elements):
        self.n_elements = n_elements
        self.effect = f"Equipment has at least {self.n_elements} Elements."

    def apply_to_equipment(self, equipment):
        equipment.min_elements = self.n_elements

    def revert_from_equipment(self, equipment):
        equipment.min_elements = 0


class mod_elemental_roll_bonus(Modifier):
    name = "Elemental Roll Bonus"
    effect = "Add a bonus when rolling to apply Elemental Damage."
    hidden = True
    bonus = 0

    def __init__(self, bonus_value):
        self.bonus = bonus_value
        self.effect = f"Add +{self.bonus}% when rolling to apply Elemental Damage."

    def apply_to_equipment(self, equipment):
        equipment.elemental_roll_bonus += self.bonus

    def revert_from_equipment(self, equipment):
        equipment.elemental_roll_bonus -= self.bonus
