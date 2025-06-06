from util import Rarity, Dice, roll_on_table
from util.modifier import Modifier
from util.elements import *

class effect_ashen_fast_recharge(Modifier):
    name = 'Ashen Guild Effect'
    effect = 'Fast Recharge Rate.'


class effect_ashen_shield_effect(Modifier):
    name = 'Ashen Guild Effect'
    effect = 'While Equipped: Gain +10 Max Health and +3 Melee Damage.'

    def apply(self, shield):
        shield.mod_stats.setdefault('mods', {}).setdefault('max_health', 0)
        shield.mod_stats['mods']['max_health'] += 10

        shield.mod_stats.setdefault('mods', {}).setdefault('melee_dmg', 0)
        shield.mod_stats['mods']['melee_dmg'] += 3


class effect_ashen_shield_effect_2(Modifier):
    name = 'Ashen Guild Effect'
    effect = 'While Equipped: Gain +30 Max Health and +10 Health Regen.'

    def apply(self, shield):
        shield.mod_stats.setdefault('mods', {}).setdefault('max_health', 0)
        shield.mod_stats['mods']['max_health'] += 30

        shield.mod_stats.setdefault('mods', {}).setdefault('health_regen', 0)
        shield.mod_stats['mods']['health_regen'] += 10


class effect_alas_shield_effect(Modifier):
    name = 'Alas! Guild Effect'
    effect = 'Shock Resistance.'

    resistance_dice = {
        (1, 6): Dice.from_string('1d4'),
        (7, 12): Dice.from_string('1d6'),
        (13, 18): Dice.from_string('1d10')
    }

    def apply(self, item):
        item.elements.append(Shock())

    def to_text(self, shield):
        dice = roll_on_table(self.resistance_dice, shield.level)

        str = f"{dice} Shock Resistance."
        return str


class effect_alas_shield_effect_2(Modifier):
    name = 'Alas! Guild Effect'
    effect = 'Roll on each incoming Attack to decrease Damage.'

    properties = {
        (19, 24): {'threshold': 60, 'damage': 'half'},
        (25, 30): {'threshold': 70, 'damage': 'no'},
    }

    def to_text(self, shield):
        effects = roll_on_table(self.properties, shield.level)

        str = f"On incoming Attack: Roll a d100. On {effects['threshold']}+, take {effects['damage']} Damage."
        return str

class effect_dahlia_shield_effect(Modifier):
    name = 'Dahlia Guild Effect'
    effect = 'Corrosive Resistance.'

    resistance_dice = {
        (1, 6): Dice.from_string('1d4'),
        (7, 12): Dice.from_string('1d6'),
        (13, 18): Dice.from_string('1d10')
    }

    def apply(self, item):
        item.elements.append(Corrosive())

    def to_text(self, shield):
        dice = roll_on_table(self.resistance_dice, shield.level)

        str = f"{dice} Corrosive Resistance."
        return str

class effect_dahlia_shield_effect_2(Modifier):
    name = 'Dahlia Guild Effect'
    effect = 'When depleted: Spawn Gold or Grenades.'

    effect_text = {
        (19, 24): '(1/Encounter) When depleted: drop 20 gold.',
        (25, 30): 'When depleted: drops 3 Grenades into adjacent squares, each dealing 3d6 Shock Damage.',
    }

    def apply(self, item):
        if 25 <= item.level <= 30:
            item.elements.append(Shock())

    def to_text(self, shield):
        return roll_on_table(self.effect_text, shield.level)


class effect_feriore_shield_effect(Modifier):
    name = 'Feriore Guild Effect'
    effect = 'Health Regen per Recharge.'

    regen_dice = {
        (1, 6): Dice.from_string('1d4'),
        (7, 12): Dice.from_string('1d6'),
        (13, 18): Dice.from_string('1d10')
    }

    def to_text(self, shield):
        dice = roll_on_table(self.regen_dice, shield.level)

        str = f"{dice} Health Regen per Shield Recharge."
        return str


class effect_feriore_shield_effect_2(Modifier):
    name = 'Feriore Guild Effect'
    effect = ''

    effect_text = {
        (19, 24): 'Recharge 5 Shield at the start of each of your Turns.',
        (25, 30): 'When depleted: Throw like a Grenade dealing 3d8 Damage. It then returns to you.',
    }

    def to_text(self, shield):
        return roll_on_table(self.effect_text, shield.level)


