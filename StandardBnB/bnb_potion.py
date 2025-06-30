from util.rarity import Rarity
from util.dice import Dice
from .cards.bnb_potion_card import generate_potion_card

'''
Health and Shield Gains:

Common - 1d8
Uncommon - 1d8 + 5
Rare - 2d8 + 5
Epic - 3d8 + 10
Legendary - 4d8 + 20
'''

class Potion:
    name = 'Unknown'

    def generate_card(self):
        generate_potion_card(self)


class HealthPotion(Potion):
    name = 'Health Potion'

    variants = {
        Rarity.COMMON: {'dice': Dice.from_string('1d8'), 'bonus': 0},
        Rarity.UNCOMMON: {'dice': Dice.from_string('1d8'), 'bonus': 5},
        Rarity.RARE: {'dice': Dice.from_string('2d8'), 'bonus': 5},
        Rarity.EPIC: {'dice': Dice.from_string('3d8'), 'bonus': 10},
        Rarity.LEGENDARY: {'dice': Dice.from_string('4d8'), 'bonus': 20},
    }

    def __init__(self, props=None):
        self.rarity = Rarity.COMMON
        if props is not None and 'rarity' in props:
            self.rarity = props['rarity']

        self.dice = self.variants[self.rarity]['dice']
        self.bonus = self.variants[self.rarity]['bonus']

        img_variant = 'minor'
        if self.rarity in [Rarity.EPIC, Rarity.LEGENDARY, Rarity.PEARLESCENT]:
            img_variant = 'major'
        self.asset = {
            'path_to_img': f"img/items/health_{img_variant}.png"
        }

        self.name = f"{self.rarity} Health Potion"


class ShieldPotion(Potion):
    name = 'Shield Potion'

    variants = {
        Rarity.COMMON: {'dice': Dice.from_string('1d8'), 'bonus': 0},
        Rarity.UNCOMMON: {'dice': Dice.from_string('1d8'), 'bonus': 5},
        Rarity.RARE: {'dice': Dice.from_string('2d8'), 'bonus': 5},
        Rarity.EPIC: {'dice': Dice.from_string('3d8'), 'bonus': 10},
        Rarity.LEGENDARY: {'dice': Dice.from_string('4d8'), 'bonus': 20},
    }

    def __init__(self, props=None):
        self.rarity = Rarity.COMMON
        if props is not None and 'rarity' in props:
            self.rarity = props['rarity']

        self.dice = self.variants[self.rarity]['dice']
        self.bonus = self.variants[self.rarity]['bonus']

        self.asset = {
            'path_to_img': f"img/items/shield.png"
        }

        self.name = f"{self.rarity} Shield Potion"
