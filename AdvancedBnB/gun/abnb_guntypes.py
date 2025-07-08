from .abnb_weapon_bonus import *
from util import Dice

class Guntype:
    name = ''
    asset_dir = ''

    def gun_part_exception(self, gun):
        return

    def __repr__(self):
        return f"{self.__class__.name}"

class Pistol(Guntype):
    name = 'Pistol'
    asset_dir = 'pistol'
    weapon_bonus = [BonusPistol()]

    @staticmethod
    def get_basestats(tier):
        table = {
            1: {'hit_dice': Dice.from_string('1d6'), 'crit_dice': Dice.from_string('1d8'), 'hits_crits': {'glance': {'hits': 1, 'crits': 0}, 'solid': {'hits': 2, 'crits': 0}, 'penetrate': {'hits': 3, 'crits': 1}}, 'range': 5, 'mag_size': 3},
            2: {'hit_dice': Dice.from_string('1d6'), 'crit_dice': Dice.from_string('1d8'), 'hits_crits': {'glance': {'hits': 2, 'crits': 0}, 'solid': {'hits': 2, 'crits': 0}, 'penetrate': {'hits': 4, 'crits': 1}}, 'range': 5, 'mag_size': 3},
            3: {'hit_dice': Dice.from_string('1d6'), 'crit_dice': Dice.from_string('1d8'), 'hits_crits': {'glance': {'hits': 2, 'crits': 0}, 'solid': {'hits': 2, 'crits': 1}, 'penetrate': {'hits': 3, 'crits': 2}}, 'range': 5, 'mag_size': 3},
            4: {'hit_dice': Dice.from_string('2d6'), 'crit_dice': Dice.from_string('2d8'), 'hits_crits': {'glance': {'hits': 1, 'crits': 0}, 'solid': {'hits': 1, 'crits': 1}, 'penetrate': {'hits': 2, 'crits': 1}}, 'range': 5, 'mag_size': 3},
            5: {'hit_dice': Dice.from_string('2d6'), 'crit_dice': Dice.from_string('2d8'), 'hits_crits': {'glance': {'hits': 1, 'crits': 0}, 'solid': {'hits': 2, 'crits': 1}, 'penetrate': {'hits': 3, 'crits': 1}}, 'range': 5, 'mag_size': 3},
            6: {'hit_dice': Dice.from_string('2d6'), 'crit_dice': Dice.from_string('2d8'), 'hits_crits': {'glance': {'hits': 2, 'crits': 0}, 'solid': {'hits': 2, 'crits': 1}, 'penetrate': {'hits': 2, 'crits': 2}}, 'range': 5, 'mag_size': 3},
            7: {'hit_dice': Dice.from_string('2d6'), 'crit_dice': Dice.from_string('2d8'), 'hits_crits': {'glance': {'hits': 2, 'crits': 0}, 'solid': {'hits': 3, 'crits': 1}, 'penetrate': {'hits': 3, 'crits': 2}}, 'range': 5, 'mag_size': 3},
            8: {'hit_dice': Dice.from_string('3d6'), 'crit_dice': Dice.from_string('3d8'), 'hits_crits': {'glance': {'hits': 2, 'crits': 0}, 'solid': {'hits': 2, 'crits': 1}, 'penetrate': {'hits': 3, 'crits': 1}}, 'range': 5, 'mag_size': 3},
            9: {'hit_dice': Dice.from_string('3d6'), 'crit_dice': Dice.from_string('3d8'), 'hits_crits': {'glance': {'hits': 2, 'crits': 0}, 'solid': {'hits': 2, 'crits': 1}, 'penetrate': {'hits': 3, 'crits': 2}}, 'range': 5, 'mag_size': 3},
            10: {'hit_dice': Dice.from_string('3d6'), 'crit_dice': Dice.from_string('3d8'), 'hits_crits': {'glance': {'hits': 3, 'crits': 0}, 'solid': {'hits': 2, 'crits': 1}, 'penetrate': {'hits': 2, 'crits': 3}}, 'range': 5, 'mag_size': 3},
        }

        return table[tier]

