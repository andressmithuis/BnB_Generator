from AdvancedBnB.abnb_guntypes import *
from util import Modifier

# Weapon Parts
class wp_part_empty(Modifier):
    name = 'Trinket'
    effect = 'Looks cool. Does Nothing.'

class wp_part_matching_barrel(Modifier):
    name = 'Matching Barrel'
    effect = '+2 on DMG Rolls.'

    def apply(self, gun):
        gun.mod_stats.setdefault('mods', {}).setdefault('dmg_mod', 0)
        gun.mod_stats['mods']['dmg_mod'] += 2

class wp_part_matching_grip(Modifier):
    name = 'Matching Grip'
    effect = '+1 on Reload and Swap Checks.'

    def apply(self, gun):
        gun.mod_stats.setdefault('mods', {}).setdefault('reload_check', 0)
        gun.mod_stats.setdefault('mods', {}).setdefault('swap_check', 0)
        gun.mod_stats['mods']['reload_check'] += 1
        gun.mod_stats['mods']['swap_check'] += 1

class wp_part_matching_stock(Modifier):
    name = 'Matching Stock'
    effect = '+1 on Accuracy Rolls.'

    def apply(self, gun):
        gun.mod_stats.setdefault('mods', {}).setdefault('acc_mod', 0)
        gun.mod_stats['mods']['acc_mod'] += 1

# Weapon Sights
class wp_part_iron_sight(Modifier):
    name = '(Scope) Iron Sight'
    effect = 'While ADS: +1 Range and +1 Minimum ADS Range.'
    situational = True
    weapon_types = [Guntypes.RIFLE, Guntypes.PISTOL, Guntypes.LAUNCHER, Guntypes.SHOTGUN, Guntypes.SMG]

    def apply(self, gun):
        gun.mod_stats.setdefault('mods', {}).setdefault('min_ads_range', 0)
        gun.mod_stats['mods']['min_ads_range'] += 1

    def to_text(self, gun):
        return 'While ADS: +1 Range.'

class wp_part_reflex_sight(Modifier):
    name = '(Scope) Reflex Sight'
    effect = 'While ADS: +2 Range and +1 Minimum ADS Range.'
    situational = True
    weapon_types = [Guntypes.RIFLE, Guntypes.PISTOL, Guntypes.LAUNCHER, Guntypes.SHOTGUN, Guntypes.SMG]

    def apply(self, gun):
        gun.mod_stats.setdefault('mods', {}).setdefault('min_ads_range', 0)
        gun.mod_stats['mods']['min_ads_range'] += 1

    def to_text(self, gun):
        return 'While ADS: +2 Range.'

class wp_part_acog(Modifier):
    name = '(Scope) ACOG'
    effect = 'While ADS: +3 Range and +2 Minimum ADS Range.'
    situational = True
    weapon_types = [Guntypes.RIFLE, Guntypes.LAUNCHER, Guntypes.SNIPER]

    def apply(self, gun):
        gun.mod_stats.setdefault('mods', {}).setdefault('min_ads_range', 0)
        gun.mod_stats['mods']['min_ads_range'] += 1

    def to_text(self, gun):
        return 'While ADS: +3 Range.'

class wp_part_sniper_scope(Modifier):
    name = '(Scope) Sniper Scope'
    effect = 'While ADS: +4 Range and +3 Minimum ADS Range.'
    situational = True
    weapon_types = [Guntypes.RIFLE, Guntypes.SNIPER]

    def apply(self, gun):
        gun.mod_stats.setdefault('mods', {}).setdefault('min_ads_range', 0)
        gun.mod_stats['mods']['min_ads_range'] += 1

    def to_text(self, gun):
        return 'While ADS: +4 Range.'

# Weapon Accessories
class wp_part_bayonet(Modifier):
    name = 'Bayonet'
    effect = 'While holding: Melee Die becomes a d10.'
    situational = True

class wp_part_laser_sight(Modifier):
    name = 'Laser Sight'
    effect = 'While NOT ADS: +1 on Accuracy Rolls.'
    situational = True

class wp_part_foregrip(Modifier):
    name = 'Foregrip'
    effect = '+2 on Accuracy rolls, +1 Fumble Range.'

    def apply(self, gun):
        gun.mod_stats.setdefault('mods', {}).setdefault('acc_mod', 0)
        gun.mod_stats.setdefault('mods', {}).setdefault('fumble_range', 0)
        gun.mod_stats['mods']['acc_mod'] += 2
        gun.mod_stats['mods']['fumble_range'] += 1

