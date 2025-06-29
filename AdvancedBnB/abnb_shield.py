import json
import random
from copy import deepcopy

from .abnb_tables import *
from .abnb_util import get_item_tier
from .abnb_shield_parts import shield_parts_table, shd_part_resistant
from .cards.abnb_shield_card import generate_shield_card

def mod_to_string(val_1, val_2):
    delta = val_1 - val_2
    if delta != 0:
        return f"({'+' if delta > 0 else ''}{delta})"

    return ''

class Shield:
    def __init__(self):
        self.name = ''
        self.name_prefix = ''
        self.level = 1
        self.tier = 1
        self.rarity = Rarity.COMMON

        self.manufacturer = None
        self.eridian = False
        self.shield_type = Shieldtypes.FAST
        self.tag = 'Energy'

        self.capacity = 0
        self.recharge_rate = 0
        self.base_stats = {
            'capacity': 0,
            'charge_rate': 0
        }
        self.mod_stats = deepcopy(self.base_stats)

        self.parts = []
        self.n_parts = 0
        self.max_parts = 0

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

        # Manufacturer and shield type
        print(f"Determining Shield Manufacturer...")
        if props is not None and 'manufacturer' in props:
            self.manufacturer = props['manufacturer']
            if self.manufacturer == Manufacturers.ERIDIAN:
                print("MANUFACTURER == ERIDIAN")
                self.eridian = True
                self.manufacturer = None

        while self.manufacturer is None:
            roll = d12.roll(self.user_rolls)
            self.manufacturer = manufacturer_table[roll]
            print(f"Rolled a {roll}! Shield Manufacturer = {self.manufacturer}")
            if self.manufacturer == Manufacturers.ERIDIAN:
                print(f"Rolled Eridian Manufacturer. Roll again for Manufacturer of Shield Base.")
                self.eridian = True
                self.manufacturer = None

        # Apply Manufacturer Shield Traits
        print(f"Applying Manufacturer Traits...")
        self.manufacturer.edit_shield(self)

        if props is not None and 'shield_type' in props:
            self.shield_type = props['shield_type']
        print(f"Shield Type = {self.shield_type}")
        print(f"Shield Tag = {self.tag}")

        for part in self.parts:
            print(f"Starting Part: {part.name} - {part.effect}")

        # Shield base stats
        self.base_stats = self.shield_type.get_basestats(self.tier)
        self.mod_stats = deepcopy(self.base_stats)

        # Rarity and element
        print(f"Determining Shield Rarity and Element...")
        d4_roll = d4.roll(self.user_rolls)
        d6_roll = d6.roll(self.user_rolls)
        self.rarity, roll_for_element = rarity_tables['normal'][d4_roll][d6_roll]

        if props is not None and 'rarity' in props:
            self.rarity = props['rarity']

        if roll_for_element:
            self.elemental_roll['n_rolls'] = 1
            self.roll_for_element()

        print(f"Rolled a {d4_roll}(d4) and a {d6_roll}(d6)! Shield Rarity = {self.rarity}, Element = {[el for el in self.elements]}")

        # If Shield is Elemental, add Resistance part
        if len(self.elements) > 0:
            self.add_resistance_part()

        # Roll for Shield parts
        print(f"Determining Shield Parts...")
        self.max_parts = shield_part_count[self.rarity]
        self.n_parts = 0

        # Roll for remaining parts
        # NOTE: Shields CAN have multiples of the same part. Shield effects denote this by the '/P'.
        while self.n_parts < self.max_parts:
            print(f"Rolling for part {self.n_parts+1}/{self.max_parts}...")
            roll = d100.roll(self.user_rolls)
            part = roll_on_table(shield_parts_table, roll)
            new_part = deepcopy(part)

            # Elemental part exceptions (Resistant, Nova, Spike)
            if new_part.name in ['Resistant', 'Spike', 'Nova']:
                # Force an element if item is not elemental
                if len(self.elements) == 0:
                    self.forced_elemental = True
                    self.roll_for_element()

            if new_part.name == 'Resistant':
                self.add_resistance_part()
                self.n_parts += 1
            else:
                print(f"Adding part: {new_part.name} - {new_part.effect}")
                self.parts.append(new_part)
                self.n_parts += 1

        # Apply Shield Part Effects
        self.apply_effects()

        # Calculate final stats
        self.calculate_stats()

        # If Originally Manufactured by Eridian, apply Eridian Shield Effects
        # NOTE: Needs to have the final stats calculated
        if self.eridian:
            self.manufacturer = Manufacturers.ERIDIAN
            eridian_traits = [shd_trait_reverse_engineer(), shd_trait_symbiotic()]
            for trait in eridian_traits:
                self.parts.append(trait)
                trait.apply(self)

        # Pick random Shield Name
        self.randomize_name()

    def roll_for_element(self):
        d100 = Dice.from_string('1d100')

        # Check if Forced Elemental
        if self.forced_elemental and self.elemental_roll['n_rolls'] == 0:
            self.elemental_roll['n_rolls'] = 1

        # Check if Forced Non-Elemental
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

    def add_resistance_part(self):
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
            new_part = shd_part_resistant()
            new_part.name = f"Resistant ({element.name})"
            new_part.type = element.name
            for i in range(element.bonus + 1):
                self.parts.append(new_part)
                print(f"Adding part: {new_part.name} - {new_part.effect}")

    def apply_effects(self):
        # Create deduplicated list of parts
        dedup_parts = []
        for part in self.parts:
            if part.name not in [x.name for x in dedup_parts]:
                dedup_parts.append(part)

        # Apply Part Effects
        # NOTE: part.apply() will check for number of similar parts for the /P calculations
        for part in dedup_parts:
            part.apply(self)

    def calculate_stats(self):
        # Extract final stats
        self.capacity = self.mod_stats['capacity']
        self.recharge_rate = self.mod_stats['charge_rate']

    def randomize_name(self):
        with open('assets.json') as file:
            asset_data = json.load(file)

        self.asset = random.choice(asset_data['shields'])
        self.name = self.asset['item_name']

    def generate_card(self):
        generate_shield_card(self)


    def  __repr__(self):
        str = ''
        str += f"--- Generated Shield --- \n"
        str += f"Name: <{self.name_prefix + ' ' if self.name_prefix != '' else ''}{self.name}> \n"
        str += f"Type: (Lv.{self.level}) {self.rarity} {self.shield_type} Shield\n"
        str += f"Tag: {self.tag}\n"
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
                str += f" - {k} {'+' if v != 0 else ''}{v} \n"

        return str




