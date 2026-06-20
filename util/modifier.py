class Modifier:
    name = '<Item Modifier>'
    effect = '<Changes the Stats of an Item.>'
    situational = False  # Effects need a specific situation to occur before taking effect (effects don't get applied and modifier has a special section on the card).
    additive = False  # Same property effects can be summed up
    hidden = False  # Used to hide this modifier in the 'Mods & Checks' table on the card.


# --- Common Modifiers ---
class mod_template(Modifier):
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect
