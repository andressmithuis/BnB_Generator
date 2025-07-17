from AdvancedBnB import Manufacturers
from util import Modifier

from .abnb_class_mod_type import ClassModtype


class cm_aimbot(ClassModtype):
    name = 'Aimbot'
    manufacturer = Manufacturers.HYPERION

    prefixes = {
        (1, 2): {'prefix': 'Hacked', 'skill': 'Targeting Matrix'},
        (3, 4): {'prefix': 'Long', 'skill': 'Optics'},
        (5, 6): {'prefix': 'Tranquil', 'skill': 'Precision'},
    }

    @staticmethod
    def alt_text(item):
        bonus = {
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            6: 6,
            7: 7,
            8: 8,
            9: 9,
            10: 10
        }

        return f"+{bonus[item.tier]} ACC MOD on Ranged Attacks."

    passive = Modifier()
    passive.name = name
    passive.effect = 'Increased ACC on Ranged Attacks.'
    passive.to_text = alt_text

    legendary_effect = Modifier()
    legendary_effect.name = 'Over Critical'
    legendary_effect.effect = 'Ranged Attacks of 30+ (after Mods) are always Lethal.'

    legendary_skills = ['Targeting Matrix', 'Optics', 'Precision', 'Velocity', 'Kill Confirmed']


class cm_battery(ClassModtype):
    name = 'Battery'
    manufacturer = Manufacturers.PANGOLIN

    prefixes = {
        (1, 2): {'prefix': '9V', 'skill': 'Grim'},
        (3, 4): {'prefix': 'XL', 'skill': 'Defense Matrix'},
        (5, 6): {'prefix': 'Zappy', 'skill': 'Discharge'},
    }

    @staticmethod
    def alt_text(item):
        bonus = {
            1: {'capacity': 10, 'charge_rate': -2},
            2: {'capacity': 20, 'charge_rate': -4},
            3: {'capacity': 30, 'charge_rate': -6},
            4: {'capacity': 40, 'charge_rate': -8},
            5: {'capacity': 50, 'charge_rate': -10},
            6: {'capacity': 60, 'charge_rate': -12},
            7: {'capacity': 70, 'charge_rate': -14},
            8: {'capacity': 80, 'charge_rate': -16},
            9: {'capacity': 90, 'charge_rate': -18},
            10: {'capacity': 100, 'charge_rate': -20},
        }

        return f"+{bonus[item.tier]['capacity']} Shield Capacity. {bonus[item.tier]['charge_rate']} Shield Recharge Rate."

    passive = Modifier()
    passive.name = name
    passive.effect = 'Increased Shield Capacity, Reduced Shield Recharge Rate.'
    passive.to_text = alt_text

    legendary_effect = Modifier()
    legendary_effect.name = 'Power Grid'
    legendary_effect.effect = 'Your Decoys gain a copy of your Shield.'

    legendary_skills = ['Grim', 'Defence Matrix', 'Discharge', 'Battery Static', 'Overclocked Capacitor']


class cm_flash(ClassModtype):
    name = 'Flash'
    manufacturer = Manufacturers.MALIWAN

    prefixes = {
        (1, 2): {'prefix': 'Tricky', 'skill': 'Unforeseen'},
        (3, 4): {'prefix': 'Unpredictable', 'skill': 'Fearless'},
        (5, 6): {'prefix': 'Zappy', 'skill': 'Discharge'},
    }

    @staticmethod
    def alt_text(item):
        bonus = {
            1: {'shock_dmg': 1, 'effect_chance': 2},
            2: {'shock_dmg': 2, 'effect_chance': 4},
            3: {'shock_dmg': 3, 'effect_chance': 6},
            4: {'shock_dmg': 4, 'effect_chance': 8},
            5: {'shock_dmg': 5, 'effect_chance': 10},
            6: {'shock_dmg': 6, 'effect_chance': 12},
            7: {'shock_dmg': 7, 'effect_chance': 14},
            8: {'shock_dmg': 8, 'effect_chance': 16},
            9: {'shock_dmg': 9, 'effect_chance': 18},
            10: {'shock_dmg': 10, 'effect_chance': 20},
        }

        return f"+{bonus[item.tier]['shock_dmg']} Shock DMG. {bonus[item.tier]['effect_chance']} Electrocute Effect Chance."

    passive = Modifier()
    passive.name = name
    passive.effect = 'Increased Shock DMG and Electrocute Effect Chance.'
    passive.to_text = alt_text

    legendary_effect = Modifier()
    legendary_effect.name = 'Live Wire'
    legendary_effect.effect = (f"When your Decoy disappears, it creates a line of electricity between it and you. "
                               f"Each Enemy touching the line takes 3d6+MST MOD Shock DMG.")

    legendary_skills = ['Unforeseen', 'Fearless', 'Discharge', 'Two Fang', 'Rising Shot']


class cm_infiltrator(ClassModtype):
    name = 'Infiltrator'
    manufacturer = Manufacturers.DAHL

    prefixes = {
        (1, 2): {'prefix': 'Graceful', 'skill': 'Be Like Water'},
        (3, 4): {'prefix': 'Tricky', 'skill': 'Unforeseen'},
        (5, 6): {'prefix': 'Rugged', 'skill': 'Iron Hand'},
    }

    @staticmethod
    def alt_text(item):
        bonus = {
            1: 1,
            2: 1,
            3: 1,
            4: 1,
            5: 2,
            6: 2,
            7: 2,
            8: 2,
            9: 3,
            10: 3,
        }

        return f"+{bonus[item.tier]} Melee DMG. +{bonus[item.tier]} Ranged Hit."

    passive = Modifier()
    passive.name = name
    passive.effect = 'Increased Melee DMG and Ranged Hits.'
    passive.to_text = alt_text

    legendary_effect = Modifier()
    legendary_effect.name = 'Double Time'
    legendary_effect.effect = f"In the first round of an encounter, take 2 consecutive Turns."

    legendary_skills = ['Be Like Water', 'Unforeseen', 'Iron Hand', 'Chilling Edge', 'Like the Wind']



