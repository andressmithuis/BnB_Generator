from util import Dice, roll_on_table
from .bnb_weapon_bonus import *


class Guntype:
    name = ''
    img_file = ''

    def __repr__(self):
        return f"{self.__class__.name}"


class Rifle(Guntype):
    name = 'Combat Rifle'
    asset_dir = 'rifle'
    img_file = 'rifle.png'
    weapon_bonus = []

    @staticmethod
    def get_basestats(item_level):
        base_stats = {
            (1, 6): {'hit_dice': Dice.from_string('1d6'), 'hits_crits': {'2-7': {'hits': 1, 'crits': 0}, '8-15': {'hits': 3, 'crits': 0}, '16+': {'hits': 3, 'crits': 1}}, 'range': 6},
            (7, 12): {'hit_dice': Dice.from_string('1d8'), 'hits_crits': {'2-7': {'hits': 2, 'crits': 0}, '8-15': {'hits': 3, 'crits': 0}, '16+': {'hits': 2, 'crits': 1}}, 'range': 6},
            (13, 18): {'hit_dice': Dice.from_string('1d8'), 'hits_crits': {'2-7': {'hits': 1, 'crits': 1}, '8-15': {'hits': 2, 'crits': 1}, '16+': {'hits': 2, 'crits': 2}}, 'range': 6},
            (19, 24): {'hit_dice': Dice.from_string('2d6'), 'hits_crits': {'2-7': {'hits': 1, 'crits': 0}, '8-15': {'hits': 2, 'crits': 1}, '16+': {'hits': 3, 'crits': 1}}, 'range': 6},
            (25, 30): {'hit_dice': Dice.from_string('1d10'), 'hits_crits': {'2-7': {'hits': 1, 'crits': 1}, '8-15': {'hits': 2, 'crits': 1}, '16+': {'hits': 2, 'crits': 3}}, 'range': 6},
        }

        return roll_on_table(base_stats, item_level)


class Pistol(Guntype):
    name = 'Pistol'
    asset_dir = 'pistol'
    img_file = 'pistol.png'
    weapon_bonus = []

    @staticmethod
    def get_basestats(item_level):
        base_stats = {
            (1, 6): {'hit_dice': Dice.from_string('2d4'), 'hits_crits': {'2-7': {'hits': 1, 'crits': 0}, '8-15': {'hits': 2, 'crits': 0}, '16+': {'hits': 3, 'crits': 0}}, 'range': 5},
            (7, 12): {'hit_dice': Dice.from_string('1d6'), 'hits_crits': {'2-7': {'hits': 1, 'crits': 0}, '8-15': {'hits': 1, 'crits': 1}, '16+': {'hits': 3, 'crits': 1}}, 'range': 5},
            (13, 18): {'hit_dice': Dice.from_string('2d6'), 'hits_crits': {'2-7': {'hits': 1, 'crits': 0}, '8-15': {'hits': 2, 'crits': 0}, '16+': {'hits': 2, 'crits': 1}}, 'range': 5},
            (19, 24): {'hit_dice': Dice.from_string('2d8'), 'hits_crits': {'2-7': {'hits': 1, 'crits': 0}, '8-15': {'hits': 1, 'crits': 1}, '16+': {'hits': 1, 'crits': 2}}, 'range': 5},
            (25, 30): {'hit_dice': Dice.from_string('2d8'), 'hits_crits': {'2-7': {'hits': 2, 'crits': 0}, '8-15': {'hits': 2, 'crits': 1}, '16+': {'hits': 2, 'crits': 2}}, 'range': 5},
        }

        return roll_on_table(base_stats, item_level)


class Smg(Guntype):
    name = 'Submachine Gun'
    asset_dir = 'smg'
    img_file = 'smg.png'
    weapon_bonus = []

    @staticmethod
    def get_basestats(item_level):
        base_stats = {
            (1, 6): {'hit_dice': Dice.from_string('1d4'), 'hits_crits': {'2-7': {'hits': 2, 'crits': 0}, '8-15': {'hits': 3, 'crits': 0}, '16+': {'hits': 5, 'crits': 0}}, 'range': 5},
            (7, 12): {'hit_dice': Dice.from_string('2d4'), 'hits_crits': {'2-7': {'hits': 2, 'crits': 0}, '8-15': {'hits': 4, 'crits': 0}, '16+': {'hits': 5, 'crits': 1}}, 'range': 5},
            (13, 18): {'hit_dice': Dice.from_string('1d6'), 'hits_crits': {'2-7': {'hits': 2, 'crits': 0}, '8-15': {'hits': 3, 'crits': 1}, '16+': {'hits': 5, 'crits': 1}}, 'range': 5},
            (19, 24): {'hit_dice': Dice.from_string('2d6'), 'hits_crits': {'2-7': {'hits': 2, 'crits': 0}, '8-15': {'hits': 2, 'crits': 1}, '16+': {'hits': 4, 'crits': 1}}, 'range': 5},
            (25, 30): {'hit_dice': Dice.from_string('1d10'), 'hits_crits': {'2-7': {'hits': 2, 'crits': 2}, '8-15': {'hits': 3, 'crits': 2}, '16+': {'hits': 5, 'crits': 2}}, 'range': 5},
        }

        return roll_on_table(base_stats, item_level)


