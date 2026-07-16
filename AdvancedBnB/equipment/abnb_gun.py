import os
import json
import random
from copy import deepcopy
import time

from file_handling import open_appdatafile, resource_path, appdata_path
from AdvancedBnB.abnb_equipment import AbnbEquipment
from util import Equipment, Dice, lookup_in_table, DiceRequest, GenerationSession, InfoEvent, AddPropertyEvent, WarningEvent
from AdvancedBnB import Fusion, FusionElement
from AdvancedBnB.abnb_tables import rarity_tables, weapon_part_count
from AdvancedBnB.abnb_util import get_item_tier
from AdvancedBnB.abnb_manufacturers import Manufacturers, manufacturer_table
from AdvancedBnB.abnb_traits import trait_high_calibre
from AdvancedBnB.gun.abnb_weapon_modifiers import *
from AdvancedBnB.gun.abnb_weapon_traits import WeaponTrait
from AdvancedBnB.gun.abnb_weapon_parts import WeaponPart, WeaponPartScope, weapon_parts_table, weapon_accessories_table, weapon_sight_table
from AdvancedBnB.gun.abnb_guntypes import Guntypes
from AdvancedBnB.gun.abnb_gun_card import generate_gun_card
from util.common_traits import trait_elemental
from util.common_modifiers import mod_is_elemental, mod_elemental_roll_number, mod_forced_element

DEBUG = True

def mod_to_string(val_1, val_2):
    delta = val_1 - val_2
    if delta != 0:
        return f"({'+' if delta > 0 else ''}{delta})"

    return ''

def debug_print(*args, **kwargs):
    if DEBUG is True:
        print(*args, **kwargs)