class wp_part_extended_magazine(Modifier):
    name = 'Extended Magazine'
    effect = '+1 Mag Size, -3 on Reload Checks.'

    def apply(self, gun):
        gun.mod_stats['mag_size'] += 1
        gun.mod_stats.setdefault('mods', {}).setdefault('reload_check', 0)
        gun.mod_stats['mods']['reload_check'] -= 3

class wp_part_light_mags(Modifier):
    name = 'Light Mags'
    effect = '-1 Mag Size, +3 on Reload Checks.'

    def apply(self, gun):
        gun.mod_stats['mag_size'] -= 1
        gun.mod_stats.setdefault('mods', {}).setdefault('reload_check', 0)
        gun.mod_stats['mods']['reload_check'] += 3

class wp_part_hairpin_trigger(Modifier):
    name = 'Hairpin Trigger'
    effect = '+2 Burst, +1 Mag Size, Consumes 2 Ammo per Attack, -3 on Accuracy Rolls.'

    def apply(self, gun):
        gun.mod_stats['mag_size'] += 1
        for atk in ['glance', 'solid', 'penetrate']:
            gun.mod_stats['hits_crits'][atk]['hits'] += 2
        gun.mod_stats.setdefault('mods', {}).setdefault('ammo_per_attack', 0)
        gun.mod_stats.setdefault('mods', {}).setdefault('acc_mod', 0)
        gun.mod_stats['mods']['ammo_per_attack'] += 1
        gun.mod_stats['mods']['acc_mod'] -= 3

class wp_part_hit_marker(Modifier):
    name = 'Hit Marker'
    effect = '-2 on Accuracy Rolls, +1 Lethal Range.'

    def apply(self, gun):
        gun.mod_stats.setdefault('mods', {}).setdefault('acc_mod', 0)
        gun.mod_stats.setdefault('mods', {}).setdefault('lethal_range', 0)
        gun.mod_stats['mods']['acc_mod'] -= 2
        gun.mod_stats['mods']['lethal_range'] += 1

class wp_part_improved_rifling(Modifier):
    name = 'Improved Rifling'
    effect = '+1 Range.'

    def apply(self, gun):
        gun.mod_stats['range'] += 1

class wp_part_sling(Modifier):
    name = 'Sling'
    effect = '+2 on Swap Checks to and from this Weapon.'

    def apply(self, gun):
        gun.mod_stats.setdefault('mods', {}).setdefault('swap_check', 0)
        gun.mod_stats['mods']['swap_check'] += 2

class wp_part_hollow_points(Modifier):
    name = 'Hollow Points'
    effect = '-1 Hit Damage, +3 Crit Damage.'

    def apply(self, gun):
        gun.mod_stats.setdefault('mods', {}).setdefault('hit_dmg', 0)
        gun.mod_stats.setdefault('mods', {}).setdefault('crit_dmg', 0)
        gun.mod_stats['mods']['hit_dmg'] -= 1
        gun.mod_stats['mods']['crit_dmg'] += 3

# Gun Generation Tables
weapon_parts_table = {
    (1, 5): wp_part_empty(),
    (6, 15): wp_part_matching_barrel(),
    (16, 25): wp_part_matching_grip(),
    (26, 35): wp_part_matching_stock(),
    (36, 50): 'sight',
    (51, 100): 'accessories'
}

weapon_sight_table = {
    (1, 25): wp_part_iron_sight(),
    (26, 50): wp_part_reflex_sight(),
    (51, 75): wp_part_acog(),
    (76, 100): wp_part_sniper_scope()
}

weapon_accessories_table = {
    (1, 10): wp_part_bayonet(),
    (11, 20): wp_part_laser_sight(),
    (21, 30): wp_part_foregrip(),
    (31, 40): wp_part_extended_magazine(),
    (41, 50): wp_part_light_mags(),
    (51, 60): wp_part_hairpin_trigger(),
    (61, 70): wp_part_hit_marker(),
    (71, 80): wp_part_improved_rifling(),
    (81, 90): wp_part_sling(),
    (91, 100): wp_part_hollow_points()
}