class Shotgun(Guntype):
    name = 'Shotgun'
    asset_dir = 'shotgun'
    img_file = 'shotgun.png'
    weapon_bonus = [BonusShotgun()]

    @staticmethod
    def get_basestats(item_level):
        base_stats = {
            (1, 6): {'hit_dice': Dice.from_string('1d8'), 'hits_crits': {'2-7': {'hits': 1, 'crits': 0}, '8-15': {'hits': 2, 'crits': 0}, '16+': {'hits': 1, 'crits': 1}}, 'range': 4},
            (7, 12): {'hit_dice': Dice.from_string('2d8'), 'hits_crits': {'2-7': {'hits': 1, 'crits': 0}, '8-15': {'hits': 2, 'crits': 0}, '16+': {'hits': 2, 'crits': 1}}, 'range': 4},
            (13, 18): {'hit_dice': Dice.from_string('1d8'), 'hits_crits': {'2-7': {'hits': 1, 'crits': 1}, '8-15': {'hits': 2, 'crits': 1}, '16+': {'hits': 2, 'crits': 2}}, 'range': 4},
            (19, 24): {'hit_dice': Dice.from_string('2d10'), 'hits_crits': {'2-7': {'hits': 1, 'crits': 0}, '8-15': {'hits': 1, 'crits': 1}, '16+': {'hits': 2, 'crits': 1}}, 'range': 4},
            (25, 30): {'hit_dice': Dice.from_string('1d12'), 'hits_crits': {'2-7': {'hits': 1, 'crits': 1}, '8-15': {'hits': 2, 'crits': 1}, '16+': {'hits': 2, 'crits': 2}}, 'range': 4},
        }

        return roll_on_table(base_stats, item_level)


class Sniper(Guntype):
    name = 'Sniper Rifle'
    asset_dir = 'sniper'
    img_file = 'sniper.png'
    weapon_bonus = [BonusSniper()]

    @staticmethod
    def get_basestats(item_level):
        base_stats = {
            (1, 6): {'hit_dice': Dice.from_string('1d10'), 'hits_crits': {'2-7': {'hits': 0, 'crits': 0}, '8-15': {'hits': 1, 'crits': 0}, '16+': {'hits': 1, 'crits': 1}}, 'range': 8},
            (7, 12): {'hit_dice': Dice.from_string('1d12'), 'hits_crits': {'2-7': {'hits': 0, 'crits': 0}, '8-15': {'hits': 1, 'crits': 0}, '16+': {'hits': 1, 'crits': 1}}, 'range': 8},
            (13, 18): {'hit_dice': Dice.from_string('1d10'), 'hits_crits': {'2-7': {'hits': 1, 'crits': 0}, '8-15': {'hits': 1, 'crits': 1}, '16+': {'hits': 1, 'crits': 2}}, 'range': 8},
            (19, 24): {'hit_dice': Dice.from_string('2d10'), 'hits_crits': {'2-7': {'hits': 1, 'crits': 0}, '8-15': {'hits': 1, 'crits': 1}, '16+': {'hits': 1, 'crits': 2}}, 'range': 8},
            (25, 30): {'hit_dice': Dice.from_string('1d12'), 'hits_crits': {'2-7': {'hits': 1, 'crits': 0}, '8-15': {'hits': 1, 'crits': 1}, '16+': {'hits': 2, 'crits': 2}}, 'range': 8},
        }

        return roll_on_table(base_stats, item_level)


class Launcher(Guntype):
    name = 'Rocket Launcher'
    asset_dir = 'launcher'
    img_file = 'launcher.png'
    weapon_bonus = [trait_splash()]

    @staticmethod
    def get_basestats(item_level):
        base_stats = {
            (1, 6): {'hit_dice': Dice.from_string('1d12'), 'hits_crits': {'2-7': {'hits': 1, 'crits': 0}, '8-15': {'hits': 1, 'crits': 0}, '16+': {'hits': 1, 'crits': 1}}, 'range': 4},
            (7, 12): {'hit_dice': Dice.from_string('2d10'), 'hits_crits': {'2-7': {'hits': 1, 'crits': 0}, '8-15': {'hits': 1, 'crits': 0}, '16+': {'hits': 1, 'crits': 1}}, 'range': 4},
            (13, 18): {'hit_dice': Dice.from_string('1d12'), 'hits_crits': {'2-7': {'hits': 1, 'crits': 0}, '8-15': {'hits': 1, 'crits': 0}, '16+': {'hits': 1, 'crits': 2}}, 'range': 4},
            (19, 24): {'hit_dice': Dice.from_string('2d12'), 'hits_crits': {'2-7': {'hits': 1, 'crits': 0}, '8-15': {'hits': 1, 'crits': 0}, '16+': {'hits': 2, 'crits': 1}}, 'range': 4},
            (25, 30): {'hit_dice': Dice.from_string('1d20'), 'hits_crits': {'2-7': {'hits': 1, 'crits': 1}, '8-15': {'hits': 1, 'crits': 1}, '16+': {'hits': 2, 'crits': 1}}, 'range': 4},
        }

        return roll_on_table(base_stats, item_level)


class Guntypes:
    PISTOL = Pistol()
    SMG = Smg()
    RIFLE = Rifle()
    SHOTGUN = Shotgun()
    SNIPER = Sniper()
    LAUNCHER = Launcher()