class Smg(Guntype):
    name = 'Submachine Gun'
    asset_dir = 'smg'
    weapon_bonus = [BonusSmg()]

    @staticmethod
    def get_basestats(tier):
        table = {
            1: {'hit_dice': Dice.from_string('2d4'), 'crit_dice': Dice.from_string('2d6'), 'hits_crits': {'glance': {'hits': 1, 'crits': 0}, 'solid': {'hits': 2, 'crits': 0}, 'penetrate': {'hits': 1, 'crits': 1}}, 'range': 5, 'mag_size': 4},
            2: {'hit_dice': Dice.from_string('2d4'), 'crit_dice': Dice.from_string('2d6'), 'hits_crits': {'glance': {'hits': 2, 'crits': 0}, 'solid': {'hits': 3, 'crits': 0}, 'penetrate': {'hits': 2, 'crits': 1}}, 'range': 5, 'mag_size': 4},
            3: {'hit_dice': Dice.from_string('2d4'), 'crit_dice': Dice.from_string('2d6'), 'hits_crits': {'glance': {'hits': 3, 'crits': 0}, 'solid': {'hits': 4, 'crits': 0}, 'penetrate': {'hits': 3, 'crits': 1}}, 'range': 5, 'mag_size': 4},
            4: {'hit_dice': Dice.from_string('3d4'), 'crit_dice': Dice.from_string('3d6'), 'hits_crits': {'glance': {'hits': 2, 'crits': 0}, 'solid': {'hits': 3, 'crits': 0}, 'penetrate': {'hits': 3, 'crits': 1}}, 'range': 5, 'mag_size': 4},
            5: {'hit_dice': Dice.from_string('3d4'), 'crit_dice': Dice.from_string('3d6'), 'hits_crits': {'glance': {'hits': 2, 'crits': 0}, 'solid': {'hits': 4, 'crits': 0}, 'penetrate': {'hits': 3, 'crits': 1}}, 'range': 5, 'mag_size': 4},
            6: {'hit_dice': Dice.from_string('3d4'), 'crit_dice': Dice.from_string('3d6'), 'hits_crits': {'glance': {'hits': 3, 'crits': 0}, 'solid': {'hits': 4, 'crits': 0}, 'penetrate': {'hits': 3, 'crits': 1}}, 'range': 5, 'mag_size': 4},
            7: {'hit_dice': Dice.from_string('3d4'), 'crit_dice': Dice.from_string('3d6'), 'hits_crits': {'glance': {'hits': 3, 'crits': 0}, 'solid': {'hits': 3, 'crits': 1}, 'penetrate': {'hits': 3, 'crits': 1}}, 'range': 5, 'mag_size': 4},
            8: {'hit_dice': Dice.from_string('4d4'), 'crit_dice': Dice.from_string('4d6'), 'hits_crits': {'glance': {'hits': 3, 'crits': 0}, 'solid': {'hits': 3, 'crits': 0}, 'penetrate': {'hits': 3, 'crits': 1}}, 'range': 5, 'mag_size': 4},
            9: {'hit_dice': Dice.from_string('4d4'), 'crit_dice': Dice.from_string('4d6'), 'hits_crits': {'glance': {'hits': 3, 'crits': 0}, 'solid': {'hits': 2, 'crits': 1}, 'penetrate': {'hits': 3, 'crits': 2}}, 'range': 5, 'mag_size': 4},
            10: {'hit_dice': Dice.from_string('4d4'), 'crit_dice': Dice.from_string('4d6'), 'hits_crits': {'glance': {'hits': 4, 'crits': 0}, 'solid': {'hits': 2, 'crits': 1}, 'penetrate': {'hits': 3, 'crits': 2}}, 'range': 5, 'mag_size': 4},
        }

        return table[tier]

