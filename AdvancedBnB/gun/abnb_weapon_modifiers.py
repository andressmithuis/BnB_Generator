import math

from AdvancedBnB.shield import Shieldtypes
from util import Modifier, Dice, Rarity

class mod_dmg_mod(Modifier):
    name = 'DMG MOD'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"DMG MOD {'+' if self.value > 0 else ''}{self.value}"


class mod_acc_mod(Modifier):
    name = 'ACC MOD'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"ACC MOD {'+' if self.value > 0 else ''}{self.value}"


class mod_range(Modifier):
    name = 'Range'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Range {'+' if self.value > 0 else ''}{self.value}"

    def apply_to_equipment(self, equipment):
        equipment.range += self.value

    def revert_from_equipment(self, equipment):
        equipment.range -= self.value


class mod_hit_damage(Modifier):
    name = 'Hit Damage'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Hit Damage {'+' if self.value > 0 else ''}{self.value}"


class mod_crit_damage(Modifier):
    name = 'Crit Damage'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Crit Damage {'+' if self.value > 0 else ''}{self.value}"


class mod_burst(Modifier):
    name = 'Burst MOD'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Burst {'+' if self.value > 0 else ''}{self.value}"


class mod_ammo_cost(Modifier):
    name = 'Ammo per Attack'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Ammo per Attack {'+' if self.value > 0 else ''}{self.value}"


class mod_lethal_range(Modifier):
    name = 'Lethal range'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Lethal range {'+' if self.value > 0 else ''}{self.value}"


class mod_mag_size(Modifier):
    name = 'Magazine Size MOD'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Mag size {'+' if self.value > 0 else ''}{self.value}"


class mod_ads_range_min(Modifier):
    name = 'Minimum ADS Range'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Min ADS range {'+' if self.value > 0 else ''}{self.value}"


class mod_fumble_range(Modifier):
    name = 'Fumble Range'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Fumble range {'+' if self.value > 0 else ''}{self.value}"


class mod_extra_movement(Modifier):
    name = 'Extra Movement'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Extra Movement {'+' if self.value > 0 else ''}{self.value}"


class mod_extra_attack(Modifier):
    name = 'Extra Attack'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Extra Attack {'+' if self.value > 0 else ''}{self.value}"


class mod_reload_check(Modifier):
    name = 'Reload Check'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Reload Check {'+' if self.value > 0 else ''}{self.value}"


class mod_swap_check(Modifier):
    name = 'Swap Check'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Swap Check {'+' if self.value > 0 else ''}{self.value}"


class mod_splash(Modifier):
    name = 'Splash'

    def __init__(self):
        self.effect = "Splash"


class mod_splash_range(Modifier):
    name = 'Splash Range'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Splash Range {'+' if self.value > 0 else ''}{self.value}"


class mod_knock_back(Modifier):
    name = 'Knock Back Chance'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Knock Back {'+' if self.value > 0 else ''}{self.value}%"


# Anshin - Secondary Gun Properties
healing = {
    Rarity.COMMON: 2,
    Rarity.UNCOMMON: 4,
    Rarity.RARE: 6,
    Rarity.EPIC: 8,
    Rarity.LEGENDARY: 10,
    Rarity.PEARLESCENT: 12
}

class mod_medic(Modifier):
    name = 'Medic'
    situational = True

    @property
    def effect(self):
        equipment = self.linked_property.linked_equipment
        heal_value = healing[equipment.rarity]
        return f"When you Target an Ally, they regain Health ({heal_value}/Hit, {heal_value * 2}/Crit)."


class mod_vampire(Modifier):
    name = 'Vampire'
    situational = True

    @property
    def effect(self):
        equipment = self.linked_property.linked_equipment
        heal_value = healing[equipment.rarity]
        return f"When you Damage an Enemy, you regain Health ({heal_value}/Hit, {heal_value * 2}/Crit)."


# --- Bandit ---
class mod_overheat(Modifier):
    name = 'Overheat'
    situational = True

    overheat = {
        Rarity.COMMON: '1d4',
        Rarity.UNCOMMON: '1d6',
        Rarity.RARE: '1d8',
        Rarity.EPIC: '1d10',
        Rarity.LEGENDARY: '1d12',
        Rarity.PEARLESCENT: '2d8'
    }

    @property
    def effect(self):
        equipment = self.linked_property.linked_equipment

        dice_multi = 1
        if equipment.tier >= 4:
            dice_multi = 2
        if equipment.tier >= 7:
            dice_multi = 3
        if equipment.tier >= 10:
            dice_multi = 4

        dmg_die = Dice.from_string(self.overheat[equipment.rarity])
        dmg_die.count *= dice_multi

        return f"When Reloading: You and Adjacent Targets take {dmg_die} Elemental Damage (Same Element as the Gun, Incendiary if Non Elemental)."


