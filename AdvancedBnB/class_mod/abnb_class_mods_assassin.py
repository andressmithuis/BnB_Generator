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
    passive.name = 'Aimbot'
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
    passive.name = 'Battery'
    passive.effect = 'Increased Shield Capacity, Reduced Shield Recharge Rate.'
    passive.to_text = alt_text

    legendary_effect = Modifier()
    legendary_effect.name = 'Power Grid'
    legendary_effect.effect = 'Your Decoys gain a copy of your Shield.'

    legendary_skills = ['Grim', 'Defence Matrix', 'Battery Static', 'Overclocked Capacitor', 'Running on all Cylinders']



