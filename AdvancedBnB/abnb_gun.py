import json
import random
from copy import deepcopy

from .abnb_tables import *
from .abnb_guntypes import Guntypes
from .abnb_weapon_parts import weapon_parts_table, weapon_accessories_table, weapon_sight_table
from .cards.abnb_gun_card import generate_gun_card


def get_item_tier(level:int):
    """
    Returns Item Tier based on Item Level

    1-30:   normal
    31-35:  TVH1
    36-40:  TVH2
    41-45:  UVH1
    46-50:  UVH2
    51+:    OP
    """

    assert level > 0, f"level argument given ({level}) is not at least 1"

    for (lo, hi), tier in level_to_tiers.items():
        if lo <= level <= hi:
            return tier

def mod_to_string(val_1, val_2):
    delta = val_1 - val_2
    if delta != 0:
        return f"({'+' if delta > 0 else ''}{delta})"

    return ''


class Gun:
    def __init__(self):
        self.name = ''
        self.name_prefix = ''
        self.level = 1
        self.tier = 1
        self.rarity = Rarity.COMMON

        self.manufacturer = None
        self.eridian = False
        self.gun_type = Guntypes.PISTOL

        self.base_stats = {
            'hit_dice': Dice.from_string('1d4'),
            'crit_dice': Dice.from_string('1d4'),
            'hits_crits' : {
                'glance': {'hits': 0, 'crits': 0},
                'solid': {'hits': 0, 'crits': 0},
                'penetrate': {'hits': 0, 'crits': 0}
            },
            'range': 0,
            'mag_size': 0
        }

        self.mod_stats = deepcopy(self.base_stats)

        self.hits_crits = self.base_stats['hits_crits']

        self.hit_dice = Dice(1, 4)
        self.crit_dice = Dice(1, 4)
        self.range = 0
        self.mag_size = 0

        self.traits = []
        self.parts = []
        self.n_parts = 0
        self.max_parts = 0
        self.n_scopes = 0
        self.max_scopes = 1

        self.elements = []

        self.forced_elemental = False
        self.forced_non_elemental = False
        self.elemental_roll = {'n_rolls': 0, 'roll_bonus': 0}

        self.user_rolls = False

    def generate(self, user_rolls=False, props = None):
        self.user_rolls = user_rolls

        # Prepare dice
        d100 = Dice(1, 100)
        d4 = Dice(1, 4)
        d6 = Dice(1, 6)
        d12 = Dice(1, 12)

        # Determine level and tier
        if props is not None and 'level' in props:
            self.level = props['level']
        self.tier = get_item_tier(self.level)

        # Manufacturer and gun type
        print(f"Determining Gun Manufacturer...")
        if props is not None and 'manufacturer' in props:
            self.manufacturer = props['manufacturer']
            if self.manufacturer == Manufacturers.ERIDIAN:
                print("MANUFACTURER == ERIDIAN")
                self.eridian = True
                self.manufacturer = None

        while self.manufacturer is None:
            roll = d12.roll(self.user_rolls)
            self.manufacturer = manufacturer_table[roll]
            print(f"Rolled a {roll}! Gun Manufacturer = {self.manufacturer}")
            if self.manufacturer == Manufacturers.ERIDIAN:
                print(f"Rolled Eridian Manufacturer. Roll again for Manufacturer of Gun Base.")
                self.eridian = True
                self.manufacturer = None

        print(f"Determining Gun Type...")
        if props is not None and 'gun_type' in props:
            self.gun_type = props['gun_type']
        else:
            roll = d12.roll(self.user_rolls)
            self.gun_type = self.manufacturer.make_random_gun(roll)
            print(f"Rolled a {roll}! Gun Type = {self.gun_type}")

        # Weapon base stats
        self.base_stats = self.gun_type.get_basestats(self.tier)
        self.mod_stats = deepcopy(self.base_stats)

        # Rarity and element
        print(f"Determining Gun Rarity and Element...")
        d4_roll = d4.roll(self.user_rolls)
        d6_roll = d6.roll(self.user_rolls)
        self.rarity, roll_for_element = rarity_tables['normal'][d4_roll][d6_roll]

        if props is not None and 'rarity' in props:
            self.rarity = props['rarity']

        if roll_for_element:
            self.elemental_roll['n_rolls'] = 1

        print(f"Rolled a {d4_roll}(d4) and a {d6_roll}(d6)! Gun Rarity = {self.rarity}.{' Might also be Elemental.' if roll_for_element else ''}")

        # Add Manufacturer Primary Traits
        print(f"Determining Manufacturer Primary Gun Traits...")
        for trait in self.manufacturer.weapon_traits['primary']:
            self.traits.append(trait)

        # Add Manufacturer Secondary Trait (chosen randomly)
        print(f"Determining Manufacturer Secondary Gun Traits...")
        if self.manufacturer != Manufacturers.DAHL:
            trait = self.manufacturer.pick_secondary_weapon_trait(self.user_rolls)
            if trait:
                self.traits.append(trait)

        # Roll for weapon parts
        print(f"Determining Gun Parts...")
        self.max_parts = weapon_part_count[self.rarity]
        self.n_parts = 0
        self.n_scopes = 0

        # PART EXCEPTIONS TODO: Add these to the Dice Rolls Questions
        # Sniper Rifle spawns with a Scope. This DOES count towards the maximum equipped number of parts
        Guntypes.SNIPER.gun_part_exception(self)

        # Bandit weapons always spawn with a Bayonet Accessory. This does NOT count towards number of Gun Parts
        Manufacturers.BANDIT.gun_part_exception(self)

        # Combat Rifle Spawns with one accessory. This does NOT count towards number of Gun Parts
        Guntypes.RIFLE.gun_part_exception(self)

        # Dahl weapons trait 'Tacti-cool' determines number of scopes and maybe accessories. Scopes count towards maximum number of parts, Accessories are extra
        Manufacturers.DAHL.gun_part_exception(self)

        # Roll for remaining parts
        while self.n_parts < self.max_parts:
            print(f"Rolling for part {self.n_parts+1}/{self.max_parts}...")
            roll = d100.roll(self.user_rolls)
            part = roll_on_table(weapon_parts_table, roll)

            if part == 'sight':
                print(f"Rolled a {roll}! You may roll for a Gun Scope!")
                if self.n_scopes < self.max_scopes:
                    part = self.pick_weapon_scope()
                    self.n_scopes += 1
            elif part == 'accessories':
                print(f"Rolled a {roll}! You may roll for a Gun Accessory!")
                part = self.pick_weapon_accessory()

            if type(part) != str and part not in self.parts:
                self.parts.append(part)
                self.n_parts += 1

        # Apply Traits and Gun Part Effects
        self.apply_effects()

        # Roll for element (if applicable)
        if self.forced_elemental and self.elemental_roll['n_rolls'] == 0:
            self.elemental_roll['n_rolls'] = 1

        if self.forced_non_elemental and not self.forced_elemental:
            self.elemental_roll['n_rolls'] = 0

        while self.elemental_roll['n_rolls'] > 0:
            dice_roll = min([d100.roll() + self.elemental_roll['roll_bonus'], 100])
            el_roll = roll_on_table(elemental_table, dice_roll)[self.rarity]

            # Maliwan can't be explosive, unless its part of a Fusion
            if self.manufacturer == Manufacturers.MALIWAN:
                if type(el_roll) == Explosive:
                    el_roll = None

            if el_roll is None:
                print(f"NO ELEMENT ROLLED! {dice_roll}")
                if not self.forced_elemental:
                    self.elemental_roll['n_rolls'] -= 1
            elif type(el_roll) == Fusion:
                d8 = Dice.from_string('2d8')

                while True:
                    rolls = d8.roll_dice()
                    # TODO: Handle 'Special' columns
                    if rolls[0] != 8 and rolls[0] != rolls[1]:
                        fusion_el = fusion_table[rolls[0]][rolls[1]]

                        if fusion_el is not None and fusion_el != 'special':
                            if fusion_el is not None:
                                fusion_el.bonus = el_roll.bonus
                                self.elements.append(fusion_el)
                                self.elemental_roll['n_rolls'] -= 1
                                break
            else:
                self.elements.append(el_roll)
                self.elemental_roll['n_rolls'] -= 1

        # Run final effect checks
        for trait in self.traits:
            trait.finalize(self)

        # If Originally Manufactured by Eridian. Apply Eridian Effects afterwards
        if self.eridian:
            self.manufacturer = Manufacturers.ERIDIAN
            self.manufacturer.gun_part_exception(self)

        # Calculate final stats
        self.calculate_stats()

        # Pick random Gun Name
        self.randomize_name()


    def apply_effects(self):
        # Apply Traits
        for trait in self.traits:
            trait.apply(self)

        # Apply Parts
        for part in self.parts:
            part.apply(self)

        # Apply Gun Type Bonus
        for bonus in self.gun_type.weapon_bonus:
            bonus.apply(self)

    def calculate_stats(self):
        # Extract final stats
        self.hit_dice = self.mod_stats['hit_dice']
        self.crit_dice = self.mod_stats['crit_dice']
        self.hits_crits = self.mod_stats['hits_crits']
        self.range = self.mod_stats['range']
        self.mag_size = self.mod_stats['mag_size']

    def randomize_name(self):
        with open('assets.json') as file:
            asset_data = json.load(file)

        self.asset = random.choice(asset_data['weapons'][self.gun_type.asset_dir])
        self.name = self.asset['item_name']

    def pick_weapon_accessory(self):
        d100 = Dice.from_string('1d100')

        part = None
        retries_left = 50
        while retries_left > 0:
            roll = d100.roll(self.user_rolls)
            part = roll_on_table(weapon_accessories_table, roll)
            if part not in self.parts:
                print(f"Rolled a {roll}! Adding Gun Accessory <{part.name}>!")
                break

            print(f"Rolled a {roll}! But the part <{part.name}> is invalid. Roll again...")
            part = None
            retries_left -= 1

        assert part is not None, f"Failed to roll for a Weapon Accessory..."

        return part

    def pick_weapon_scope(self):
        part = None
        d100 = Dice.from_string('1d100')

        retries_left = 50
        while retries_left > 0:
            roll = d100.roll(self.user_rolls)
            part = roll_on_table(weapon_sight_table, roll)
            if self.gun_type in part.weapon_types:
                if part not in self.parts:
                    print(f"Rolled a {roll}! Adding Gun Scope <{part.name}>!")
                    break

            print(f"Rolled a {roll}! But the part <{part.name}> is invalid. Roll again...")
            part = None
            retries_left -= 1

        assert part is not None, f"Failed to roll for a Weapon Scope...\n{self}"

        return part

    def generate_card(self):
        generate_gun_card(self)


    def  __repr__(self):
        str = ''
        str += f"--- Generated Gun --- \n"
        str += f"Name: <{self.name_prefix + ' ' if self.name_prefix != '' else ''}{self.name}> \n"
        str += f"Type: (Lv.{self.level}) {self.rarity} {self.gun_type}\n"
        str += f"Manufacturer: {self.manufacturer}\n"
        str += f"n Gun Parts: {self.max_parts}\n"
        str += f"n Gun Scope: {self.max_scopes}\n"

        str += f"Elements: "
        if self.forced_elemental or not self.forced_non_elemental:
            for el in self.elements:
                str += f"{el} "
        str += f"\n\n"

        mod_str = mod_to_string(self.range, self.base_stats['range'])
        str += f"Range: {self.range}{mod_str}\n"
        mod_str = mod_to_string(self.mag_size, self.base_stats['mag_size'])
        str += f"Mag Size: {self.mag_size}{mod_str}\n"
        str += f"Accuracy:\n"
        for atk, acc_range in [('glance', '2-7 '),  ('solid', '8-15'), ('penetrate', '16+ ')]:
            hit_mod = mod_to_string(self.hits_crits[atk]['hits'], self.base_stats['hits_crits'][atk]['hits'])
            crit_mod = mod_to_string(self.hits_crits[atk]['crits'], self.base_stats['hits_crits'][atk]['crits'])

            str += f" - {acc_range}: {self.hits_crits[atk]['hits']}{hit_mod} Hits, {self.hits_crits[atk]['crits']}{crit_mod} Crits\n"

        str += f"Hit Die : {self.hit_dice}\n"
        str += f"Crit Die: {self.crit_dice}\n"
        str += f"\n"

        # Weapon Bonus
        str += f"Weapon Bonus:\n"
        for bonus in self.gun_type.weapon_bonus:
            str += f" - {bonus}\n"
        str += f"\n"

        # Print Weapon Traits
        str += f"Traits:\n"
        for trait in self.traits:
           str += f" - {trait.name} - {trait.to_text(self)}\n"
        str += f"\n"

        # Print Weapon Parts
        str += f"Parts:\n"
        for part in self.parts:
            str += f" - {part.name}: {part}\n"
        str += f"\n"

        # Mods & Checks
        str += f"Mods & Checks:\n"
        if 'mods' in self.mod_stats:
            for k, v in self.mod_stats['mods'].items():
                w_parts = k.split('_')
                for i in range(len(w_parts)):
                    w = w_parts[i]
                    w = f"{w[0].upper()}{w[1:]}"
                    if w in ['Dmg', 'Ads', 'Acc', 'Mod']:
                        w = w.upper()
                    w_parts[i] = w
                k = ' '.join(w_parts)
                str += f" - {k} {'+' if v > 0 else ''}{v} \n"

        return str




