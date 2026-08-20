import json
import random
from copy import deepcopy
import time
import os

from AdvancedBnB.abnb_equipment import AbnbEquipment
from AdvancedBnB.abnb_tables import rarity_tables, shield_part_count
from AdvancedBnB.abnb_util import get_item_tier
from AdvancedBnB.shield.abnb_shield_card import generate_shield_card
from AdvancedBnB import FusionElement
from AdvancedBnB.abnb_manufacturers import Manufacturers, manufacturer_table
from util import Dice, lookup_in_table, DiceRequest, InfoEvent, AddPropertyEvent, WarningEvent
from util.common_modifiers import *
from file_handling import open_appdatafile, resource_path, appdata_path

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
        self.card_render_func = generate_shield_card

        self.shield_type = Shieldtypes.FAST
        self.tag = None

        self.base_stats = {
            'capacity': 0,
            'charge_rate': 0
        }

        self.max_parts = 0

    def generator_func(self):
        t_start = time.time()

        self.reset()

        # Manufacturer and shield type
        new_manufacturer = None
        while new_manufacturer is None:
            roll = yield DiceRequest('1d12', f"Roll [b][u]1d12[/u][/b] on the Manufacturer table.")
            new_manufacturer = manufacturer_table[roll]
            yield InfoEvent(f"Rolled Manufacturer <[b][i]{new_manufacturer}[/i][/b]>!", trailing_img=resource_path(f"img/guild_logo/AdvancedBnB/{new_manufacturer}.png"))
            if new_manufacturer == Manufacturers.ERIDIAN:
                yield InfoEvent(f"Rolled <[b][i]Eridian[/i][/b]> Manufacturer. Roll again for Manufacturer of Shield Base.")
                self.eridian = True
                new_manufacturer = None
            else:
                yield from self.set_manufacturer(new_manufacturer)

        # Shield base stats
        self.base_stats = self.shield_type.get_basestats(self.tier)

        # Rarity and element
        print(f"Determining Shield Rarity and Element...")
        d4_roll = yield DiceRequest('1d4', f"Roll [b][u]1d4[/u][/b] on the Rarity and Element table (1/2).")
        d6_roll = yield DiceRequest('1d6', f"Roll [b][u]1d6[/u][/b] on the Rarity and Element table (2/2).")
        self.rarity, roll_for_element = rarity_tables['normal'][d4_roll][d6_roll]
        yield InfoEvent(f"Rolled <[b][i]{self.rarity}[/i][/b]> Rarity!")
        if roll_for_element is True:
            yield InfoEvent(f"You may roll on the Elemental table later!")

        # Roll for Element(s)
        # Determine number of Elemental Rolls
        elemental_rolls = 0
        if roll_for_element is True or self.has_modifier(mod_forced_element):
            elemental_rolls = 1

        if self.has_modifier(mod_elemental_roll_number):
            elemental_rolls = self.get_modifier_value(mod_elemental_roll_number)

        yield from self.roll_for_elements(elemental_rolls)

        # If the Shield is now Elemental, add a matching Resistant part
        if len(self.elements) > 0:
            yield from self.add_resistant_parts()

        # Roll for Shield parts
        print(f"Determining Shield Parts...")
        self.max_parts = shield_part_count[self.rarity]
        self.n_parts = 0

        # Roll for remaining parts
        # NOTE: Shields CAN have multiples of the same part. Shield effects denote this by the '/P'.
        while self.n_parts < self.max_parts:
            print(f"Rolling for part {self.n_parts+1}/{self.max_parts}...")
            roll = yield DiceRequest('1d100', f"Roll [b][u]1d100[/u][/b] on the Shield Parts Table.")
            part = lookup_in_table(shield_parts_table, roll)
            new_part = deepcopy(part)

            # Elemental part exceptions (Resistant, Nova, Spike)
            if isinstance(new_part, (shd_part_resistant, shd_part_spike, shd_part_nova)):
                # Reroll if Shield has to be Non-Elemental
                if self.forced_non_elemental:
                    yield InfoEvent(f"Rolled a <[b][i]{new_part.name}[/i][/b]> part, but the Shield is forced Non-Elemental... Roll again...")
                    continue

                # Force an element if the Shield is not elemental yet
                while len(self.elements) == 0:
                    yield InfoEvent(f"Rolled a <[b][i]{new_part.name}[/i][/b]> part, but the Shield is not yet Elemental...")
                    yield from self.roll_for_elements(1)
                    # If the Shield is now Elemental, add a matching Resistant part(unless the new part is a Resistant part, which will be added a bit later anyway)
                    if not isinstance(new_part, shd_part_resistant):
                        if len(self.elements) > 0:
                            yield from self.add_resistant_parts()

            if isinstance(new_part, shd_part_resistant):
                # Add Resistant part
                yield from self.add_resistant_parts()
            else:
                # Add regular part
                yield AddPropertyEvent('Shield Part', new_part)
                new_part.attach(self)

            self.n_parts += 1

        # If Originally Manufactured by Eridian, apply Eridian Shield Effects
        if self.eridian:
            yield InfoEvent(f"Applying <[b][i]Eridian[/i][/b]> properties...")
            self.manufacturer = Manufacturers.ERIDIAN
            eridian_traits = Manufacturers.ERIDIAN.shield_traits['parts']
            for trait in eridian_traits:
                yield AddPropertyEvent('Eridian Trait', trait)
                trait.attach(self)

        # Randomly choose a name
        yield from self.randomize_name()

    def set_manufacturer(self, new_manufacturer):
        # Remove old manufacturer parts
        if self.manufacturer is not None:
            for old_part in self.manufacturer.shield_traits['parts']:
                old_part.detach()

        # Set new manufacturer
        self.manufacturer = new_manufacturer

        # Load new manufacturer parts
        self.shield_type, self.tag, parts = new_manufacturer.make_random_shield()
        yield InfoEvent(f"Shield Properties:\n-\nType: <[b][i]{self.shield_type}[/i][/b]>\nTag: <[b][i]{self.tag.name}[/i][/b]>([i]{self.tag.effect}[/i])")
        for part in parts:
            yield AddPropertyEvent('Shield Part', part)
            part.attach(self)

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
                yield AddPropertyEvent('Shield Part', new_part)
                new_part.attach(self)

    def randomize_name(self):
        if os.path.isfile(appdata_path('assets.json')):
            with open_appdatafile('assets.json') as file:
                asset_data = json.load(file)

            self.asset = random.choice(asset_data['shields'])
            self.name_raw = self.asset['item_name']
            yield InfoEvent(f"Random Shield name: <[b][i]{self.name_raw}[/i][/b]>")
        else:
            yield WarningEvent(f"[b][u]No Shield Images loaded![/u][/b] Please go to [i]Image Assets[/i] -> [i]Load Images[/i].")
            self.name_raw = "New Shield"

        self.name_raw = yield from self.overrides.apply('name', self.name_raw)

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
                str += f"{part.active_mods}\n"
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




