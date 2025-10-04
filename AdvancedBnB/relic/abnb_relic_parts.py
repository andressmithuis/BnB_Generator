from util import Modifier

from .abnb_relic_part_tables import *

# --- Gun Parts ---
class relic_part_gun_damage(Modifier):
    name = 'Gun Damage'
    effect = 'Increases Gun Damage.'
    applies_to = '<Unknown>'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x == self])
        tier = item.tier

        ret_str = f"+{gun_parts[tier]['gun_damage'] * n_parts} Damage Dice for "
        if self.applies_to in ['Pistol', 'Submachine Gun', 'Combat Rifle', 'Shotgun', 'Sniper Rifle', 'Rocket Launcher']:
            ret_str += f"{self.applies_to}s."
        else:
            ret_str += f"{self.applies_to} Guns."

        return ret_str

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.applies_to == self.applies_to


class relic_part_gun_accuracy(Modifier):
    name = 'Gun Accuracy'
    effect = 'Increases Gun Accuracy.'
    applies_to = '<Unknown>'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x == self])
        tier = item.tier

        ret_str = f"+{gun_parts[tier]['gun_accuracy'] * n_parts} {self.applies_to} ACC MOD."

        return ret_str

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.applies_to == self.applies_to


class relic_part_gun_reload(Modifier):
    name = 'Reload Speed'
    effect = 'Increases Reload Checks.'
    applies_to = '<Unknown>'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x == self])
        tier = item.tier

        return f"+{gun_parts[tier]['reload_checks'] * n_parts} on {self.applies_to} Reload Checks."

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.applies_to == self.applies_to


class relic_part_gun_swap(Modifier):
    name = 'Swap Speed'
    effect = 'Increases Swap Checks.'
    applies_to = '<Unknown>'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x == self])
        tier = item.tier

        return f"+{gun_parts[tier]['swap_checks'] * n_parts} on {self.applies_to} Swap Checks."

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.applies_to == self.applies_to


class relic_part_gun_magsize(Modifier):
    name = 'Mag Size'
    effect = 'Increases Mag Size.'
    applies_to = '<Unknown>'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x == self])
        tier = item.tier

        ret_str = f"+{gun_parts[tier]['mag_size'] * n_parts} "
        if self.applies_to in ['Pistol', 'Submachine Gun', 'Combat Rifle', 'Shotgun', 'Sniper Rifle', 'Rocket Launcher']:
            ret_str += f"{self.applies_to} Mag Size."
        else:
            ret_str += f"{self.applies_to} Gun Mag Size."

        return ret_str

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.applies_to == self.applies_to


# --- Elemental Parts ---
class relic_part_elemental_damage(Modifier):
    name = 'Elemental Damage'
    effect = 'Increases Elemental Damage.'
    applies_to = '<Unknown>'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x == self])
        tier = item.tier

        return f"+{element_parts[tier]['elemental_damage'] * n_parts} {self.applies_to} Damage Dice."

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.applies_to == self.applies_to


class relic_part_elemental_effect(Modifier):
    name = 'Status Effect Chance'
    effect = 'Increases Elemental Effect Chance.'
    applies_to = '<Unknown>'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x == self])
        tier = item.tier

        return f"+{element_parts[tier]['effect_chance'] * n_parts}% {self.applies_to} Effect Chance."

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.applies_to == self.applies_to


class relic_part_elemental_puddle(Modifier):
    name = 'Elemental Puddle'
    effect = 'Increases Elemental Puddle Chance.'
    applies_to = '<Unknown>'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x == self])
        tier = item.tier

        return f"+{element_parts[tier]['puddle_chance'] * n_parts}% Chance to create a {self.applies_to} Puddle."

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.applies_to == self.applies_to


# --- Action Skill Parts ---
class relic_part_actionskill_damage(Modifier):
    name = 'Action Skill Damage'
    effect = 'Increases Action Skill Damage.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x == self])
        tier = item.tier

        return f"+{action_skill_parts[tier]['action_skill_damage'] * n_parts} Action Skill Damage Dice."


