from util.rarity import Rarity
from util.dice import Dice
from .cards.bnb_potion_card import generate_potion_card

'''
Common - 1d8
Uncommon - 1d8 + 5
Rare - 2d8 + 5
Epic - 3d8 + 10
Legendary - 4d8 + 20
'''

class HealthPotion:
    variants = {
        Rarity.COMMON: {'dice': Dice.from_string('1d8'), 'bonus': 0},
        Rarity.UNCOMMON: {'dice': Dice.from_string('1d8'), 'bonus': 5},
        Rarity.RARE: {'dice': Dice.from_string('2d8'), 'bonus': 5},
        Rarity.EPIC: {'dice': Dice.from_string('3d8'), 'bonus': 10},
        Rarity.LEGENDARY: {'dice': Dice.from_string('4d8'), 'bonus': 20},
    }

    def __init__(self, rarity: Rarity):
        self.rarity = rarity

        self.dice = self.variants[self.rarity]['dice']
        self.bonus = self.variants[self.rarity]['bonus']

        img_variant = 'minor'
        if self.rarity in [Rarity.EPIC, Rarity.LEGENDARY, Rarity.PEARLESCENT]:
            img_variant = 'major'
        self.asset = {
            'path_to_img': f"img/items/health_{img_variant}.png"
        }



    def generate_card(self):
        generate_potion_card(self)