class effect_malefactor_shield_effect(Modifier):
    name = 'Malefactor Guild Effect'
    effect = 'On Shield Depletion: Shock Damage to Adjacent targets.'

    dmg_dice = {
        (1, 6): Dice.from_string('1d6'),
        (7, 12): Dice.from_string('2d6'),
        (13, 18): Dice.from_string('3d6')
    }

    def apply(self, item):
        item.elements.append(Shock())

    def to_text(self, shield):
        dice = roll_on_table(self.dmg_dice, shield.level)

        str = f"On Shield Depletion: {dice} Shock Damage to adjacent Targets."
        return str


class effect_malefactor_shield_effect_2(Modifier):
    name = 'Malefactor Guild Effect'
    effect = ''

    effect_text = {
        (19, 24): 'On Shield Depletion: Pulls Targets up to 3 squares into an adjacent square of you. Then it deals 4d6 Shock Damage to adjacent Targets.',
        (25, 30): 'Deals 2d6 Incendiary Damage to adjacent squares each turn while Depleted.',
    }

    def apply(self, item):
        if 25 <= item.level <= 30:
            item.elements.append(Incendiary())

    def to_text(self, shield):
        return roll_on_table(self.effect_text, shield.level)


class effect_pangoblin_shield_effect(Modifier):
    name = 'Pangoblin Guild Effect'
    effect = 'High Capacity.'

class effect_pangoblin_shield_effect_2(Modifier):
    name = 'Pangoblin Guild Effect'
    effect = 'While NOT Depleted: Gain an Effect.'
    situational = True

    effect_text = {
        (19, 24): 'While NOT Depleted: Movement is reduced to 2 squares.',
        (25, 30): 'While NOT Depleted: +4 DMG MOD for Ranged Attacks.',
    }

    def to_text(self, shield):
        return roll_on_table(self.effect_text, shield.level)


class effect_stoker_shield_effect(Modifier):
    name = 'Stoker Guild Effect'
    effect = 'On Shield Depletion: Incendiary Damage to Adjacent targets.'

    dmg_dice = {
        (1, 6): Dice.from_string('1d6'),
        (7, 12): Dice.from_string('2d6'),
        (13, 18): Dice.from_string('3d6')
    }

    def apply(self, item):
        item.elements.append(Incendiary())

    def to_text(self, shield):
        dice = roll_on_table(self.dmg_dice, shield.level)

        str = f"On Shield Depletion: {dice} Incendiary Damage to adjacent Targets."
        return str


class effect_stoker_shield_effect_2(Modifier):
    name = 'Stoker Guild Effect'
    effect = ''
    situational = True

    effect_text = {
        (19, 24): 'Shock Damage Recharges the Shield instead of Damaging it.',
        (25, 30): 'On taking 10+ Damage from an Attack: Launches 3 Spikes at the Attacker dealing 1d6 Corrosive Damage each.',
    }

    def apply(self, item):
        if 19 <= item.level <= 24:
            item.elements.append(Shock())

        if 25 <= item.level <= 30:
            item.elements.append(Corrosive())

    def to_text(self, shield):
        return roll_on_table(self.effect_text, shield.level)


class effect_torgue_shield_effect(Modifier):
    name = 'Torgue Guild Effect'
    effect = 'Gain Max Health.'

    health_bonus = {
        (1, 6): 10,
        (7, 12): 20,
        (13, 18): 30
    }

    def apply(self, item):
        bonus = roll_on_table(self.health_bonus, item.level)
        item.mod_stats.setdefault('mods', {}).setdefault('max_health', 0)
        item.mod_stats['mods']['max_health'] += bonus


class effect_torgue_shield_effect_2(Modifier):
    name = 'Torgue Guild Effect'
    effect = ''
    situational = True

    effect_text = {
        (19, 24): "Each Turn: Insult an Enemy as Mr. Torgue, dealing 1d4 'Psychic Mockery' Damage and Taunting it.",
        (25, 30): 'On Shield Depletion: Explodes in a 3x3 square area dealing 3d6 Explosive Damage and causing Knock Back.',
    }

    def apply(self, item):
        if 19 <= item.level <= 24:
            item.elements.append(PsychicMockery())
        if 25 <= item.level <= 30:
            item.elements.append(Explosive())

    def to_text(self, shield):
        return roll_on_table(self.effect_text, shield.level)