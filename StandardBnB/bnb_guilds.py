from copy import deepcopy

from .bnb_guntypes import Guntypes
from .bnb_weapon_bonus import *
from.bnb_shield_effects import *
from util import Rarity
from util import Dice, roll_on_table


class Guild:
    name = ''
    logo_file = ''
    weapon_bonus = []

    def apply_weapon_bonus(self, gun):
        return

    def __repr__(self):
        return f"{self.__class__.name}"

class Ashen(Guild):
    name = 'Ashen'
    logo_file = 'Anshin.png'

    def make_shield(self, shield):
        shield_table = {
            (1, 6):     {'capacity': 30, 'charge_rate': 15, 'effect': effect_ashen_fast_recharge()},
            (7, 12):    {'capacity': 55, 'charge_rate': 20, 'effect': effect_ashen_fast_recharge()},
            (13, 18):   {'capacity': 70, 'charge_rate': 25, 'effect': effect_ashen_fast_recharge()},
            (19, 24):   {'capacity': 70, 'charge_rate': 15, 'effect': effect_ashen_shield_effect()},
            (25, 30):   {'capacity': 60, 'charge_rate': 10, 'effect': effect_ashen_shield_effect_2()}
        }

        table_result = roll_on_table(shield_table, shield.level)

        shield.base_stats['capacity'] = table_result['capacity']
        shield.base_stats['charge_rate'] = table_result['charge_rate']
        shield.mod_stats = deepcopy(shield.base_stats)

        shield.effects.append(table_result['effect'])


class Alas(Guild):
    name = 'Alas'
    logo_file = 'Alas.png'
    weapon_bonus = []

    def __init__(self):
        self.makes = {
            'weapons': [Guntypes.RIFLE, Guntypes.PISTOL, Guntypes.SHOTGUN, Guntypes.SNIPER],
            'grenades': [],
            'shields': [],
            'relics': []
        }

    def apply_weapon_bonus(self, gun):
        # Increased Damage (based on Rarity)
        # Guns are NEVER Elemental
        bonus_table = {
            Rarity.COMMON:     {'dmg_mod': 1},
            Rarity.UNCOMMON:   {'dmg_mod': 2},
            Rarity.RARE:       {'dmg_mod': 3},
            Rarity.EPIC:       {'dmg_mod': 3},
            Rarity.LEGENDARY:  {'dmg_mod': 4},
        }

        bonus = bonus_table[gun.rarity]
        for k, v in bonus.items():
            gun.mod_stats.setdefault('mods', {}).setdefault(k, 0)
            gun.mod_stats['mods'][k] += v

        gun.forced_non_elemental = True

    def make_shield(self, shield):
        shield_table = {
            (1, 6):     {'capacity': 30, 'charge_rate': 10, 'effect': effect_alas_shield_effect()},
            (7, 12):    {'capacity': 55, 'charge_rate': 20, 'effect': effect_alas_shield_effect()},
            (13, 18):   {'capacity': 70, 'charge_rate': 20, 'effect': effect_alas_shield_effect()},
            (19, 24):   {'capacity': 60, 'charge_rate': 10, 'effect': effect_alas_shield_effect_2()},
            (25, 30):   {'capacity': 0, 'charge_rate': 0, 'effect': effect_alas_shield_effect_2()}
        }

        table_result = roll_on_table(shield_table, shield.level)

        shield.base_stats['capacity'] = table_result['capacity']
        shield.base_stats['charge_rate'] = table_result['charge_rate']
        shield.mod_stats = deepcopy(shield.base_stats)

        shield.effects.append(table_result['effect'])


