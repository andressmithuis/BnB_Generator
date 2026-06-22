import math

from AdvancedBnB.shield import Shieldtypes
from util.modifier import Modifier, AdditiveModifier
from util import Dice, Rarity



class mod_dmg_mod(AdditiveModifier):
    name = 'DMG MOD'


class mod_acc_mod(AdditiveModifier):
    name = 'ACC MOD'


class mod_range(AdditiveModifier):
    name = 'Range'
    hidden = True


class mod_hit_damage(AdditiveModifier):
    name = 'Hit Damage'


class mod_crit_damage(AdditiveModifier):
    name = 'Crit Damage'


class mod_burst(AdditiveModifier):
    name = 'Burst'
    hidden = True


class mod_ammo_cost(AdditiveModifier):
    name = 'Ammo per Attack'


class mod_lethal_range(AdditiveModifier):
    name = 'Lethal range'


class mod_mag_size(AdditiveModifier):
    name = 'Mag size'
    hidden = True


class mod_ads_range_min(AdditiveModifier):
    name = 'Min ADS range'


class mod_fumble_range(AdditiveModifier):
    name = 'Fumble Range'


class mod_extra_movement(AdditiveModifier):
    name = 'Extra Movement'


class mod_extra_attack(AdditiveModifier):
    name = 'Extra Attack'


class mod_reload_check(AdditiveModifier):
    name = 'Reload Check'


class mod_swap_check(AdditiveModifier):
    name = 'Swap Check'


class mod_splash(Modifier):
    name = 'Splash'

    def __init__(self):
        self.effect = "Splash"


class mod_splash_range(AdditiveModifier):
    name = 'Splash Range'


class mod_knock_back(AdditiveModifier):
    name = 'Knock Back Chance'
    additive = True

    @property
    def effect(self):
        return f"Knock Back {'+' if self.value > 0 else ''}{self.value}%"


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
        equipment = self.get_linked_equipment()
        heal_value = healing[equipment.rarity]
        return f"When you Target an Ally, they regain Health ({heal_value}/Hit, {heal_value * 2}/Crit)."


class mod_vampire(Modifier):
    name = 'Vampire'
    situational = True

    @property
    def effect(self):
        equipment = self.get_linked_equipment()
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
        equipment = self.get_linked_equipment()

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
        equipment = self.get_linked_equipment()
        shield_stats = Shieldtypes.BALANCED.get_basestats(equipment.tier)
        shield_cap = math.floor(shield_stats['capacity'] / 2)

        return f"While ADS: Gun gives an Extra Shield (Capacity: {shield_cap}). Recharges after Encounter."


# --- Torgue ---
class mod_explosive_only(Modifier):
    name = 'Explosive Only'
    effect = 'This Equipment can only get the Explosive Element.'


# --- Jakobs ---
class mod_penetrate_crits(AdditiveModifier):
    name = 'Penetrate Crits'
    hidden = True

class mod_lethal_crits(AdditiveModifier):
    name = 'Lethal Crits'


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
        equipment = self.get_linked_equipment()
        amount = battery[equipment.rarity]
        return f"When you Target an Ally, they regain Shields ({amount}/Hit, {amount * 2}/Crit)."


class mod_drain(Modifier):
    name = 'Drain'
    effect = 'When you Damage an Enemy, you regain Shields.'
    situational = True

    @property
    def effect(self):
        equipment = self.get_linked_equipment()
        amount = battery[equipment.rarity]
        return f"When you Damage an Enemy, you regain Shields ({amount}/Hit, {amount * 2}/Crit)."


# --- Vladof ---
class mod_grenade_launcher(Modifier):
    name = 'Grenade Launcher'
    effect = '(1/Encounter) Shoot a 1d8/Tier Explosive Grenade at a point within 5 squares.'
    situational = True

    @property
    def effect(self):
        equipment = self.get_linked_equipment()
        dmg_dice = Dice(1, 8)
        dmg_dice.count *= equipment.tier
        return f"(1/Encounter): Shoot a {dmg_dice} Explosive Grenade at a point within 5 squares."


class mod_taser(Modifier):
    name = 'Taser'
    effect = '(1/Encounter) When used: Each Enemy within a 3 square Cone takes 1d4/Tier Shock Damage and is Dazed.'
    situational = True

    @property
    def effect(self):
        equipment = self.get_linked_equipment()
        dmg_dice = Dice(1, 4)
        dmg_dice.count *= equipment.tier
        return f"(1/Encounter) When used: Each Enemy within a 3 square Cone takes {dmg_dice} Shock Damage and is Dazed."
