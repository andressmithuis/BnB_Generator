from copy import deepcopy
from tkinter import Tk, filedialog
import pathlib

from util import Equipment, lookup_in_table, DiceRequest
from util.common_modifiers import *
from util.common_traits import *
from util.cards.card_basics import card_merge_sideways
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
            rolled_element = yield from self.pick_element_from_table()
            n_rolls += 1

            # Check if rolled Element is blacklisted
            if rolled_element is not None:
                for blacklisted_element in self.blacklisted_elements:
                    if isinstance(rolled_element, type(blacklisted_element)):
                        rolled_element = None
                        break

            # Check if rolled Element matches forced Element (to allow forced Element +1/+2)
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
        dice_roll = yield DiceRequest('1d100', f"Roll 1d100 for Element on Element table")
        element_roll = min([dice_roll + self.elemental_roll_bonus, 100])
        rolled_element = lookup_in_table(elemental_table, element_roll)[self.rarity]
        print(f"Rolled a {dice_roll}(+{self.elemental_roll_bonus})! Rolled a <{rolled_element}> Element")

        if isinstance(rolled_element, Fusion):
            while True:
                print(f"Rolling for specific Fusion Element...")
                roll_1 = yield DiceRequest('1d8', f"Roll 1d8 on Elemental Fusion table (1/2)")
                roll_2 = yield DiceRequest('1d8', f"Roll 1d8 on Elemental Fusion table (2/2)")
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

    def export_generated_card(self):
        card_joined = card_merge_sideways(self.generated_card[0], self.generated_card[1])

        # Open SaveAs Dialog
        root = Tk()
        root.withdraw()

        filename = filedialog.asksaveasfilename(
            defaultextension='*.png',
            filetypes = [
                ('PNG Image', '*.png'),
                ('BMP Image', '*.bmp'),
                ('All Files', '*.*')
            ]
        )
        root.destroy()

        # Save file if valid path is given
        if filename:
            ext = pathlib.Path(filename).suffix
            ext = ext.replace('.', '').upper()
            card_joined.save(filename, ext, quality=100)