class Skulldugger(Guild):
    name = 'Skulldugger'
    logo_file = 'Skulldugger.png'
    weapon_bonus = []

    def __init__(self):
        self.makes = {
            'weapons': [Guntypes.PISTOL, Guntypes.SMG, Guntypes.SHOTGUN, Guntypes.SNIPER],
            'grenades': [],
            'shields': [],
            'relics': []
        }

    def apply_weapon_bonus(self, gun):
        # Increased Damage + Overheat (based on Rarity)
        bonus_table = {
            Rarity.COMMON:     {'dmg_mod': 2, 'overheat': Dice.from_string('1d4')},
            Rarity.UNCOMMON:   {'dmg_mod': 3, 'overheat': Dice.from_string('1d6')},
            Rarity.RARE:       {'dmg_mod': 4, 'overheat': Dice.from_string('1d8')},
            Rarity.EPIC:       {'dmg_mod': 5, 'overheat': Dice.from_string('1d10')},
            Rarity.LEGENDARY:  {'dmg_mod': 6, 'overheat': Dice.from_string('1d12')},
        }

        bonus = bonus_table[gun.rarity]
        gun.mod_stats.setdefault('mods', {}).setdefault('dmg_mod', 0)
        gun.mod_stats['mods']['dmg_mod'] += bonus['dmg_mod']

        gun.effects.append(trait_overheat())


class Dahlia(Guild):
    name = 'Dahlia'
    logo_file = 'Dahlia.png'
    weapon_bonus = []

    def __init__(self):
        self.makes = {
            'weapons': [Guntypes.RIFLE, Guntypes.PISTOL, Guntypes.SMG, Guntypes.SHOTGUN, Guntypes.SNIPER],
            'grenades': [],
            'shields': [],
            'relics': []
        }

    def apply_weapon_bonus(self, gun):
        # Burst +1, + ACC MOD (based on Rarity)
        bonus_table = {
            Rarity.COMMON: {},
            Rarity.UNCOMMON: {'acc_mod': 1},
            Rarity.RARE: {'acc_mod': 2},
            Rarity.EPIC: {'acc_mod': 3},
            Rarity.LEGENDARY: {'acc_mod': 4},
        }

        bonus = bonus_table[gun.rarity]
        if 'acc_mod' in bonus:
            gun.mod_stats.setdefault('mods', {}).setdefault('acc_mod', 0)
            gun.mod_stats['mods']['acc_mod'] += bonus['acc_mod']

        for atk in ['2-7', '8-15', '16+']:
            gun.mod_stats['hits_crits'][atk]['hits'] += 1

    def make_shield(self, shield):
        shield_table = {
            (1, 6):     {'capacity': 30, 'charge_rate': 10, 'effect': effect_dahlia_shield_effect()},
            (7, 12):    {'capacity': 55, 'charge_rate': 15, 'effect': effect_dahlia_shield_effect()},
            (13, 18):   {'capacity': 75, 'charge_rate': 20, 'effect': effect_dahlia_shield_effect()},
            (19, 24):   {'capacity': 80, 'charge_rate': 10, 'effect': effect_dahlia_shield_effect_2()},
            (25, 30):   {'capacity': 80, 'charge_rate': 15, 'effect': effect_dahlia_shield_effect_2()}
        }

        table_result = roll_on_table(shield_table, shield.level)

        shield.base_stats['capacity'] = table_result['capacity']
        shield.base_stats['charge_rate'] = table_result['charge_rate']
        shield.mod_stats = deepcopy(shield.base_stats)

        shield.effects.append(table_result['effect'])


class Blackpowder(Guild):
    name = 'Blackpowder'
    logo_file = 'Blackpowder.png'
    weapon_bonus = []

    def __init__(self):
        self.makes = {
            'weapons': [Guntypes.PISTOL, Guntypes.SHOTGUN, Guntypes.SNIPER],
            'grenades': [],
            'shields': [],
            'relics': []
        }

    def apply_weapon_bonus(self, gun):
        # +2 ACC MOD, + Crit DMG (based on Rarity)
        # Guns are NEVER Elemental
        bonus_table = {
            Rarity.COMMON: {'acc_mod': 2, 'crit_dmg': 2},
            Rarity.UNCOMMON: {'acc_mod': 2, 'crit_dmg': 3},
            Rarity.RARE: {'acc_mod': 2, 'crit_dmg': 4},
            Rarity.EPIC: {'acc_mod': 2, 'crit_dmg': 5},
            Rarity.LEGENDARY: {'acc_mod': 2, 'crit_dmg': 6},
        }

        bonus = bonus_table[gun.rarity]
        for k, v in bonus.items():
            gun.mod_stats.setdefault('mods', {}).setdefault(k, 0)
            gun.mod_stats['mods'][k] += v

        gun.forced_non_elemental = True


