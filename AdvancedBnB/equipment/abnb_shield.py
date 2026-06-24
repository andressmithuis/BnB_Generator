import json
import random
from copy import deepcopy

from AdvancedBnB.abnb_equipment import AbnbEquipment
from AdvancedBnB.abnb_tables import rarity_tables, shield_part_count
from AdvancedBnB.abnb_util import get_item_tier
from AdvancedBnB.shield.abnb_shield_card import generate_shield_card
from AdvancedBnB import FusionElement
from AdvancedBnB.abnb_manufacturers import Manufacturers, manufacturer_table
from util import Dice, lookup_in_table
from util.common_modifiers import *

from AdvancedBnB.shield.abnb_shieldtypes import Shieldtypes
from AdvancedBnB.shield.abnb_shield_parts import ShieldPart, shield_parts_table, shd_part_resistant, shd_part_spike, shd_part_nova
from AdvancedBnB.shield.abnb_shield_modifiers import mod_capacity, mod_shield_regen


def mod_to_string(val_1, val_2):
    delta = val_1 - val_2
    if delta != 0:
        return f"({'+' if delta > 0 else ''}{delta})"

    return ''

class Shield(AbnbEquipment):
    def __init__(self):
        super().__init__()

        self.shield_type = Shieldtypes.FAST
        self.tag = None

        self.base_stats = {
            'capacity': 0,
            'charge_rate': 0
        }

        self.max_parts = 0

    def generate(self):
        # Prepare dice
        d100 = Dice(1, 100)
        d4 = Dice(1, 4)
        d6 = Dice(1, 6)
        d12 = Dice(1, 12)

        # Determine level and tier
        self.tier = get_item_tier(self.level)

        # Manufacturer and shield type
        print(f"Determining Shield Manufacturer...")

        while self.manufacturer is None:
            roll = d12.roll()
            new_manufacturer = manufacturer_table[roll]
            print(f"Rolled a {roll}! Shield Manufacturer = {new_manufacturer}")
            if new_manufacturer == Manufacturers.ERIDIAN:
                print(f"Rolled Eridian Manufacturer. Roll again for Manufacturer of Shield Base.")
                self.eridian = True
                self.manufacturer = None
            else:
                self.set_manufacturer(new_manufacturer)

        print(f"Shield Type = {self.shield_type}")
        print(f"Shield Tag = {self.tag}")

        for property in self.equipment_properties:
            print(f"Starting Part: {property.name} - {property.effect}")

        # Shield base stats
        self.base_stats = self.shield_type.get_basestats(self.tier)
        print(self.base_stats)

        # Rarity and element
        print(f"Determining Shield Rarity and Element...")
        d4_roll = d4.roll()
        d6_roll = d6.roll()
        self.rarity, roll_for_element = rarity_tables['normal'][d4_roll][d6_roll]

        # Roll for Element(s)
        # Determine number of Elemental Rolls
        elemental_rolls = 0
        if roll_for_element is True:
            elemental_rolls = 1

        if self.has_modifier(mod_elemental_roll_number):
            elemental_rolls = self.get_modifier_value(mod_elemental_roll_number)

        self.roll_for_elements(elemental_rolls)
        # If the Shield is now Elemental, add a matching Resistant part
        if len(self.elements) > 0:
            self.add_resistant_parts()

        print(f"Rolled a {d4_roll}(d4) and a {d6_roll}(d6)! Shield Rarity = {self.rarity}, Element = {[el for el in self.elements]}")

        # Roll for Shield parts
        print(f"Determining Shield Parts...")
        self.max_parts = shield_part_count[self.rarity]
        self.n_parts = 0

        # Roll for remaining parts
        # NOTE: Shields CAN have multiples of the same part. Shield effects denote this by the '/P'.
        while self.n_parts < self.max_parts:
            print(f"Rolling for part {self.n_parts+1}/{self.max_parts}...")
            roll = d100.roll()
            part = lookup_in_table(shield_parts_table, roll)
            new_part = deepcopy(part)

            # Elemental part exceptions (Resistant, Nova, Spike)
            if isinstance(new_part, (shd_part_resistant, shd_part_spike, shd_part_nova)):
                # Reroll if Shield has to be Non-Elemental
                if self.forced_non_elemental:
                    print(f"Rolled a <{new_part.name}> part, but the Shield is forced Non-Elemental... Roll again...")
                    continue

                # Force an element if the Shield is not elemental yet
                while len(self.elements) == 0:
                    print(f"Rolled a <{new_part.name}> part, but the Shield is not yet Elemental...")
                    self.roll_for_elements(1)
                    # If the Shield is now Elemental, add a matching Resistant part(unless the new part is a Resistant part, which will be added a bit later anyway)
                    if not isinstance(new_part, shd_part_resistant):
                        if len(self.elements) > 0:
                            self.add_resistant_parts()

            if isinstance(new_part, shd_part_resistant):
                # Add Resistant part
                self.add_resistant_parts()
            else:
                # Add regular part
                print(f"Adding part: {new_part.name} - {new_part.effect}")
                new_part.attach(self)

            self.n_parts += 1


        # If Originally Manufactured by Eridian, apply Eridian Shield Effects
        if self.eridian:
            self.manufacturer = Manufacturers.ERIDIAN
            eridian_traits = Manufacturers.ERIDIAN.shield_traits['parts']
            for trait in eridian_traits:
                trait.attach(self)

        # Randomly choose a name
        self.randomize_name()

    def set_manufacturer(self, new_manufacturer):
        self.shield_type, self.tag, parts = new_manufacturer.make_random_shield()
        for part in parts:
            part.attach(self)

        self.manufacturer = new_manufacturer

    def add_resistant_parts(self):
        el = []
        if len(self.elements) > 0:
            for element in self.elements:
                if isinstance(element, FusionElement):
                    for sub_element in element.fusion_elements:
                        for i in range(element.bonus + 1):
                            el.append(sub_element)

                else:
                    el.append(element)

        for element in el:
            for i in range(element.bonus + 1):
                new_part = shd_part_resistant()
                new_part.type = element.name
                new_part.attach(self)
                print(f"Adding part: {new_part.name} - {new_part.effect}")

    def randomize_name(self):
        with open('assets.json') as file:
            asset_data = json.load(file)

        self.asset = random.choice(asset_data['shields'])
        self.name_raw = self.asset['item_name']

    def generate_card(self):
        generate_shield_card(self)

    @property
    def capacity(self):
        return self.base_stats['capacity'] + self.get_modifier_value(mod_capacity)

    @property
    def recharge_rate(self):
        return self.base_stats['charge_rate'] + self.get_modifier_value(mod_shield_regen)

    def  __repr__(self):
        str = ''
        str += f"--- Generated Shield --- \n"
        str += f"Name: <{self.name}> \n"
        str += f"Type: (Lv.{self.level}) {self.rarity} {self.shield_type} Shield\n"
        str += f"Tag: {self.tag.name}\n"
        str += f"Manufacturer: {self.manufacturer}\n"
        str += f"n Parts: {self.max_parts}\n"

        str += f"Elements: "
        if self.forced_elemental or not self.forced_non_elemental:
            for el in self.elements:
                str += f"{el} "
        str += f"\n\n"

        mod_str = mod_to_string(self.capacity, self.base_stats['capacity'])
        str += f"Capacity: {self.capacity}{mod_str}\n"
        mod_str = mod_to_string(self.recharge_rate, self.base_stats['charge_rate'])
        str += f"Recharge Rate: {self.recharge_rate}{mod_str}\n"
        str += f"\n\n"

        # Print Shield Parts
        str += f"Parts:\n"
        for part in self.equipment_properties:
            if isinstance(part, ShieldPart):
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
        str += f"\n"

        # Print Shield Parts
        str += f"All Properties:\n"
        for part in self.equipment_properties:
            str += f" - {part.name}: {part.effect}\n"
        str += f"\n"

        return str




