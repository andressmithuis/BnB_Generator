from util import mod_template, EquipmentProperty
from .abnb_weapon_modifiers import *
from .abnb_guntypes import Guntypes

class WeaponPart(EquipmentProperty):
    pass


# Weapon Parts
class wp_part_empty(WeaponPart):
    name = 'Trinket'
    effect = 'Looks cool. Does Nothing.'

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, self.effect)
        new_modifier.hidden = True
        self.replace_modifiers([new_modifier])

class wp_part_matching_barrel(WeaponPart):
    name = 'Matching Barrel'
    effect = '+2 on DMG Rolls.'

    def reload_modifiers(self):
        self.replace_modifiers([mod_dmg_mod(2)])


class wp_part_matching_grip(WeaponPart):
    name = 'Matching Grip'
    effect = '+1 on Reload and Swap Checks.'

    def reload_modifiers(self):
        self.replace_modifiers([mod_reload_check(1), mod_swap_check(1)])


class wp_part_matching_stock(WeaponPart):
    name = 'Matching Stock'
    effect = '+1 on Accuracy Rolls.'

    def reload_modifiers(self):
        self.replace_modifiers([mod_dmg_mod(1)])


# Weapon Sights / Scopes
class wp_part_iron_sight(WeaponPart):
    name = '(Scope) Iron Sight'
    effect = 'While ADS: +1 Range and +1 Minimum ADS Range.'
    weapon_types = [Guntypes.RIFLE, Guntypes.PISTOL, Guntypes.LAUNCHER, Guntypes.SHOTGUN, Guntypes.SMG]

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, 'While ADS: +1 Range')
        new_modifier.situational = True
        self.replace_modifiers([mod_ads_range_min(1), new_modifier])


class wp_part_reflex_sight(WeaponPart):
    name = '(Scope) Reflex Sight'
    effect = 'While ADS: +2 Range and +1 Minimum ADS Range.'
    weapon_types = [Guntypes.RIFLE, Guntypes.PISTOL, Guntypes.LAUNCHER, Guntypes.SHOTGUN, Guntypes.SMG]

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, 'While ADS: +2 Range')
        new_modifier.situational = True
        self.replace_modifiers([mod_ads_range_min(1), new_modifier])


class wp_part_acog(WeaponPart):
    name = '(Scope) ACOG'
    effect = 'While ADS: +3 Range and +2 Minimum ADS Range.'
    weapon_types = [Guntypes.RIFLE, Guntypes.LAUNCHER, Guntypes.SNIPER]

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, 'While ADS: +3 Range')
        new_modifier.situational = True
        self.replace_modifiers([mod_ads_range_min(2), new_modifier])


class wp_part_sniper_scope(WeaponPart):
    name = '(Scope) Sniper Scope'
    effect = 'While ADS: +4 Range and +3 Minimum ADS Range.'
    weapon_types = [Guntypes.RIFLE, Guntypes.SNIPER]

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, 'While ADS: +4 Range')
        new_modifier.situational = True
        self.replace_modifiers([mod_ads_range_min(3), new_modifier])


# Weapon Accessories
class wp_part_bayonet(WeaponPart):
    name = 'Bayonet'
    effect = 'While holding: Melee Die becomes a d10.'

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, self.effect)
        new_modifier.situational = True
        self.replace_modifiers([new_modifier])


class wp_part_laser_sight(WeaponPart):
    name = 'Laser Sight'
    effect = 'While NOT ADS: +1 on Accuracy Rolls.'

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, self.effect)
        new_modifier.situational = True
        self.replace_modifiers([new_modifier])


class wp_part_foregrip(WeaponPart):
    name = 'Foregrip'
    effect = '+2 on Accuracy rolls, +1 Fumble Range.'

    def reload_modifiers(self):
        self.replace_modifiers([mod_acc_mod(2), mod_fumble_range(1)])


class wp_part_extended_magazine(WeaponPart):
    name = 'Extended Magazine'
    effect = '+1 Mag Size, -3 on Reload Checks.'

    def reload_modifiers(self):
        self.replace_modifiers([mod_mag_size(1), mod_reload_check(-3)])


class wp_part_light_mags(WeaponPart):
    name = 'Light Mags'
    effect = '-1 Mag Size, +3 on Reload Checks.'

    def reload_modifiers(self):
        self.replace_modifiers([mod_mag_size(-1), mod_reload_check(3)])


class wp_part_hairpin_trigger(WeaponPart):
    name = 'Hairpin Trigger'
    effect = '+2 Burst, +1 Mag Size, Consumes 2 Ammo per Attack, -3 on Accuracy Rolls.'

    def reload_modifiers(self):
        self.replace_modifiers([
            mod_burst(2),
            mod_mag_size(1),
            mod_ammo_cost(1),
            mod_acc_mod(-3)
        ])


class wp_part_hit_marker(WeaponPart):
    name = 'Hit Marker'
    effect = '-2 on Accuracy Rolls, +1 Lethal Range.'

    def reload_modifiers(self):
        self.replace_modifiers([
            mod_acc_mod(-2),
            mod_lethal_range(1)
        ])


class wp_part_improved_rifling(WeaponPart):
    name = 'Improved Rifling'
    effect = '+1 Range.'

    def reload_modifiers(self):
        self.replace_modifiers([
            mod_range(1)
        ])


class wp_part_sling(WeaponPart):
    name = 'Sling'
    effect = '+2 on Swap Checks to and from this Weapon.'

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, self.effect)
        new_modifier.situational = True
        self.replace_modifiers([new_modifier])


class wp_part_hollow_points(WeaponPart):
    name = 'Hollow Points'
    effect = '-1 Hit Damage, +3 Crit Damage.'

    def apply(self, gun):
        gun.mod_stats.setdefault('mods', {}).setdefault('hit_dmg', 0)
        gun.mod_stats.setdefault('mods', {}).setdefault('crit_dmg', 0)
        gun.mod_stats['mods']['hit_dmg'] -= 1
        gun.mod_stats['mods']['crit_dmg'] += 3


    def reload_modifiers(self):
        self.replace_modifiers([
            mod_hit_damage(-1),
            mod_crit_damage(3)
        ])

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