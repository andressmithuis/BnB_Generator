from copy import deepcopy

from util import Equipment, Dice, lookup_in_table
from util.common_modifiers import *
from util.common_traits import *
from .abnb_tables import elemental_table, fusion_table
from .abnb_element import Fusion, FusionElement
from .abnb_traits import *


class AbnbEquipment(Equipment):
    enable_high_calibre = False  # Specific for Gun Equipment

    def __init__(self):
        super().__init__()

        self.generated_card = []

    def roll_for_elements(self, attempts):
        # Rolls for Element(s)
        n_rolls = 0
        while n_rolls < attempts:
            print(f"Rolling Element attempt {n_rolls + 1}/{attempts}")
            rolled_element = self.pick_element_from_table()
            n_rolls += 1

            # Check if rolled Element is blacklisted
            if rolled_element is not None:
                for blacklisted_element in self.disabled_elements:
                    if isinstance(rolled_element, type(blacklisted_element)):
                        rolled_element = None
                        break

            # Check if rolled Element matches forced Element (to allow forced Element +1/+2)
            if rolled_element is not None:
                if self.forced_element is not None:
                    if not isinstance(rolled_element, type(self.forced_element)):
                        print(f"Element is being forced to be <{self.forced_element}>")
                        rolled_element = self.forced_element

            # Check if Equipment is forced Non-Elemental
            if rolled_element is not None:
                if self.forced_non_elemental:
                    if self.enable_high_calibre is True:
                        # Add High Caliber Property instead (Gun Equipment only)
                        new_trait = trait_high_calibre()
                        new_trait.n_dice = 1 + rolled_element.bonus
                        if isinstance(rolled_element, FusionElement):
                            # If rolled element is a Fusion, effectively double the number of bonus dice
                            new_trait.n_dice *= 2
                        new_trait.attach(self)

                    rolled_element = None

            # Check if rolled Element is already present
            if rolled_element is not None:
                for available_element in self.elements:
                    if isinstance(rolled_element, type(available_element)):
                        print(f"Element <{rolled_element}> is already applied!")
                        rolled_element = None

            # Add resulting element
            if rolled_element is not None:
                element_trait = trait_elemental()
                element_mod = deepcopy(rolled_element)
                element_trait.type = element_mod
                element_mod.attach(element_trait)
                element_trait.attach(self)

            # Allow a reroll if Equipment is forced Elemental, but the Elemental rolls did not result in an Element being applied
            if self.forced_elemental:
                if n_rolls >= attempts:
                    if len(self.elements) == 0:
                        print(f"Equipment is forced Elemental, but no Elements are applied yet! Roll again...")
                        n_rolls = attempts - 1

    def pick_element_from_table(self):
        d100 = Dice.from_string('1d100')
        dice_roll = min([d100.roll(f"Roll on Element table") + self.elemental_roll_bonus, 100])
        rolled_element = lookup_in_table(elemental_table, dice_roll)[self.rarity]
        print(f"Rolled a {dice_roll}(+{self.elemental_roll_bonus})! Rolled a <{rolled_element}> Element")

        if isinstance(rolled_element, Fusion):
            d8 = Dice.from_string('1d8')

            while True:
                print(f"Rolling for specific Fusion Element...")
                roll_1 = d8.roll(f"Roll on Elemental Fusion Table(1/2)")
                roll_2 = d8.roll(f"Roll on Elemental Fusion Table(2/2)")
                fusion_element = fusion_table[roll_1][roll_2]

                print(f"Rolled a {roll_1} and {roll_2} resulting in <{fusion_element}> Element Fusion")

                # TODO: Handle 'Special' columns
                if fusion_element == 'special':
                    # Reroll for now
                    pass
                else:
                    if fusion_element is not None:
                        fusion_element.bonus = rolled_element.bonus
                    rolled_element = fusion_element
                    break

        return rolled_element
