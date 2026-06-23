import json
import random
from copy import deepcopy

from util import Equipment, Dice, lookup_in_table
from AdvancedBnB import Fusion
from AdvancedBnB.abnb_tables import rarity_tables, weapon_part_count, elemental_table, fusion_table
from AdvancedBnB.abnb_util import get_item_tier
from AdvancedBnB.abnb_manufacturers import Manufacturers, manufacturer_table
from AdvancedBnB.gun.abnb_weapon_modifiers import *
from AdvancedBnB.gun.abnb_weapon_traits import WeaponTrait
from AdvancedBnB.gun.abnb_weapon_parts import WeaponPart, WeaponPartScope, weapon_parts_table, weapon_accessories_table, weapon_sight_table
from AdvancedBnB.gun.abnb_guntypes import Guntypes
from AdvancedBnB.gun.abnb_gun_card import generate_gun_card


def mod_to_string(val_1, val_2):
    delta = val_1 - val_2
    if delta != 0:
        return f"({'+' if delta > 0 else ''}{delta})"

    return ''

class Gun(Equipment):
    def __init__(self):
        super().__init__()

        self._gun_type = Guntypes.PISTOL

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

        self.hit_dice = Dice(1, 4)
        self.crit_dice = Dice(1, 4)

    def generate(self, user_rolls=False):
        # Prepare dice
        d100 = Dice(1, 100)
        d4 = Dice(1, 4)
        d6 = Dice(1, 6)
        d12 = Dice(1, 12)
        #Dice.input_rolls = True

        # Determine level and tier
        self.tier = get_item_tier(self.level)

        # Manufacturer and gun type
        print(f"Determining Gun Manufacturer...")
        while self.manufacturer is None:
            roll = d12.roll(f"Roll for Manufacturer")
            new_manufacturer = manufacturer_table[roll]
            print(f"Rolled a {roll}! Gun Manufacturer = {new_manufacturer}")
            if new_manufacturer == Manufacturers.ERIDIAN:
                print(f"Rolled Eridian Manufacturer. Roll again for Manufacturer of Gun Base.")
                self.eridian = True
                self.manufacturer = None
            else:
                self.set_manufacturer(new_manufacturer)

        print(f"Determining Gun Type...")
        roll = d12.roll(f"Roll for Gun Type")
        self.gun_type = self.manufacturer.make_random_gun(roll)
        print(f"Rolled a {roll}! Gun Type = {self.gun_type}")

        # Weapon base stats
        self.base_stats = self.gun_type.get_basestats(self.tier)
        self.hit_dice = self.base_stats['hit_dice']
        self.crit_dice = self.base_stats['crit_dice']

        # Rarity and element
        print(f"Determining Gun Rarity and Element...")
        d4_roll = d4.roll(f"Roll for Rarity and Element(1/2)")
        d6_roll = d6.roll(f"Roll for Rarity and Element(2/2)")
        self.rarity, roll_for_element = rarity_tables['normal'][d4_roll][d6_roll]

        print(f"Rolled a {d4_roll}(d4) and a {d6_roll}(d6)! Gun Rarity = {self.rarity}.{' Might also be Elemental.' if roll_for_element else ''}")

        # Roll for weapon parts
        print(f"Determining Gun Parts...")

        # Resolve Gun Parts provided by Traits/Mods (These all do not count towards Part count total)
        max_firemodes = self.get_modifier_value(mod_tacticool_firemodes)
        n_firemodes = 0
        while n_firemodes < max_firemodes:
            fire_mode = Manufacturers.DAHL.pick_fire_mode()
            if self.has_property(type(fire_mode)) is False:
                self.add_property(fire_mode)
                n_firemodes += 1
            else:
                print(f"Fire mode <{fire_mode.name}> already present!")

        max_scopes = self.get_modifier_value(mod_fixed_scopes)
        n_scopes = 0
        while n_scopes < max_scopes:
            scope_part = self.pick_weapon_scope()
            if self.has_property(type(scope_part)) is False:
                self.add_property(scope_part)
                n_scopes += 1
            else:
                print(f"Scope Part <{scope_part.name}> already present!")

        max_parts = self.get_modifier_value(mod_extra_accessories)
        n_parts = 0
        while n_parts < max_parts:
            accessory_part = self.pick_weapon_accessory()
            if self.has_property(type(accessory_part)) is False:
                self.add_property(accessory_part)
                n_parts += 1
            else:
                print(f"Accessory Part <{accessory_part.name}> already present!")

        # Roll for remaining parts
        self.n_parts = 0
        while self.n_parts < self.max_parts:
            print(f"Rolling for part {self.n_parts+1}/{self.max_parts}...")
            roll = d100.roll(f"Roll for Gun Part")
            part = lookup_in_table(weapon_parts_table, roll)

            if part == 'sight':
                print(f"Rolled a {roll}! You may roll for a Gun Scope!")
                if self.has_property(WeaponPartScope):
                    print(f"Gun already has a Gun Scope... Roll for new part...")
                    part = None
                else:
                    part = self.pick_weapon_scope()
                    # Check if Scope is compatible with the Gun Type
                    if not self.gun_type in part.weapon_types:
                        print(f"Gun Type <{self.gun_type}> is not compatible with Scope <{part.name}>... Roll for new part...")
                        part = None

            elif part == 'accessories':
                print(f"Rolled a {roll}! You may roll for a Gun Accessory!")
                part = self.pick_weapon_accessory()

            # Check if part is already applied
            if self.has_property(type(part)):
                print(f"Picked a <{part.name}>! But the Gun already has it... Try again!")
                part = None

            if part is not None:
                self.add_property(part)
                self.n_parts += 1

        # Roll for element (if applicable)
        if self.forced_elemental is True:
            self.min_elements = max(self.min_elements, 1)

        if self.forced_non_elemental is True and self.forced_elemental is False:
            self.min_elements = 0

        if roll_for_element is True and len(self.elements) > 0:
            # Already got at least one Element forced by a Modifier, which replaces the one that could result from the rarity table
            roll_for_element = False

        while roll_for_element is True or len(self.elements) < self.min_elements:
            dice_roll = min([d100.roll(f"Roll on Element table") + self.elemental_roll_bonus, 100])
            el_roll = lookup_in_table(elemental_table, dice_roll)[self.rarity]

            # Ignore disabled elements
            if type(el_roll) in [type(el) for el in self.disabled_elements]:
                el_roll = None

            if el_roll is None:
                print(f"NO ELEMENT ROLLED! {dice_roll}")
            elif type(el_roll) == Fusion:
                d8 = Dice.from_string('1d8')

                while True:
                    roll_1 = d8.roll(f"Roll on Elemental Fusion Table(1/2)")
                    roll_2 = d8.roll(f"Roll on Elemental Fusion Table(2/2)")
                    # TODO: Handle 'Special' columns
                    if roll_1 != 8 and roll_1 != roll_2:
                        fusion_el = fusion_table[roll_1][roll_2]

                        if fusion_el is not None and fusion_el != 'special':
                            if fusion_el is not None:
                                fusion_el.bonus = el_roll.bonus
                                self.elements.append(fusion_el)
                                break
            else:
                self.elements.append(el_roll)

            roll_for_element = False


        # If Originally Manufactured by Eridian. Apply Eridian Effects afterwards
        if self.eridian:
            self.manufacturer = Manufacturers.ERIDIAN
            self.manufacturer.gun_part_exception(self)

        # Randomly choose a name
        self.randomize_name()

    def set_manufacturer(self, new_manufacturer):
        # Remove old manufacturer traits
        if self.manufacturer is not None:
            for old_trait in self.manufacturer.weapon_traits['primary'] + self.manufacturer.weapon_traits['secondary']:
                self.remove_property(old_trait)

        # Set new manufacturer
        self.manufacturer = new_manufacturer

        # Load new manufacturer traits
        # Primary weapon traits
        for trait in self.manufacturer.weapon_traits['primary']:
            self.add_property(trait)

        # Secondary weapon trait
        trait = self.manufacturer.pick_secondary_weapon_trait()
        if trait:
            self.add_property(trait)

    def randomize_name(self):
        with open('assets.json') as file:
            asset_data = json.load(file)

        self.asset = random.choice(asset_data['weapons'][self.gun_type.asset_dir])
        self.name_raw = self.asset['item_name']

    def pick_weapon_accessory(self):
        d100 = Dice.from_string('1d100')
        roll = d100.roll(f"Roll for Gun Accessory")
        part = lookup_in_table(weapon_accessories_table, roll)

        return part

    def pick_weapon_scope(self):
        part = None
        d100 = Dice.from_string('1d100')

        retries_left = 50
        while retries_left > 0:
            roll = d100.roll(f"Roll for Gun Scope")
            part = lookup_in_table(weapon_sight_table, roll)
            # Check if part already present
            for property in self.equipment_properties:
                if isinstance(part, type(property)):
                    print(f"Rolled a {roll}! But the part <{part.name}> is already equipped. Roll again...")
                    part = None
                    retries_left -= 1
                    break

            if part is not None:
                print(f"Rolled a {roll}! Adding Gun Scope <{part.name}>!")
                break

        assert part is not None, f"Failed to roll for a Weapon Scope...\n{self}"

        return part

    @property
    def gun_type(self):
        return self._gun_type

    @gun_type.setter
    def gun_type(self, new_type):
        for old_trait in self._gun_type.weapon_bonus:
            self.remove_property(old_trait)

        for new_trait in new_type.weapon_bonus:
            self.add_property(new_trait)

        self._gun_type = new_type

    @property
    def mag_size(self):
        mag_size = self.base_stats['mag_size'] + self.get_modifier_value(mod_mag_size)

        # Magazine size cannot go below 1
        if mag_size < 1:
            mag_size = 1

        return mag_size

    @property
    def range(self):
        return self.base_stats['range'] + self.get_modifier_value(mod_range)

    @property
    def max_parts(self):
        return weapon_part_count[self.rarity] + self.get_modifier_value(mod_maximum_parts)

    @property
    def n_scopes(self):
        scope_cnt = 0
        for property in self.equipment_properties:
            if isinstance(property, WeaponPartScope):
                scope_cnt += 1

        return scope_cnt

    @property
    def hits_crits(self):
        # Load base stats
        stats = deepcopy(self.base_stats['hits_crits'])

        # Apply Modifiers to stats
        burst_value = self.get_modifier_value(mod_burst)
        for atk in ['glance', 'solid', 'penetrate']:
            stats[atk]['hits'] += burst_value

        stats['penetrate']['crits'] += self.get_modifier_value(mod_penetrate_crits)

        # Clamp values
        # Hits & Crits cannot be lowered below 1 (if Gun basestats were non-zero)
        for atk in ['glance', 'solid', 'penetrate']:
            if stats[atk]['hits'] < 1 and self.base_stats['hits_crits'][atk]['hits'] != 0:
                stats[atk]['hits'] = 1

            if stats[atk]['crits'] < 1 and self.base_stats['hits_crits'][atk]['crits'] != 0:
                stats[atk]['crits'] = 1

        return stats


    def generate_card(self):
        generate_gun_card(self)


    def  __repr__(self):
        str = ''
        str += f"--- Generated Gun --- \n"
        str += f"Name: <{self.name}> \n"
        str += f"Type: (Lv.{self.level}) {self.rarity} {self.gun_type}\n"
        str += f"Manufacturer: {self.manufacturer}\n"
        str += f"n Gun Parts: {self.n_parts}\n"
        str += f"n Gun Scope: {self.n_scopes}\n"

        str += f"Elements: \n"
        if self.forced_elemental or not self.forced_non_elemental:
            for el in self.elements:
                str += f" - {el}\n"
        str += f"\n"

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
            str += f" - {bonus.effect}\n"
        str += f"\n"

        # Print Weapon Traits
        str += f"Traits:\n"
        for trait in self.equipment_properties:
            if isinstance(trait, WeaponTrait):
                str += f" - {trait.name} - {trait.effect}\n"
        str += f"\n"

        # Print Weapon Parts
        str += f"Parts:\n"
        for part in self.equipment_properties:
            if isinstance(part, WeaponPart):
                str += f" - {part.name}: {part.effect}\n"
        str += f"\n"

        # Mods & Checks
        str += f"Mods & Checks:\n"
        for mod in self.equipment_modifiers:
            effect = mod.effect
            if mod.hidden:
                effect = f"({mod.effect})"
            elif mod.situational:
                effect = f"[{mod.effect}]"

            str += f" - {effect}\n"

        return str
