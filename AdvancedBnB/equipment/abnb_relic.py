import json
import random

from AdvancedBnB.abnb_tables import *
from AdvancedBnB.abnb_util import get_item_tier
from util import Dice, roll_on_table

from AdvancedBnB.relic import Relictypes, basic_relics_table, advanced_relics_table, generate_relic_card


def mod_to_string(val_1, val_2):
    delta = val_1 - val_2
    if delta != 0:
        return f"({'+' if delta > 0 else ''}{delta})"

    return ''

class Relic:
    def __init__(self):
        self.name = ''
        self.name_prefix = ''
        self.level = 1
        self.tier = 1
        self.rarity = Rarity.COMMON

        self.type = None
        self.manufacturer = None

        self.elements = []

        self.mod_stats = {}

        self.max_parts = 0
        self.parts = []

        self.user_rolls = False

    def generate(self, user_rolls=False, props=None):
        self.user_rolls = user_rolls

        # Determine level and tier
        if props is not None and 'item_level' in props:
            self.level = props['item_level']
        self.tier = get_item_tier(self.level)

        # Rarity and element
        print(f"Determining Relic Rarity...")
        d4_roll = Dice.from_string('1d4').roll(self.user_rolls)
        d6_roll = Dice.from_string('1d6').roll(self.user_rolls)
        self.rarity, _ = rarity_tables['normal'][d4_roll][d6_roll]

        if props is not None and 'rarity' in props:
            self.rarity = props['rarity']

        print(f"Rolled a {d4_roll}(d4) and a {d6_roll}(d6)! Relic Rarity = {self.rarity}")

        # Determine Relic Type (Uncommon ~ Rare = Basic Relic, Epic+ = Advanced Relic)
        if self.rarity in [Rarity.COMMON, Rarity.UNCOMMON, Rarity.RARE]:
            self.type = basic_relics_table[Dice.from_string('1d10').roll()]
        else:
            self.type = roll_on_table(advanced_relics_table, Dice.from_string('1d10').roll())

        # Manufacturer
        print(f"Determining Relic Manufacturer...")
        self.manufacturer = self.type.pick_manufacturer()

        if props is not None and 'manufacturer' in props:
            self.manufacturer = props['manufacturer']

        # Roll for Relic parts
        print(f"Determining Relic Parts...")
        self.max_parts = relic_part_count[self.rarity]
        self.parts = self.type.roll_parts(self.tier, self.max_parts)

        # Apply Relic Part Effects
        self.apply_effects()

        # Randomly choose a name
        self.randomize_name()
        if props is not None and 'item_name' in props:
            self.name = props['item_name']

    def apply_effects(self):
        # Create deduplicated list of parts
        dedup_parts = []
        for part in self.parts:
            if part not in dedup_parts:
                dedup_parts.append(part)

        # Apply Part Effects
        for part in dedup_parts:
            part.apply(self)

    def randomize_name(self):
        with open('assets.json') as file:
            asset_data = json.load(file)

        self.asset = random.choice(asset_data['relics'])
        self.name = self.asset['item_name']

    def generate_card(self):
        generate_relic_card(self)

    def  __repr__(self):
        str = ''
        str += f"--- Generated Relic --- \n"
        str += f"Name: <{self.name_prefix + ' ' if self.name_prefix != '' else ''}{self.name}> \n"
        str += f"Type: (Lv.{self.level}) {self.rarity} {self.type.name} Relic\n"
        str += f"Manufacturer: {self.manufacturer}\n"
        str += f"\n\n"

        # Print Relic Parts
        str += f"Parts[{self.max_parts}]:\n"
        for part in self.parts:
            str += f" - {part.name}: {part.to_text(self)}\n"
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




