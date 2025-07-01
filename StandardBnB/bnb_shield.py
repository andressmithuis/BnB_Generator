import json
import random
from copy import deepcopy

from util import Rarity, Dice, roll_on_table
from .bnb_guilds import Guilds
from .bnb_tables import shield_guild_table, rarity_table
from .cards.bnb_shield_card import generate_shield_card


class Shield:
    def __init__(self):
        self.guild = None
        self.rarity = Rarity.COMMON
        self.elements = []
        self.level = 1

        self.base_stats = {
            'capacity': 0,
            'charge_rate': 0
        }
        self.mod_stats = deepcopy(self.base_stats)

        self.capacity = 0
        self.recharge_rate = 0

        self.effects = []

        self.name_prefix = ''
        self.name = ''
        self.asset = {'item_id': '', 'item_name': '', 'path_to_img': ''}



    def generate(self, input_rolls=False, props=None):
        '''
        Roll d6 for guild
        Based on level and guild, select capacity and recharge rate
        Add guild bonus to base stats?
        roll d4 and d6 for rarity (table pg. 81)
        roll a d6 for element -> Only activates by specific mods!
        roll d100 for n Mods
        - For each mod, roll guild shield mod table
        - - How to deal with elements?
        '''

        if props is not None and 'item_level' in props:
            if 1 <= props['item_level'] <= 30:
                self.level = props['item_level']

        # Guild type
        d8 = Dice.from_string('1d8').roll(input_rolls)
        self.guild = shield_guild_table[d8]

        print(f"Rolled a {d8}(1d8) -> Guild: {self.guild}")

        # Guild Basestats
        self.guild.make_shield(self)

        # Rarity
        d4 = Dice.from_string('1d4').roll(input_rolls)
        d6 = Dice.from_string('1d6').roll(input_rolls)

        self.rarity, _ = rarity_table[d4][d6]
        print(f"Rolled a {d4}(1d4) and {d6}(1d6) -> Rarity: {self.rarity}")

        # Apply Shield Effects
        for effect in self.effects:
            effect.apply(self)

        # Element
        # TODO: check if needed
        if False:
            roll = Dice.from_string('1d100').roll(input_rolls)
            self.element = roll_on_table(elemental_table, roll)[d6]
            print(f"Rolled a {roll}(1d100) -> Element: {self.element.to_str()}")

        # Calculate Final Stats
        self.capacity = self.mod_stats['capacity']
        self.recharge_rate = self.mod_stats['charge_rate']

        # Randomly choose a name
        self.randomize_name()
        if props is not None and 'item_name' in props:
            self.name = props['item_name']

    def randomize_name(self):
        with open('assets.json') as file:
            asset_data = json.load(file)

        self.asset = random.choice(asset_data['shields'])
        self.name = self.asset['item_name']

    def generate_card(self):
        generate_shield_card(self)

    def __repr__(self):
        str = '\n\n'
        str += f"--- Generated Shield --- \n"
        str += f"Name: <{self.name}> (Lv.{self.level})\n"
        str += f"Type: {self.rarity} {self.guild} Shield\n"

        str += f"Stats:\n"
        str += f" - Capacity: {self.capacity}\n"
        str += f" - Recharge Rate: {self.recharge_rate}\n"

        str += f"Effects:\n"
        for ef in self.effects:
            str += f" - {ef.name}: {ef.to_text(self)}\n"
        str += "\n"

        return str