class Rifle(Guntype):
    name = 'Combat Rifle'
    asset_dir = 'rifle'
    weapon_bonus = [BonusRifle()]

    @staticmethod
    def get_basestats(tier):
        table = {
            1: {'hit_dice': Dice.from_string('1d8'), 'crit_dice': Dice.from_string('1d10'), 'hits_crits': {'glance': {'hits': 1, 'crits': 0}, 'solid': {'hits': 3, 'crits': 0}, 'penetrate': {'hits': 3, 'crits': 1}}, 'range': 6, 'mag_size': 5},
            2: {'hit_dice': Dice.from_string('1d8'), 'crit_dice': Dice.from_string('1d10'), 'hits_crits': {'glance': {'hits': 2, 'crits': 0}, 'solid': {'hits': 3, 'crits': 0}, 'penetrate': {'hits': 3, 'crits': 1}}, 'range': 6, 'mag_size': 5},
            3: {'hit_dice': Dice.from_string('1d8'), 'crit_dice': Dice.from_string('1d10'), 'hits_crits': {'glance': {'hits': 1, 'crits': 1}, 'solid': {'hits': 3, 'crits': 1}, 'penetrate': {'hits': 2, 'crits': 2}}, 'range': 6, 'mag_size': 5},
            4: {'hit_dice': Dice.from_string('1d8'), 'crit_dice': Dice.from_string('1d10'), 'hits_crits': {'glance': {'hits': 2, 'crits': 1}, 'solid': {'hits': 3, 'crits': 1}, 'penetrate': {'hits': 3, 'crits': 2}}, 'range': 6, 'mag_size': 5},
            5: {'hit_dice': Dice.from_string('1d8'), 'crit_dice': Dice.from_string('1d10'), 'hits_crits': {'glance': {'hits': 2, 'crits': 1}, 'solid': {'hits': 3, 'crits': 1}, 'penetrate': {'hits': 3, 'crits': 2}}, 'range': 6, 'mag_size': 5},
            6: {'hit_dice': Dice.from_string('2d8'), 'crit_dice': Dice.from_string('2d10'), 'hits_crits': {'glance': {'hits': 1, 'crits': 0}, 'solid': {'hits': 2, 'crits': 1}, 'penetrate': {'hits': 2, 'crits': 1}}, 'range': 6, 'mag_size': 5},
            7: {'hit_dice': Dice.from_string('2d8'), 'crit_dice': Dice.from_string('2d10'), 'hits_crits': {'glance': {'hits': 1, 'crits': 1}, 'solid': {'hits': 2, 'crits': 1}, 'penetrate': {'hits': 3, 'crits': 1}}, 'range': 6, 'mag_size': 5},
            8: {'hit_dice': Dice.from_string('2d8'), 'crit_dice': Dice.from_string('2d10'), 'hits_crits': {'glance': {'hits': 1, 'crits': 1}, 'solid': {'hits': 3, 'crits': 1}, 'penetrate': {'hits': 2, 'crits': 2}}, 'range': 6, 'mag_size': 5},
            9: {'hit_dice': Dice.from_string('2d8'), 'crit_dice': Dice.from_string('2d10'), 'hits_crits': {'glance': {'hits': 2, 'crits': 1}, 'solid': {'hits': 3, 'crits': 1}, 'penetrate': {'hits': 3, 'crits': 2}}, 'range': 6, 'mag_size': 5},
            10: {'hit_dice': Dice.from_string('2d8'), 'crit_dice': Dice.from_string('2d10'), 'hits_crits': {'glance': {'hits': 2, 'crits': 1}, 'solid': {'hits': 3, 'crits': 1}, 'penetrate': {'hits': 3, 'crits': 3}}, 'range': 6, 'mag_size': 5},
        }

        return table[tier]

    def gun_part_exception(self, gun):
        # Combat Rifle Spawns with one accessory. This does NOT count towards number of Gun Parts.
        if gun.gun_type == self:
            part = gun.pick_weapon_accessory()
            gun.parts.append(part)