class Malefactor(Guild):
    name = 'Malefactor'
    logo_file = 'Malefactor.png'
    weapon_bonus = []

    def __init__(self):
        self.makes = {
            'weapons': [Guntypes.PISTOL, Guntypes.SMG, Guntypes.SHOTGUN, Guntypes.SNIPER, Guntypes.LAUNCHER],
            'grenades': [],
            'shields': [],
            'relics': []
        }

    def apply_weapon_bonus(self, gun):
        # Elemental Roll Bonus, DMG MOD (base on Rarity)
        # Guns are ALWAYS Elemental
        bonus_table = {
            Rarity.COMMON: {'dmg_mod': -2},
            Rarity.UNCOMMON: {'dmg_mod': -1},
            Rarity.RARE: {'roll_bonus': 10},
            Rarity.EPIC: {'roll_bonus': 15},
            Rarity.LEGENDARY: {'roll_bonus': 20},
        }

        bonus = bonus_table[gun.rarity]
        if 'dmg_mod' in bonus:
            gun.mod_stats.setdefault('mods', {}).setdefault('dmg_mod', 0)
            gun.mod_stats['mods']['dmg_mod'] += bonus['dmg_mod']

        if 'roll_bonus' in bonus:
            gun.element_roll_bonus += bonus['roll_bonus']

        gun.forced_elemental = True

    def make_shield(self, shield):
        shield_table = {
            (1, 6):     {'capacity': 30, 'charge_rate': 10, 'effect': effect_malefactor_shield_effect()},
            (7, 12):    {'capacity': 50, 'charge_rate': 15, 'effect': effect_malefactor_shield_effect()},
            (13, 18):   {'capacity': 70, 'charge_rate': 20, 'effect': effect_malefactor_shield_effect()},
            (19, 24):   {'capacity': 70, 'charge_rate': 15, 'effect': effect_malefactor_shield_effect_2()},
            (25, 30):   {'capacity': 80, 'charge_rate': 15, 'effect': effect_malefactor_shield_effect_2()}
        }

        table_result = roll_on_table(shield_table, shield.level)

        shield.base_stats['capacity'] = table_result['capacity']
        shield.base_stats['charge_rate'] = table_result['charge_rate']
        shield.mod_stats = deepcopy(shield.base_stats)

        shield.effects.append(table_result['effect'])


class Hyperius(Guild):
    name = 'Hyperius'
    logo_file = 'Hyperius.png'
    weapon_bonus = []

    def __init__(self):
        self.makes = {
            'weapons': [Guntypes.RIFLE, Guntypes.PISTOL, Guntypes.SMG, Guntypes.SHOTGUN, Guntypes.SNIPER, Guntypes.LAUNCHER],
            'grenades': [],
            'shields': [],
            'relics': []
        }

    def apply_weapon_bonus(self, gun):
        # + ACC MOD, - DMG MOD (based on Rarity)
        bonus_table = {
            Rarity.COMMON: {'acc_mod': 1, 'dmg_mod': -2},
            Rarity.UNCOMMON: {'acc_mod': 2, 'dmg_mod': -2},
            Rarity.RARE: {'acc_mod': 3, 'dmg_mod': -2},
            Rarity.EPIC: {'acc_mod': 4, 'dmg_mod': -2},
            Rarity.LEGENDARY: {'acc_mod': 5, 'dmg_mod': -2},
        }

        bonus = bonus_table[gun.rarity]
        for k, v in bonus.items():
            gun.mod_stats.setdefault('mods', {}).setdefault(k, 0)
            gun.mod_stats['mods'][k] += v


