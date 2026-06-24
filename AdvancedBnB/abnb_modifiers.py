from util import Dice, AdditiveModifier


class mod_high_calibre(AdditiveModifier):
    name = 'High Calibre'
    effect = 'Add additional Dice to your Equipment Damage'
    situational = True

    @property
    def effect(self):
        elemental_damage_dice = {
            1: Dice.from_string('1d4'),
            2: Dice.from_string('1d6'),
            3: Dice.from_string('1d8'),
            4: Dice.from_string('1d10'),
            5: Dice.from_string('1d12'),
            6: Dice.from_string('2d8'),
            7: Dice.from_string('2d8'),
            8: Dice.from_string('2d10'),
            9: Dice.from_string('2d10'),
            10: Dice.from_string('2d12')
        }

        equipment = self.get_linked_equipment()
        dmg_dice = elemental_damage_dice[equipment.tier]
        dmg_dice.count = self.value
        return f"When doing Ranged Damage: Damage +{dmg_dice}."