class Shotgun(Guntype):
    name = 'Shotgun'
    asset_dir = 'shotgun'
    weapon_bonus = [BonusShotgun()]

    @staticmethod
    def get_basestats(tier):
        table = {
            1: {'hit_dice': Dice.from_string('1d8'), 'crit_dice': Dice.from_string('1d10'), 'hits_crits': {'glance': {'hits': 1, 'crits': 0}, 'solid': {'hits': 2, 'crits': 0}, 'penetrate': {'hits': 1, 'crits': 1}}, 'range': 4, 'mag_size': 3},
            2: {'hit_dice': Dice.from_string('1d8'), 'crit_dice': Dice.from_string('1d10'), 'hits_crits': {'glance': {'hits': 1, 'crits': 0}, 'solid': {'hits': 3, 'crits': 0}, 'penetrate': {'hits': 3, 'crits': 1}}, 'range': 4, 'mag_size': 3},
            3: {'hit_dice': Dice.from_string('1d8'), 'crit_dice': Dice.from_string('1d10'), 'hits_crits': {'glance': {'hits': 2, 'crits': 0}, 'solid': {'hits': 2, 'crits': 1}, 'penetrate': {'hits': 4, 'crits': 1}}, 'range': 4, 'mag_size': 3},
            4: {'hit_dice': Dice.from_string('1d8'), 'crit_dice': Dice.from_string('1d10'), 'hits_crits': {'glance': {'hits': 3, 'crits': 0}, 'solid': {'hits': 3, 'crits': 1}, 'penetrate': {'hits': 4, 'crits': 1}}, 'range': 4, 'mag_size': 3},
            5: {'hit_dice': Dice.from_string('1d8'), 'crit_dice': Dice.from_string('1d10'), 'hits_crits': {'glance': {'hits': 3, 'crits': 0}, 'solid': {'hits': 3, 'crits': 1}, 'penetrate': {'hits': 4, 'crits': 2}}, 'range': 4, 'mag_size': 3},
            6: {'hit_dice': Dice.from_string('1d8'), 'crit_dice': Dice.from_string('1d10'), 'hits_crits': {'glance': {'hits': 3, 'crits': 0}, 'solid': {'hits': 4, 'crits': 1}, 'penetrate': {'hits': 4, 'crits': 2}}, 'range': 4, 'mag_size': 3},
            7: {'hit_dice': Dice.from_string('2d8'), 'crit_dice': Dice.from_string('2d10'), 'hits_crits': {'glance': {'hits': 2, 'crits': 0}, 'solid': {'hits': 2, 'crits': 0}, 'penetrate': {'hits': 3, 'crits': 1}}, 'range': 4, 'mag_size': 3},
            8: {'hit_dice': Dice.from_string('2d8'), 'crit_dice': Dice.from_string('2d10'), 'hits_crits': {'glance': {'hits': 2, 'crits': 0}, 'solid': {'hits': 2, 'crits': 0}, 'penetrate': {'hits': 3, 'crits': 2}}, 'range': 4, 'mag_size': 3},
            9: {'hit_dice': Dice.from_string('2d8'), 'crit_dice': Dice.from_string('2d10'), 'hits_crits': {'glance': {'hits': 2, 'crits': 0}, 'solid': {'hits': 3, 'crits': 0}, 'penetrate': {'hits': 3, 'crits': 2}}, 'range': 4, 'mag_size': 3},
            10: {'hit_dice': Dice.from_string('2d8'), 'crit_dice': Dice.from_string('2d10'), 'hits_crits': {'glance': {'hits': 2, 'crits': 0}, 'solid': {'hits': 2, 'crits': 1}, 'penetrate': {'hits': 3, 'crits': 2}}, 'range': 4, 'mag_size': 3},
        }

        return table[tier]