class Feriore(Guild):
    name = 'Feriore'
    logo_file = 'Feriore.png'
    weapon_bonus = []

    def __init__(self):
        self.makes = {
            'weapons': [Guntypes.RIFLE, Guntypes.PISTOL, Guntypes.SMG, Guntypes.SHOTGUN],
            'grenades': [],
            'shields': [],
            'relics': []
        }

    def apply_weapon_bonus(self, gun):
        # On Reload/Swap: The Gun is Thrown like a Grenade, dealing DMG. - ACC MOD (Based on Rarity)
        bonus_table = {
            Rarity.COMMON: {'acc_mod': -3},
            Rarity.UNCOMMON: {'acc_mod': -3},
            Rarity.RARE: {'acc_mod': -2},
            Rarity.EPIC: {'acc_mod': -2},
            Rarity.LEGENDARY: {'acc_mod': -1},
        }

        bonus = bonus_table[gun.rarity]
        gun.mod_stats.setdefault('mods', {}).setdefault('acc_mod', 0)
        gun.mod_stats['mods']['acc_mod'] += bonus['acc_mod']

        gun.effects.append(trait_swap_reload())

    def make_shield(self, shield):
        shield_table = {
            (1, 6):     {'capacity': 30, 'charge_rate': 10, 'effect': effect_feriore_shield_effect()},
            (7, 12):    {'capacity': 50, 'charge_rate': 15, 'effect': effect_feriore_shield_effect()},
            (13, 18):   {'capacity': 70, 'charge_rate': 20, 'effect': effect_feriore_shield_effect()},
            (19, 24):   {'capacity': 70, 'charge_rate': 20, 'effect': effect_feriore_shield_effect_2()},
            (25, 30):   {'capacity': 60, 'charge_rate': 20, 'effect': effect_feriore_shield_effect_2()}
        }

        table_result = roll_on_table(shield_table, shield.level)

        shield.base_stats['capacity'] = table_result['capacity']
        shield.base_stats['charge_rate'] = table_result['charge_rate']
        shield.mod_stats = deepcopy(shield.base_stats)

        shield.effects.append(table_result['effect'])


class Torgue(Guild):
    name = 'Torgue'
    logo_file = 'Torgue.png'
    weapon_bonus = []

    def __init__(self):
        self.makes = {
            'weapons': [Guntypes.RIFLE, Guntypes.PISTOL, Guntypes.SMG, Guntypes.SHOTGUN, Guntypes.SNIPER, Guntypes.LAUNCHER],
            'grenades': [],
            'shields': [],
            'relics': []
        }

    def apply_weapon_bonus(self, gun):
        # Splash. - ACC MOD (Based on Rarity)
        bonus_table = {
            Rarity.COMMON: {'acc_mod': -4},
            Rarity.UNCOMMON: {'acc_mod': -3},
            Rarity.RARE: {'acc_mod': -2},
            Rarity.EPIC: {'acc_mod': -1},
            Rarity.LEGENDARY: {'acc_mod': 0},
        }

        bonus = bonus_table[gun.rarity]
        gun.mod_stats.setdefault('mods', {}).setdefault('acc_mod', 0)
        gun.mod_stats['mods']['acc_mod'] += bonus['acc_mod']

        if trait_splash not in [type(ef) for ef in gun.effects]:
            gun.effects.append(trait_splash())

    def make_shield(self, shield):
        shield_table = {
            (1, 6):     {'capacity': 30, 'charge_rate': 10, 'effect': effect_torgue_shield_effect()},
            (7, 12):    {'capacity': 50, 'charge_rate': 15, 'effect': effect_torgue_shield_effect()},
            (13, 18):   {'capacity': 70, 'charge_rate': 20, 'effect': effect_torgue_shield_effect()},
            (19, 24):   {'capacity': 75, 'charge_rate': 15, 'effect': effect_torgue_shield_effect_2()},
            (25, 30):   {'capacity': 80, 'charge_rate': 15, 'effect': effect_torgue_shield_effect_2()}
        }

        table_result = roll_on_table(shield_table, shield.level)

        shield.base_stats['capacity'] = table_result['capacity']
        shield.base_stats['charge_rate'] = table_result['charge_rate']
        shield.mod_stats = deepcopy(shield.base_stats)

        shield.effects.append(table_result['effect'])