class relic_part_actionskill_uses(Modifier):
    name = 'Action Skill Uses'
    effect = 'Increases Action Skill uses per Day.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x == self])
        tier = item.tier

        return f"+{action_skill_parts[tier]['action_skill_damage'] * n_parts} Action Skill uses per Day."


class relic_part_actionskill_duration(Modifier):
    name = 'Action Skill Duration'
    effect = 'Increases Action Skill Duration.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x == self])
        tier = item.tier

        return f"Action Skill Duration +{action_skill_parts[tier]['action_skill_damage'] * n_parts} Turns."


# --- Health Parts ---
class relic_part_max_health(Modifier):
    name = 'Max Health'
    effect = 'Increased Max Health.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x == self])
        tier = item.tier

        bonus = health_parts[tier]['max_health'] * n_parts

        return f"+{bonus} Max Health."


class relic_part_health_regen(Modifier):
    name = 'Health Regen'
    effect = 'Increased Health Regen.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x == self])
        tier = item.tier

        bonus = health_parts[tier]['health_regen'] * n_parts

        return f"+{bonus} Health Regen."


class relic_part_ffyl_duration(Modifier):
    name = 'FFYL Duration'
    effect = 'Increased FFYL Duration.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x == self])
        tier = item.tier

        bonus = health_parts[tier]['ffyl_duration'] * n_parts

        return f"+{bonus} Extra Turns when in Fight For Your Life."


class relic_part_revive_healing(Modifier):
    name = 'Revive Health'
    effect = 'Increased Health gained on Revive.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x == self])
        tier = item.tier

        return f"+{health_parts[tier]['revive_health'] * n_parts} Health gained when you are Revived."


# --- Defensive Parts ---
class relic_part_shield_capacity(Modifier):
    name = 'Shield Capacity'
    effect = 'Increased Shield Capacity.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x == self])
        tier = item.tier

        bonus = defensive_parts[tier]['shield_capacity'] * n_parts

        return f"+{bonus} Shield Capacity."


class relic_part_shield_recharge(Modifier):
    name = 'Shield Recharge'
    effect = 'Increased Shield Recharge Rate.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x == self])
        tier = item.tier

        bonus = defensive_parts[tier]['shield_recharge'] * n_parts

        return f"+{bonus} Shield Recharge Rate."


class relic_part_elemental_resistance(Modifier):
    name = 'Elemental Resistance'
    effect = 'Increased Elemental Resistance.'
    applies_to = '<Unknown>'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x == self])
        tier = item.tier

        dice_bonus = defensive_parts[tier]['elemental_resistance']
        dice_bonus.count *= n_parts

        return f"+{dice_bonus} {self.applies_to} Resistance."

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.applies_to == self.applies_to


# --- Melee Parts ---
class relic_part_melee_damage(Modifier):
    name = 'Melee Damage'
    effect = 'Increased Melee Damage.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x == self])
        tier = item.tier

        return f"+{melee_parts[tier]['melee_damage'] * n_parts} Melee Damage Dice."


class relic_part_melee_attacks(Modifier):
    name = 'Melee Attacks'
    effect = 'Extra Melee Attacks.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x == self])
        tier = item.tier

        bonus = melee_parts[tier]['melee_attacks'] * n_parts

        return f"+{bonus} Extra Melee Attacks."


class relic_part_move_speed(Modifier):
    name = 'Movement Speed'
    effect = 'Extra Movement.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x == self])
        tier = item.tier

        bonus = melee_parts[tier]['move_speed'] * n_parts

        return f"+{bonus} Extra Movement."


# --- Ammo Parts ---
class relic_part_expanded_reserve(Modifier):
    name = 'Expanded Reserve'
    effect = 'Increases Max Gun Ammo Reserves.'
    applies_to = '<Unknown>'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x == self])
        tier = item.tier

        return f"+{ammo_parts[tier]['expanded_reserves']} {self.applies_to} Ammo Reserves."

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.applies_to == self.applies_to


class relic_part_expanded_grenades(Modifier):
    name = 'Expanded Grenades'
    effect = 'Increases Max Grenades Reserves.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x == self])
        tier = item.tier

        return f"+{ammo_parts[tier]['expanded_grenades'] * n_parts} Grenade Reserves."