class Sniper(Guntype):
    name = 'Sniper Rifle'
    asset_dir = 'sniper'
    weapon_bonus = [BonusSniper_scope(), BonusSniper_accuracy()]

    def gun_part_exception(self, gun):
        # Sniper Rifle spawns with a Scope. This DOES count towards the maximum equipped number of parts
        if gun.gun_type == self:
            part = gun.pick_weapon_scope()
            gun.parts.append(part)
            gun.n_scopes += 1
            gun.n_parts += 1

    @staticmethod
    def get_basestats(tier):
        table = {
            1: {'hit_dice': Dice.from_string('1d12'), 'crit_dice': Dice.from_string('1d20'), 'hits_crits': {'glance': {'hits': 0, 'crits': 0}, 'solid': {'hits': 1, 'crits': 0}, 'penetrate': {'hits': 0, 'crits': 1}}, 'range': 8, 'mag_size': 2},
            2: {'hit_dice': Dice.from_string('1d12'), 'crit_dice': Dice.from_string('1d20'), 'hits_crits': {'glance': {'hits': 0, 'crits': 0}, 'solid': {'hits': 1, 'crits': 0}, 'penetrate': {'hits': 1, 'crits': 1}}, 'range': 8, 'mag_size': 2},
            3: {'hit_dice': Dice.from_string('1d12'), 'crit_dice': Dice.from_string('1d20'), 'hits_crits': {'glance': {'hits': 0, 'crits': 0}, 'solid': {'hits': 1, 'crits': 0}, 'penetrate': {'hits': 0, 'crits': 2}}, 'range': 8, 'mag_size': 2},
            4: {'hit_dice': Dice.from_string('1d12'), 'crit_dice': Dice.from_string('1d20'), 'hits_crits': {'glance': {'hits': 0, 'crits': 0}, 'solid': {'hits': 1, 'crits': 0}, 'penetrate': {'hits': 1, 'crits': 2}}, 'range': 8, 'mag_size': 2},
            5: {'hit_dice': Dice.from_string('2d12'), 'crit_dice': Dice.from_string('2d20'), 'hits_crits': {'glance': {'hits': 0, 'crits': 0}, 'solid': {'hits': 1, 'crits': 0}, 'penetrate': {'hits': 1, 'crits': 1}}, 'range': 8, 'mag_size': 2},
            6: {'hit_dice': Dice.from_string('2d12'), 'crit_dice': Dice.from_string('2d20'), 'hits_crits': {'glance': {'hits': 0, 'crits': 0}, 'solid': {'hits': 1, 'crits': 0}, 'penetrate': {'hits': 0, 'crits': 2}}, 'range': 8, 'mag_size': 2},
            7: {'hit_dice': Dice.from_string('2d12'), 'crit_dice': Dice.from_string('2d20'), 'hits_crits': {'glance': {'hits': 0, 'crits': 0}, 'solid': {'hits': 1, 'crits': 0}, 'penetrate': {'hits': 1, 'crits': 2}}, 'range': 8, 'mag_size': 2},
            8: {'hit_dice': Dice.from_string('2d12'), 'crit_dice': Dice.from_string('2d20'), 'hits_crits': {'glance': {'hits': 0, 'crits': 0}, 'solid': {'hits': 2, 'crits': 0}, 'penetrate': {'hits': 1, 'crits': 2}}, 'range': 8, 'mag_size': 2},
            9: {'hit_dice': Dice.from_string('2d12'), 'crit_dice': Dice.from_string('2d20'), 'hits_crits': {'glance': {'hits': 0, 'crits': 0}, 'solid': {'hits': 2, 'crits': 0}, 'penetrate': {'hits': 2, 'crits': 2}}, 'range': 8, 'mag_size': 2},
            10: {'hit_dice': Dice.from_string('2d12'), 'crit_dice': Dice.from_string('2d20'), 'hits_crits': {'glance': {'hits': 0, 'crits': 0}, 'solid': {'hits': 2, 'crits': 0}, 'penetrate': {'hits': 1, 'crits': 3}}, 'range': 8, 'mag_size': 2},
        }

        return table[tier]