class Stoker(Guild):
    name = 'Stoker'
    logo_file = 'Stoker.png'
    weapon_bonus = []

    def __init__(self):
        self.makes = {
            'weapons': [Guntypes.RIFLE, Guntypes.PISTOL, Guntypes.SHOTGUN, Guntypes.SNIPER, Guntypes.LAUNCHER],
            'grenades': [],
            'shields': [],
            'relics': []
        }

    def apply_weapon_bonus(self, gun):
        # Extra Attack, - ACC MOD, Extra Movement (Based on Rarity)
        bonus_table = {
            Rarity.COMMON: {'acc_mod': -3},
            Rarity.UNCOMMON: {'acc_mod': -2},
            Rarity.RARE: {'acc_mod': -1},
            Rarity.EPIC: {},
            Rarity.LEGENDARY: {'extra_movement': True},
        }

        bonus = bonus_table[gun.rarity]
        if 'acc_mod' in bonus:
            gun.mod_stats.setdefault('mods', {}).setdefault('acc_mod', 0)
            gun.mod_stats['mods']['acc_mod'] += bonus['acc_mod']

        if 'extra_movement' in bonus:
            gun.effects.append(trait_extra_movement())

        gun.effects.append(trait_extra_attack())

    def make_shield(self, shield):
        shield_table = {
            (1, 6):     {'capacity': 30, 'charge_rate': 10, 'effect': effect_stoker_shield_effect()},
            (7, 12):    {'capacity': 50, 'charge_rate': 15, 'effect': effect_stoker_shield_effect()},
            (13, 18):   {'capacity': 70, 'charge_rate': 20, 'effect': effect_stoker_shield_effect()},
            (19, 24):   {'capacity': 70, 'charge_rate': 15, 'effect': effect_stoker_shield_effect_2()},
            (25, 30):   {'capacity': 80, 'charge_rate': 15, 'effect': effect_stoker_shield_effect_2()}
        }

        table_result = roll_on_table(shield_table, shield.level)

        shield.base_stats['capacity'] = table_result['capacity']
        shield.base_stats['charge_rate'] = table_result['charge_rate']
        shield.mod_stats = deepcopy(shield.base_stats)

        shield.effects.append(table_result['effect'])


class Pangoblin(Guild):
    name = 'Pangoblin'
    logo_file = 'Pangoblin.png'
    weapon_bonus = []

    def __init__(self):
        self.makes = {
            'weapons': [],
            'grenades': [],
            'shields': [],
            'relics': []
        }

    def make_shield(self, shield):
        shield_table = {
            (1, 6):     {'capacity': 40, 'charge_rate': 5, 'effect': effect_pangoblin_shield_effect()},
            (7, 12):    {'capacity': 60, 'charge_rate': 10, 'effect': effect_pangoblin_shield_effect()},
            (13, 18):   {'capacity': 80, 'charge_rate': 20, 'effect': effect_pangoblin_shield_effect()},
            (19, 24):   {'capacity': 100, 'charge_rate': 20, 'effect': effect_pangoblin_shield_effect_2()},
            (25, 30):   {'capacity': 60, 'charge_rate': 10, 'effect': effect_pangoblin_shield_effect_2()}
        }

        table_result = roll_on_table(shield_table, shield.level)

        shield.base_stats['capacity'] = table_result['capacity']
        shield.base_stats['charge_rate'] = table_result['charge_rate']
        shield.mod_stats = deepcopy(shield.base_stats)

        shield.effects.append(table_result['effect'])




class Guilds:
    ASHEN = Ashen()
    ALAS = Alas()
    SKULLDUGGER = Skulldugger()
    DAHLIA = Dahlia()
    BLACKPOWDER = Blackpowder()
    MALEFACTOR = Malefactor()
    HYPERIUS = Hyperius()
    FERIORE = Feriore()
    TORGUE = Torgue()
    STOKER = Stoker()
    PANGOBLIN = Pangoblin()

