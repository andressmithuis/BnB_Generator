import random
from copy import deepcopy

import json

from util import Dice, roll_on_table

from .bnb_tables import *
from .bnb_guntypes import Guntypes
from .cards.bnb_gun_card import generate_gun_card
from util.gun_prefixes import prefix_crappy

class Gun:
    def __init__(self):
        self.type = Guntypes.PISTOL
        self.guild = None
        self.rarity = Rarity.COMMON
        self.level = 1
        self.element_roll_bonus = 0
        self.elements = []
        self.modifiers = []
        self.effects = []

        self.base_stats = {
            'hit_dice': Dice.from_string('1d4'),
            'hits_crits': {
                'glance': {'hits': 0, 'crits': 0},
                'solid': {'hits': 0, 'crits': 0},
                'penetrate': {'hits': 0, 'crits': 0}
            },
            'range': 0,
            'mag_size': 0
        }
        self.mod_stats = deepcopy(self.base_stats)

        self.range = 0
        self.hit_dice = Dice.from_string('1d4')
        self.hits_crits = self.base_stats['hits_crits']

        self.forced_elemental = False
        self.forced_non_elemental = False

        self.asset = {'item_id': '', 'item_name': '', 'path_to_img': ''}
        self.name = 'The Placeholder'
        self.name_prefix = None

    def generate(self, level: int = 1, input_rolls=False, starting=False, props=None):
        # Random gun - page 80
        # ---
        # Roll 2d8 to determine the type of gun (row) and manufacturer (col) - page 81
        #   - Select a Favored Gun if applicable
        # Roll 1d4 and 1d6 to determine rarity and element roll - page 81
        # Fill in gun stats based on VH lvl  - pages 90 - 92
        # Fill in guild bonuses - pages 93 - 98
        #   - If elemental, roll % on elemental table - page 82 (Alas! and Blackpowder NEVER, Malafactor ALWAYS)
        # Optional: Add Prefix
        #   - If Epic or Legendary: Optional: Add Red Text

        if starting is False:
            if 0 < level <= 30:
                self.level = level

            # Gun Type / Guild Type
            rolls = Dice.from_string('2d8').roll_dice(user=input_rolls)

            #_row = gun_table[d8_1-1]
            result = gun_table_v2[rolls[0]] # Gun Table fix

            self.type = result[0]
            if self.type == 'rolled_a_7':
                self.type = rolled_a_7[rolls[1]]
            self.guild = result[1][rolls[1]]

            print(f"Rolled a {rolls[0]}(1d8) and {rolls[1]}(1d8) -> Gun: {self.type}, Guild: {self.guild}")
        else:
            self.level = 1
            self.type = 'favored'
            self.guild = 'choice'
            input_rolls = True

        self.type = 'favored'

        # Favored Gun / Guild Choice check
        if self.type == 'favored':
            if input_rolls:
                self.type = ask_for_favored_gun()
            else:
                self.type = random.choice([Guntypes.PISTOL, Guntypes.SMG, Guntypes.RIFLE, Guntypes.SHOTGUN, Guntypes.SNIPER, Guntypes.LAUNCHER])

            print(f"Chosen favored gun: {self.type}")

        if self.guild == 'choice':
            if input_rolls:
                self.guild = ask_for_guild(self.type)
            else:
                self.guild = random.choice(guilds_per_weapon[self.type])

            print(f"Chosen guild: {self.guild}")

        # Set Gun Base Stats
        self.base_stats = self.type.get_basestats(self.level)
        self.mod_stats = deepcopy(self.base_stats)

        # Rarity and Elemental Roll
        if starting is False:
            d4 = Dice.from_string('1d4').roll(input_rolls)
            d6 = Dice.from_string('1d6').roll(input_rolls)

            self.rarity, roll_for_element = rarity_table[d4][d6]
            print(f"Rolled a {d4}(1d4) and {d6}(1d6) -> Rarity: {self.rarity}, Elemental: {roll_for_element}")
        else:
            self.rarity = Rarity.COMMON
            roll_for_element = False

        # Add Weapon Type Bonus Effects
        for weapon_bonus in self.type.weapon_bonus:
            if type(weapon_bonus) not in [type(ef) for ef in self.effects]:
                self.effects.append(weapon_bonus)

        # Add Guild Bonus Effects
        self.guild.apply_weapon_bonus(self)

        # Elemental Roll Checks
        if self.forced_elemental is True:
            roll_for_element = True
        elif self.forced_non_elemental is True:
            roll_for_element = False

        # Roll for Element
        if roll_for_element:
            d100 = Dice.from_string('1d100').roll(input_rolls)
            d100_res = min([d100 + self.element_roll_bonus, 100])

            print(f"Element roll result: {d100_res} ({d100} [Roll] + {self.element_roll_bonus} [Bonus])")

            elements = roll_on_table(elemental_table, d100_res)[self.rarity]
            for el in elements:
                self.elements.append(el)

        # Gun Name Prefix
        if starting:
            # 'Crappy' Starting guns get a -2 DMG Mod
            self.name_prefix = prefix_crappy()
        else:
            d10 = Dice.from_string('1d10').roll(input_rolls)

            if False:
            #if d10 >= prefix_threshold[self.rarity]:
                d100 = Dice.from_string('1d100').roll(input_rolls)
                #d100 = (d100 % len(gun_prefixes)) + 1  # TODO: Remove when Gun prefixes table is completed

        if self.name_prefix is not None:
            self.name_prefix.apply(self)

        # Calculate Final Gun Stats
        self.range = self.mod_stats['range']
        self.hit_dice = self.mod_stats['hit_dice']
        self.hits_crits = self.mod_stats['hits_crits']

        # Randomly choose a name
        self.randomize_name()

    def randomize_name(self):
        with open('assets.json') as file:
            asset_data = json.load(file)

        self.asset = random.choice(asset_data['weapons'][self.type.asset_dir])
        self.name = self.asset['item_name']

    def generate_card(self):
        generate_gun_card(self)

    def __repr__(self):
        str = '\n\n'
        str += f"--- Generated Gun --- \n"
        gun_name = f"{self.name}"
        if self.name_prefix is not None:
            gun_name = f"{self.name_prefix.name} {self.name}"
        str += f"Name: <{gun_name}> (Lv.{self.level})\n"
        str += f"Type: {self.rarity} {self.type} ({self.guild})\n"

        str += f"Elements: "
        for el in self.elements:
            str += f"{el.name} "
        str += f"\n"

        str += f"Range: {self.range}\n"
        str += f"Accuracy:\n"
        for atk in ['2-7 ', '8-15', '16+ ']:
            _atk = atk.strip()
            str += f" - {atk}: {self.hits_crits[_atk]['hits']} Hits, {self.hits_crits[_atk]['crits']} Crits\n"

        str += f"Damage: {self.hit_dice}\n"
        str += f"\n"

        str += f"Weapon Effects:\n"
        for effect in self.effects:
            str += f" - {effect}\n"
        str += f"\n"

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