# --- Dahl ---
class mod_tacticool(Modifier):
    name = 'Tacti-cool'
    effect = "Gains extra Parts."
    hidden = True

    def __init__(self):
        self.applied_fire_modes = []
        self.applied_scopes = []
        self.applied_accessories = []

    def apply_to_equipment(self, equipment):
        tacticool = {
            Rarity.COMMON: {'fire_modes': 1, 'scopes': 1},
            Rarity.UNCOMMON: {'fire_modes': 1, 'scopes': 1, 'accessories': 1},
            Rarity.RARE: {'fire_modes': 2, 'scopes': 1, 'accessories': 1},
            Rarity.EPIC: {'fire_modes': 2, 'scopes': 2, 'accessories': 1},
            Rarity.LEGENDARY: {'fire_modes': 2, 'scopes': 2, 'accessories': 2},
            Rarity.PEARLESCENT: {'fire_modes': 2, 'scopes': 2, 'accessories': 3},
        }

        extra_parts = tacticool[equipment.rarity]

        # Add Fire Mode(s)
        # (Exclusive to DAHL's 'Tacti-Cool', fixed number)
        for _ in range(extra_parts['fire_modes']):
            while True:
                fire_mode = equipment.manufacturer.pick_fire_mode()
                if fire_mode not in equipment.equipment_properties:
                    equipment.add_property(fire_mode)
                    self.applied_fire_modes.append(fire_mode)
                    break

        # Add Scope(s)
        equipment.max_scopes = extra_parts['scopes']
        for _ in range(extra_parts['scopes']):
            if equipment.n_scopes >= equipment.max_scopes:
                break
            part = equipment.pick_weapon_scope()
            equipment.add_property(part)
            self.applied_scopes.append(part)
            equipment.n_scopes += 1
            equipment.n_parts += 1

        # Add Bonus Accessories (don't count towards total)
        if 'accessories' in extra_parts:
            for _ in range(extra_parts['accessories']):
                part = equipment.pick_weapon_accessory()
                equipment.add_property(part)
                self.applied_accessories.append(part)

    def revert_from_equipment(self, equipment):
        # Remove Fire Mode(s)
        to_remove = self.applied_fire_modes.copy()
        for fire_mode in to_remove:
            equipment.remove_property(fire_mode)

        self.applied_fire_modes.clear()

        # Remove Scope(s)
        to_remove = self.applied_scopes.copy()
        for scope_property in to_remove:
            equipment.remove_property(scope_property)
            equipment.n_scopes -= 1
            equipment.n_parts -= 1

        equipment.max_scopes = 1  # Remove DAHL scope limit exception

        self.applied_scopes.clear()

        # Remove Bonus Accessories
        to_remove = self.applied_accessories.copy()
        for accessory in to_remove:
            equipment.remove_property(accessory)

        self.applied_accessories.clear()


# --- Hyperion ---
class mod_gun_shield(Modifier):
    name = 'Gun Shield'
    effect = 'While ADS: Gun provides an Extra Energy Shield. Capacity is half of a Balanced Shield. Recharges after every Encounter.'
    situational = True

    @property
    def effect(self):
        equipment = self.linked_property.linked_equipment
        shield_stats = Shieldtypes.BALANCED.get_basestats(equipment.tier)
        shield_cap = math.floor(shield_stats['capacity'] / 2)

        return f"While ADS: Gun gives an Extra Shield (Capacity: {shield_cap}). Recharges after Encounter."


# --- Torgue ---
class mod_explosive_only(Modifier):
    name = 'Explosive Only'
    effect = 'This Equipment can only get the Explosive Element.'


# --- Pangolin ---
battery = {
    Rarity.COMMON: 2,
    Rarity.UNCOMMON: 4,
    Rarity.RARE: 6,
    Rarity.EPIC: 8,
    Rarity.LEGENDARY: 10,
    Rarity.PEARLESCENT: 12
}

class mod_charge(Modifier):
    name = 'Charge'
    effect = 'When you Target an Ally, they regain Shields.'
    situational = True

    @property
    def effect(self):
        equipment = self.linked_property.linked_equipment
        amount = battery[equipment.rarity]
        return f"When you Target an Ally, they regain Shields ({amount}/Hit, {amount * 2}/Crit)."


class mod_drain(Modifier):
    name = 'Drain'
    effect = 'When you Damage an Enemy, you regain Shields.'
    situational = True

    @property
    def effect(self):
        equipment = self.linked_property.linked_equipment
        amount = battery[equipment.rarity]
        return f"When you Damage an Enemy, you regain Shields ({amount}/Hit, {amount * 2}/Crit)."


# --- Vladof ---
class mod_grenade_launcher(Modifier):
    name = 'Grenade Launcher'
    effect = '(1/Encounter) Shoot a 1d8/Tier Explosive Grenade at a point within 5 squares.'
    situational = True

    @property
    def effect(self):
        equipment = self.linked_property.linked_equipment
        dmg_dice = Dice(1, 8)
        dmg_dice.count *= equipment.tier
        return f"(1/Encounter): Shoot a {dmg_dice} Explosive Grenade at a point within 5 squares."


class mod_taser(Modifier):
    name = 'Taser'
    effect = '(1/Encounter) When used: Each Enemy within a 3 square Cone takes 1d4/Tier Shock Damage and is Dazed.'
    situational = True

    @property
    def effect(self):
        equipment = self.linked_property.linked_equipment
        dmg_dice = Dice(1, 4)
        dmg_dice.count *= equipment.tier
        return f"(1/Encounter) When used: Each Enemy within a 3 square Cone takes {dmg_dice} Shock Damage and is Dazed."