class Gun(AbnbEquipment):
    enable_high_calibre = True

    def __init__(self):
        super().__init__()

        self.gun_type = Guntypes.PISTOL

        self.base_stats = {
            'hit_dice': Dice.from_string('1d4'),
            'crit_dice': Dice.from_string('1d4'),
            'hits_crits' : {
                'glance': {'hits': 0, 'crits': 0},
                'solid': {'hits': 0, 'crits': 0},
                'penetrate': {'hits': 0, 'crits': 0}
            },
            'range': 0,
            'mag_size': 0
        }

        self.hit_dice = Dice(1, 4)
        self.crit_dice = Dice(1, 4)

    def reset(self):
        # Clear Equipment
        to_delete = self.equipment_properties.copy()
        for prop in to_delete:
            prop.detach()

        self.eridian = False
        self.n_parts = 0

        print(f"Reset equipment...")
        print(f" - {len(self.equipment_properties)} Properties left")
        print(f" - {len(self.equipment_modifiers)} Modifiers left")

    def new_generation_session(self, user_input=False):
        return GenerationSession(self._generate_impl(), manual=user_input)

    def _generate_impl(self):
        t_start = time.time()

        self.reset()

        # Determine level and tier
        self.tier = get_item_tier(self.level)

        # Manufacturer and gun type
        debug_print(f"Determining Gun Manufacturer...")
        new_manufacturer = None
        while new_manufacturer is None:
            roll = yield DiceRequest('1d12', f"Roll [b][u]1d12[/u][/b] on the Manufacturer table.")
            new_manufacturer = manufacturer_table[roll]
            yield InfoEvent(f"Rolled Manufacturer <[b][i]{new_manufacturer}[/i][/b]>!", trailing_img=resource_path(f"img/guild_logo/AdvancedBnB/{new_manufacturer}.png"))
            debug_print(f"Rolled a {roll}! Gun Manufacturer = {new_manufacturer}")
            if new_manufacturer == Manufacturers.ERIDIAN:
                yield InfoEvent(f"Rolled <[b][i]Eridian[/i][/b]> Manufacturer. Roll again for Manufacturer of Gun Base.")
                debug_print(f"Rolled Eridian Manufacturer. Roll again for Manufacturer of Gun Base.")
                self.eridian = True
                new_manufacturer = None
            else:
                yield from self.set_manufacturer(new_manufacturer)

        debug_print(f"Determining Gun Type, made by {self.manufacturer}...")
        roll = yield DiceRequest('1d12', f"Roll [b][u]1d12[/u][/b] on the Gun Type table.")
        new_guntype = self.manufacturer.make_random_gun(roll)
        debug_print(f"Rolled a {roll}! Gun Type = {new_guntype}")
        yield InfoEvent(f"Rolled a <[b][i]{new_guntype}[/i][/b]>!", trailing_img=resource_path(f"img/gun_symbol/{new_guntype.asset_dir}.png"))
        yield from self.set_gun_type(new_guntype)

        # Weapon base stats
        self.base_stats = self.gun_type.get_basestats(self.tier)
        self.hit_dice = self.base_stats['hit_dice']
        self.crit_dice = self.base_stats['crit_dice']

        # Rarity and element
        debug_print(f"Determining Gun Rarity and Element...")
        d4_roll = yield DiceRequest('1d4', f"Roll [b][u]1d4[/u][/b] on the Rarity and Element table (1/2).")
        d6_roll = yield DiceRequest('1d6', f"Roll [b][u]1d6[/u][/b] on the Rarity and Element table (2/2).")
        self.rarity, roll_for_element = rarity_tables['normal'][d4_roll][d6_roll]

        debug_print(f"Rolled a {d4_roll}(d4) and a {d6_roll}(d6)! Gun Rarity = {self.rarity}.{' Might also be Elemental.' if roll_for_element else ''}")
        yield InfoEvent(f"Rolled <[b][i]{self.rarity}[/i][/b]> Rarity!")
        if roll_for_element is True:
            yield InfoEvent(f"You may roll on the Elemental table later!")

        # Roll for weapon parts
        debug_print(f"Determining Gun Parts...")

        # Resolve Gun Parts provided by Traits/Mods (These all do not count towards Part count total)
        max_firemodes = self.get_modifier_value(mod_tacticool_firemodes)
        n_firemodes = 0
        while n_firemodes < max_firemodes:
            fire_mode = yield from Manufacturers.DAHL.pick_fire_mode()
            if self.has_property(type(fire_mode)) is False:
                fire_mode.attach(self)
                n_firemodes += 1
                yield AddPropertyEvent('Dahl Fire Mode', fire_mode)
            else:
                debug_print(f"Fire mode <{fire_mode.name}> already present!")
                yield InfoEvent(f"Dahl Fire Mode <[b][i]{fire_mode.name}[/i][/b]> is already present! Roll again...")

        max_scopes = self.get_modifier_value(mod_fixed_scopes)
        n_scopes = 0
        while n_scopes < max_scopes:
            scope_part = yield from self.pick_weapon_scope()
            if self.has_property(type(scope_part)) is False:
                scope_part.attach(self)
                n_scopes += 1
                yield AddPropertyEvent('Gun Scope Part', scope_part)
            else:
                debug_print(f"Scope Part <{scope_part.name}> already present!")
                yield InfoEvent(f"Gun Scope Part <[b][i]{scope_part.name}[/i][/b]> is already present! Roll again...")

        max_parts = self.get_modifier_value(mod_extra_accessories)
        n_parts = 0
        while n_parts < max_parts:
            accessory_part = yield from self.pick_weapon_accessory()
            if self.has_property(type(accessory_part)) is False:
                accessory_part.attach(self)
                n_parts += 1
                yield AddPropertyEvent('Accessory Gun Part', accessory_part)
            else:
                debug_print(f"Accessory Part <{accessory_part.name}> already present!")
                yield InfoEvent(f"Gun Accessory Part <[b][i]{accessory_part.name}[/i][/b]> is already present! Roll again...")

        # Roll for remaining parts
        self.n_parts = 0
        while self.n_parts < self.max_parts:
            debug_print(f"Rolling for part {self.n_parts+1}/{self.max_parts}...")
            yield InfoEvent(f"Picking Gun Part {self.n_parts+1}/{self.max_parts}...")
            roll = yield DiceRequest('1d100', f"Roll [b][u]1d100[/u][/b] on the Gun Part table.")
            part = lookup_in_table(weapon_parts_table, roll)

            if part == 'sight':
                debug_print(f"Rolled a {roll}! You may roll for a Gun Scope!")
                yield InfoEvent(f"Rolled a Gun Scope!")

                if self.has_property(WeaponPartScope):
                    debug_print(f"Gun already has a Gun Scope... Roll for new part...")
                    yield InfoEvent(f"Gun already has a Gun Scope... Roll for a new Gun Part...")
                    part = None
                else:
                    part = yield from self.pick_weapon_scope()
                    # Check if Scope is compatible with the Gun Type
                    if not self.gun_type in part.weapon_types:
                        debug_print(f"Gun Type <{self.gun_type}> is not compatible with Scope <{part.name}>... Roll for a new part...")
                        yield InfoEvent(f"Gun Type <[b][i]{self.gun_type}[/i][/b]> is not compatible with Scope <[b][i]{part.name}[/i][/b]>... Roll for a new Gun Part...")
                        part = None

            elif part == 'accessories':
                yield InfoEvent(f"Rolled a Gun Accessory!")
                debug_print(f"Rolled a {roll}! You may roll for a Gun Accessory!")
                part = yield from self.pick_weapon_accessory()

            # Check if part is already applied
            if self.has_property(type(part)):
                debug_print(f"Picked a <{part.name}>! But the Gun already has it... Try again!")
                yield InfoEvent(f"Rolled a <[b][i]{part.name}[/i][/b]>, but the Gun already has that part... Roll for a new Gun Part...")
                part = None

            if part is not None:
                part.attach(self)
                yield AddPropertyEvent('Gun Part', part)
                self.n_parts += 1

        # Roll for Element(s)
        # Determine number of Elemental Rolls
        elemental_rolls = 0
        if roll_for_element is True or self.has_modifier(mod_forced_element):
            elemental_rolls = 1

        if self.has_modifier(mod_elemental_roll_number):
            elemental_rolls = self.get_modifier_value(mod_elemental_roll_number)

        yield from self.roll_for_elements(elemental_rolls)

        # If Originally Manufactured by Eridian. Apply Eridian Effects afterwards
        if self.eridian:
            self.manufacturer = Manufacturers.ERIDIAN
            self.manufacturer.gun_part_exception(self)

        # Randomly choose a Gun name
        yield from self.randomize_name()

        print(f"Finished generating <{self.name}> in {time.time() - t_start}s")
        yield InfoEvent(f"Finished generating Gun <[b][i]{self.name}[/i][/b]>!")

    def set_manufacturer(self, new_manufacturer):
        # Remove old manufacturer traits
        if self.manufacturer is not None:
            for old_trait in self.manufacturer.weapon_traits['primary'] + self.manufacturer.weapon_traits['secondary']:
                old_trait.detach()

        # Set new manufacturer
        self.manufacturer = new_manufacturer

        # Load new manufacturer traits
        # Primary weapon traits
        for trait in self.manufacturer.weapon_traits['primary']:
            trait.attach(self)
            yield AddPropertyEvent('Primary Gun Trait', trait)

        # Secondary weapon trait
        if self.manufacturer.sec_wpn_trait_roll is True:
            roll = yield DiceRequest('1d6', f"Roll [b][u]1d6[/u][/b] for {self.manufacturer} Secondary Gun Trait.")
            trait = self.manufacturer.pick_secondary_weapon_trait(roll)
            if trait:
                trait.attach(self)
                yield AddPropertyEvent('Secondary Gun Trait', trait)

    def set_gun_type(self, new_type):
        for old_trait in self.gun_type.weapon_bonus:
            old_trait.detach()

        self.gun_type = new_type

        for new_trait in new_type.weapon_bonus:
            new_trait.attach(self)
            yield AddPropertyEvent('Gun Bonus', new_trait)

    def randomize_name(self):
        if os.path.isfile(appdata_path('assets.json')):
            with open_appdatafile('assets.json') as file:
                asset_data = json.load(file)

            self.asset = random.choice(asset_data['weapons'][self.gun_type.asset_dir])
            self.name_raw = self.asset['item_name']
            yield InfoEvent(f"Random Gun name: <[b][i]{self.name_raw}[/i][/b]>")
        else:
            yield WarningEvent(f"[b][u]No Gun Images loaded![/u][/b] Please go to [i]Image Assets[/i] -> [i]Load Images[/i].")
            self.name_raw = "New Gun"

    def pick_weapon_accessory(self):
        roll = yield DiceRequest('1d100', f"Roll a [b][u]1d100[/u][/b] on the Gun Accessory table.")
        part = lookup_in_table(weapon_accessories_table, roll)

        return part

    def pick_weapon_scope(self):
        part = None

        retries_left = 50
        while retries_left > 0:
            roll = yield DiceRequest('1d100', f"Roll a [b][u]d100[/u][/b] on Gun Scope table.")
            part = lookup_in_table(weapon_sight_table, roll)
            # Check if part already present
            for property in self.equipment_properties:
                if isinstance(part, type(property)):
                    debug_print(f"Rolled a {roll}! But the part <{part.name}> is already equipped. Roll again...")
                    part = None
                    retries_left -= 1
                    break

            if part is not None:
                debug_print(f"Rolled a {roll}! Adding Gun Scope <{part.name}>!")
                break

        assert part is not None, f"Failed to roll for a Weapon Scope...\n{self}"

        return part

    @property
    def mag_size(self):
        mag_size = self.base_stats['mag_size'] + self.get_modifier_value(mod_mag_size)

        # Magazine size cannot go below 1
        if mag_size < 1:
            mag_size = 1

        return mag_size

    @property
    def range(self):
        return self.base_stats['range'] + self.get_modifier_value(mod_range)

    @property
    def max_parts(self):
        return weapon_part_count[self.rarity] + self.get_modifier_value(mod_maximum_parts)

    @property
    def n_scopes(self):
        scope_cnt = 0
        for property in self.equipment_properties:
            if isinstance(property, WeaponPartScope):
                scope_cnt += 1

        return scope_cnt

    @property
    def hits_crits(self):
        # Load base stats
        stats = deepcopy(self.base_stats['hits_crits'])

        # Apply Modifiers to stats
        burst_value = self.get_modifier_value(mod_burst)
        for atk in ['glance', 'solid', 'penetrate']:
            stats[atk]['hits'] += burst_value

        stats['penetrate']['crits'] += self.get_modifier_value(mod_penetrate_crits)

        # Clamp values
        # Hits & Crits cannot be lowered below 1 (if Gun basestats were non-zero)
        for atk in ['glance', 'solid', 'penetrate']:
            if stats[atk]['hits'] < 1 and self.base_stats['hits_crits'][atk]['hits'] != 0:
                stats[atk]['hits'] = 1

            if stats[atk]['crits'] < 1 and self.base_stats['hits_crits'][atk]['crits'] != 0:
                stats[atk]['crits'] = 1

        return stats


    def generate_card(self):
        self.generated_card = generate_gun_card(self)


    def  __repr__(self):
        t_start = time.time()

        str = ''
        str += f"--- Generated Gun --- \n"
        str += f"Name: <{self.name}> \n"
        str += f"Type: (Lv.{self.level}) {self.rarity} {self.gun_type}\n"
        str += f"Manufacturer: {self.manufacturer}\n"
        str += f"n Gun Parts: {self.n_parts}\n"
        str += f"n Gun Scope: {self.n_scopes}\n"

        str += f"Elements: \n"
        for el in self.elements:
            str += f" - {el}\n"
        str += f"\n"

        mod_str = mod_to_string(self.range, self.base_stats['range'])
        str += f"Range: {self.range}{mod_str}\n"
        mod_str = mod_to_string(self.mag_size, self.base_stats['mag_size'])
        str += f"Mag Size: {self.mag_size}{mod_str}\n"
        str += f"Accuracy:\n"
        for atk, acc_range in [('glance', '2-7 '),  ('solid', '8-15'), ('penetrate', '16+ ')]:
            hit_mod = mod_to_string(self.hits_crits[atk]['hits'], self.base_stats['hits_crits'][atk]['hits'])
            crit_mod = mod_to_string(self.hits_crits[atk]['crits'], self.base_stats['hits_crits'][atk]['crits'])

            str += f" - {acc_range}: {self.hits_crits[atk]['hits']}{hit_mod} Hits, {self.hits_crits[atk]['crits']}{crit_mod} Crits\n"

        str += f"Hit Die : {self.hit_dice}\n"
        str += f"Crit Die: {self.crit_dice}\n"
        str += f"\n"

        # Weapon Bonus
        str += f"Weapon Bonus:\n"
        for bonus in self.gun_type.weapon_bonus:
            str += f" - {bonus.effect}\n"
        str += f"\n"

        # Print Weapon Traits
        str += f"Traits:\n"
        for trait in self.equipment_properties:
            if isinstance(trait, WeaponTrait):
                str += f" - {trait.name} - {trait.effect}\n"
        str += f"\n"

        # Print Weapon Parts
        str += f"Parts:\n"
        for part in self.equipment_properties:
            if isinstance(part, WeaponPart):
                str += f" - {part.name}: {part.effect}\n"
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

        print(f"Building repr: {time.time() - t_start}s")

        return str