class Launcher(Guntype):
    name = 'Rocket Launcher'
    asset_dir = 'launcher'
    weapon_bonus = [BonusLauncher()]

    @staticmethod
    def get_basestats(tier):
        table = {
            1: {'hit_dice': Dice.from_string('1d10'), 'crit_dice': Dice.from_string('1d12'), 'hits_crits' : {'glance': {'hits': 1, 'crits': 0}, 'solid': {'hits': 1, 'crits': 0}, 'penetrate': {'hits': 1, 'crits': 1}}, 'range': 4, 'mag_size': 1},
            2: {'hit_dice': Dice.from_string('1d10'), 'crit_dice': Dice.from_string('1d12'), 'hits_crits': {'glance': {'hits': 1, 'crits': 0}, 'solid': {'hits': 2, 'crits': 0}, 'penetrate': {'hits': 2, 'crits': 1}}, 'range': 4, 'mag_size': 1},
            3: {'hit_dice': Dice.from_string('1d10'), 'crit_dice': Dice.from_string('1d12'), 'hits_crits': {'glance': {'hits': 1, 'crits': 0}, 'solid': {'hits': 2, 'crits': 0}, 'penetrate': {'hits': 3, 'crits': 1}}, 'range': 4, 'mag_size': 1},
            4: {'hit_dice': Dice.from_string('2d10'), 'crit_dice': Dice.from_string('2d12'), 'hits_crits': {'glance': {'hits': 1, 'crits': 0}, 'solid': {'hits': 1, 'crits': 0}, 'penetrate': {'hits': 1, 'crits': 1}}, 'range': 4, 'mag_size': 1},
            5: {'hit_dice': Dice.from_string('2d10'), 'crit_dice': Dice.from_string('2d12'), 'hits_crits': {'glance': {'hits': 1, 'crits': 0}, 'solid': {'hits': 1, 'crits': 0}, 'penetrate': {'hits': 2, 'crits': 1}}, 'range': 4, 'mag_size': 1},
            6: {'hit_dice': Dice.from_string('2d10'), 'crit_dice': Dice.from_string('2d12'), 'hits_crits': {'glance': {'hits': 1, 'crits': 0}, 'solid': {'hits': 2, 'crits': 0}, 'penetrate': {'hits': 2, 'crits': 1}}, 'range': 4, 'mag_size': 1},
            7: {'hit_dice': Dice.from_string('2d10'), 'crit_dice': Dice.from_string('2d12'), 'hits_crits': {'glance': {'hits': 2, 'crits': 0}, 'solid': {'hits': 2, 'crits': 0}, 'penetrate': {'hits': 2, 'crits': 1}}, 'range': 4, 'mag_size': 1},
            8: {'hit_dice': Dice.from_string('2d10'), 'crit_dice': Dice.from_string('2d12'), 'hits_crits': {'glance': {'hits': 2, 'crits': 0}, 'solid': {'hits': 3, 'crits': 0}, 'penetrate': {'hits': 2, 'crits': 1}}, 'range': 4, 'mag_size': 1},
            9: {'hit_dice': Dice.from_string('2d10'), 'crit_dice': Dice.from_string('2d12'), 'hits_crits': {'glance': {'hits': 2, 'crits': 0}, 'solid': {'hits': 3, 'crits': 0}, 'penetrate': {'hits': 3, 'crits': 1}}, 'range': 4, 'mag_size': 1},
            10: {'hit_dice': Dice.from_string('3d10'), 'crit_dice': Dice.from_string('3d12'), 'hits_crits': {'glance': {'hits': 2, 'crits': 0}, 'solid': {'hits': 2, 'crits': 0}, 'penetrate': {'hits': 2, 'crits': 1}}, 'range': 4, 'mag_size': 1},
        }

        return table[tier]

class Guntypes:
    PISTOL = Pistol()
    SMG = Smg()
    RIFLE = Rifle()
    SHOTGUN = Shotgun()
    SNIPER = Sniper()
    LAUNCHER = Launcher()