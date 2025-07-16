import json
import random
from copy import deepcopy

from AdvancedBnB.abnb_tables import *
from AdvancedBnB.abnb_util import get_item_tier
from AdvancedBnB.class_mod.abnb_classes import class_mods_per_class
from util import Dice, lookup_in_table

from AdvancedBnB.class_mod import classes_table, generate_class_mod_card


def mod_to_string(val_1, val_2):
    delta = val_1 - val_2
    if delta != 0:
        return f"({'+' if delta > 0 else ''}{delta})"

    return ''

class ClassMod:
    def __init__(self):
        self.name = ''
        self.name_prefix = ''
        self.level = 1
        self.tier = 1
        self.rarity = Rarity.COMMON

        self.vh_class = ''
        self.type = None
        self.passive_effect = None
        self.legendary_effect = None
        self.manufacturer = None

        self.skills = {}

        self.elements = []

        self.user_rolls = False

    def generate(self, user_rolls=False, props=None):
        self.user_rolls = user_rolls

        # Choose a name / img
        self.randomize_name()

        # Determine level and tier
        if props is not None and 'item_level' in props:
            self.level = props['item_level']
        self.tier = get_item_tier(self.level)

        # Rarity
        print(f"Determining Class Mod Rarity...")
        while True:
            d4_roll = Dice.from_string('1d4').roll(self.user_rolls)
            d6_roll = Dice.from_string('1d6').roll(self.user_rolls)
            self.rarity, _ = rarity_tables['normal'][d4_roll][d6_roll]

            if self.rarity not in [Rarity.LEGENDARY, Rarity.PEARLESCENT]:
                break

            if self.rarity == Rarity.LEGENDARY and self.tier > 2:
                break

        if props is not None and 'rarity' in props:
            self.rarity = props['rarity']

        print(f"Rolled a {d4_roll}(d4) and a {d6_roll}(d6)! Class Mod Rarity = {self.rarity}")

        # Collect valid classes for Class Mod
        if 'class_mod_classes' in props:
            possible_classes = {}
            for i in range(len(props['class_mod_classes'])):
                possible_classes.update({i+1: props['class_mod_classes'][i]})
        else:
            possible_classes = classes_table

        # Roll for Vault Hunter Class
        dice = Dice.best_dice_for_table(possible_classes)

        roll = 100
        while roll > len(possible_classes):
            roll = dice.roll()

        self.vh_class = lookup_in_table(possible_classes, roll)

        # Roll for Class Mod from picked Vault Hunter Class
        self.type = deepcopy(lookup_in_table(class_mods_per_class[self.vh_class],Dice.from_string('1d12').roll()))

        # Load Class Mod Traits
        self.type.create(self)

        if props is not None and 'item_name' in props:
            self.name = props['item_name']

    def add_skill(self, skill, count=1):
        self.skills.setdefault(skill, 0)
        self.skills[skill] += count

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
        generate_class_mod_card(self)

    def  __repr__(self):
        str = ''
        str += f"--- Generated Class Mod --- \n"
        str += f"Name: <{self.name_prefix + ' ' if self.name_prefix != '' else ''}{self.name}> \n"
        str += f"Type: (Lv.{self.level}) {self.rarity} {self.type.name} Class Mod ({self.vh_class})\n"
        str += f"Manufacturer: {self.manufacturer}\n"
        str += f"\n\n"

        # Passive Effect
        str += f"-- Passive Effect -- \n"
        str += f"{self.passive_effect.to_text(self)}\n"
        str += f"\n\n"

        # Skill Bonusses
        str += f"-- Skill Bonusses -- \n"
        for skill, count in self.skills.items():
            str += f"- {skill} +{count}\n"
        str += f"\n\n"

        # Legendary Effect
        if self.legendary_effect is not None:
            str += f"-- Legendary Effect -- \n"
            str += f"{self.legendary_effect.name} - {self.legendary_effect.to_text(self)}\n"
            str += f"\n\n"

        return str




