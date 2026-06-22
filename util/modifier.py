class Modifier:
    name = '<Item Modifier>'
    effect = '<Changes the Stats of an Item.>'
    situational = False  # Effects need a specific situation to occur before taking effect (effects don't get applied and modifier has a special section on the card).
    additive = False  # Same property effects can be summed up
    hidden = False  # Used to hide this modifier in the 'Mods & Checks' table on the card.
    linked_property = None

    def apply_to_equipment(self, equipment):
        pass

    def revert_from_equipment(self, equipment):
        pass