def ask_for_favored_gun():
    gun_selected = 'favored'

    while gun_selected == 'favored':
        gun_list = [Guntypes.PISTOL, Guntypes.SMG, Guntypes.RIFLE, Guntypes.SHOTGUN, Guntypes.SNIPER, Guntypes.LAUNCHER]

        print()
        print(f"Please select your Favored Gun:")
        idx = 0
        for guntype in gun_list:
            print(f"{idx} - {guntype}")

        inp = input("Number selected: ")
        try:
            sel = int(inp)

            if 0 <= sel <= len(gun_list):
                gun_selected = gun_list[idx]
                print(f"Selected {gun_selected}")
                return gun_selected
            else:
                print(f"Given number {sel} is not in the list!")
        except ValueError:
            print(f"Given input <{inp}> is not a number!")

def ask_for_guild(gun_type: Guntypes):
    guild_selected = 'choice'

    while guild_selected == 'choice':
        print()
        print(f"Please select your guild of choice:")

        idx = 0
        for guild in guilds_per_weapon[gun_type]:
            #print(f"{guild.value} - {guild}: {guild.gun_info()}")
            # TODO: Rework!
            print(f"{idx} - {guild}")
            idx += 1

        inp = input("Number selected: ")
        try:
            sel = int(inp)

            if 0 <= sel <= len(guilds_per_weapon[gun_type]):
                guild_selected = guilds_per_weapon[gun_type][sel]
                print(f"Selected {guild_selected}")
                return guild_selected
            else:
                print(f"Given number {sel} is not in the list!")
        except ValueError:
            print(f"Given input <{inp}> is not a number!")

if __name__ == '__main__':
    new_gun = Gun()
    new_gun.generate(input_rolls=True)
    print(new_gun)
