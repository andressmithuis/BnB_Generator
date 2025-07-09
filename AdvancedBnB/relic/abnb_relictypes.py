from copy import deepcopy

from AdvancedBnB import Manufacturers, Incendiary, Shock, Corrosive, Explosive, Slag, Cryo, Radiation
from AdvancedBnB.abnb_manufacturers import manufacturer_table
from AdvancedBnB.gun import Guntypes
from util import Rarity, Dice, roll_on_table

from .abnb_relic_parts import *

rarity_nparts_table = {
    Rarity.COMMON: 1,
    Rarity.UNCOMMON: 2,
    Rarity.RARE: 3,
    Rarity.EPIC: 4,
    Rarity.LEGENDARY: 5,
    Rarity.PEARLESCENT: 6
}

dice_table = {
    (1, 4): Dice.from_string('1d4'),
    (5, 6): Dice.from_string('1d6'),
    (7, 8): Dice.from_string('1d8'),
    (9, 10): Dice.from_string('1d10'),
    (11, 12): Dice.from_string('1d12'),
    (13, 20): Dice.from_string('1d20'),
}

weapon_types_table = {
    1: Guntypes.PISTOL,
    2: Guntypes.SMG,
    3: Guntypes.RIFLE,
    4: Guntypes.SHOTGUN,
    5: Guntypes.SNIPER,
    6: Guntypes.LAUNCHER
}

element_type_table = {
    1: Incendiary(),
    2: Shock(),
    3: Corrosive(),
    4: Explosive(),
    5: Slag(),
    6: Cryo(),
    7: Radiation(),
    8: 'again'
}

class Relic:
    part_options = []

    def pick_manufacturer(self):
        return Manufacturers.ERIDIAN

    def create_part_pool(self, tier):
        # Add (copy) parts to pool (list)
        pool = []
        for part in self.part_options:
            for i in range(part[1]):
                new_part = deepcopy(part[0])
                pool.append(new_part)

        return pool

    def roll_parts(self, item):
        part_pool = self.create_part_pool(item.tier)

        n_parts = rarity_nparts_table[item.rarity]

        selected_parts = []
        while n_parts > 0:
            # If no parts are left, break off NOTE: SHOULD NOT BE POSSIBLE
            if len(part_pool) == 0:
                break

            # If one part left in the pool, return that one directly
            if len(part_pool) == 1:
                selected_parts.append(part_pool[0])
                break

            # Determine used dice based on size of pool
            dice = roll_on_table(dice_table, len(part_pool))

            # Roll part from pool
            roll = 100
            while roll > len(part_pool):
                roll = dice.roll()

            # Remove part from pool, add it to the selection
            part = part_pool.pop(roll-1)
            selected_parts.append(part)
            n_parts -= 1

        return selected_parts


class RelicAggression(Relic):
    name = 'Aggression'

    part_options = [
        (relic_part_gun_damage(), 2),
        (relic_part_gun_accuracy(), 1),
        (relic_part_gun_reload(), 2),
        (relic_part_gun_swap(), 2),
        (relic_part_gun_magsize(), 1)
    ]

    def create_part_pool(self, tier):
        #Roll for Weapon Type
        weapon = weapon_types_table[Dice.from_string('1d6').roll()]

        # Add (copy) parts to pool (list)
        pool = []
        for part in self.part_options:
            for i in range(part[1]):
                new_part = deepcopy(part[0])
                new_part.applies_to = weapon.name
                pool.append(new_part)

        return pool


class RelicAllegiance(Relic):
    name = 'Allegiance'
    manufacturer = None

    part_options = [
        (relic_part_gun_damage(), 2),
        (relic_part_gun_accuracy(), 1),
        (relic_part_gun_reload(), 2),
        (relic_part_gun_swap(), 2),
        (relic_part_gun_magsize(), 1)
    ]

    def pick_manufacturer(self):
        # Roll for Manufacturer Type
        self.manufacturer = manufacturer_table[Dice.from_string('1d12').roll()]
        return self.manufacturer

    def create_part_pool(self, tier):
        if self.manufacturer is None:
            self.pick_manufacturer()

        # Add (copy) parts to pool (list)
        pool = []
        for part in self.part_options:
            for i in range(part[1]):
                new_part = deepcopy(part[0])
                new_part.applies_to = self.manufacturer.name
                pool.append(new_part)

        return pool


class RelicElemental(Relic):
    name = 'Elemental'

    part_options = [
        (relic_part_elemental_damage(), 2),
        (relic_part_elemental_effect(), 3),
        (relic_part_elemental_puddle(), 1),
    ]

    def pick_manufacturer(self):
        manufacturer_table = {
            (1, 6): Manufacturers.ERIDIAN,
            (6, 12): Manufacturers.MALIWAN
        }

        # Roll for Manufacturer Type
        return manufacturer_table[Dice.from_string('1d12').roll()]

    def create_part_pool(self, tier):
        #Roll for Element Type
        element = 'again'
        while element == 'again':
            element = element_type_table[Dice.from_string('1d8').roll()]

        # Add (copy) parts to pool (list)
        pool = []
        for part in self.part_options:
            for i in range(part[1]):
                new_part = deepcopy(part[0])
                new_part.applies_to = element.name
                pool.append(new_part)

        return pool


class RelicProficiency(Relic):
    name = 'Proficiency'

    part_options = [
        (relic_part_actionskill_damage(), 3),
        (relic_part_actionskill_uses(), 1),
        (relic_part_actionskill_duration(), 1),
    ]


class RelicProtection(Relic):
    name = 'Protection'

    part_options = [
        (relic_part_shield_capacity(), 2),
        (relic_part_shield_recharge(), 3),
    ]


class RelicResistance(Relic):
    name = 'Resistance'

    part_options = [
        (relic_part_elemental_resistance(), 4),
    ]

    def create_part_pool(self, tier):
        elements_used = []

        # Add (copy) parts to pool (list)
        pool = []
        for part in self.part_options:
            for i in range(part[1]):
                new_part = deepcopy(part[0])
                # Roll for element (need to be different everytime)
                element = 'again'
                while element == 'again':
                    element = element_type_table[Dice.from_string('1d8').roll()]
                    if element.name in elements_used:
                        element = 'again'

                new_part.applies_to = element.name
                pool.append(new_part)
                elements_used.append(element.name)

        return pool


class RelicStockpile(Relic):
    name = 'Stockpile'

    part_options = [
        (relic_part_expanded_reserve(), 3),
        (relic_part_expanded_grenades(), 1),
    ]

    def create_part_pool(self, tier):
        guntypes_used = []

        # Add (copy) parts to pool (list)
        pool = []
        for part in self.part_options:
            for i in range(part[1]):
                new_part = deepcopy(part[0])

                if isinstance(new_part, relic_part_expanded_reserve):
                    # Roll for Gun Type (need to be different everytime)
                    guntype = 'again'
                    while guntype == 'again':
                        guntype = weapon_types_table[Dice.from_string('1d6').roll()]
                        if guntype.name in guntypes_used:
                            guntype = 'again'

                    new_part.applies_to = guntype.name
                    guntypes_used.append(guntype.name)

                pool.append(new_part)


        return pool


class RelicStrength(Relic):
    name = 'Strength'

    part_options = [
        (relic_part_melee_damage(), 3),
        (relic_part_move_speed(), 1),
        (relic_part_melee_attacks(), 2),
    ]

    def pick_manufacturer(self):
        manufacturer_table = {
            (1, 6): Manufacturers.ERIDIAN,
            (6, 12): Manufacturers.BANDIT
        }

        # Roll for Manufacturer Type
        return roll_on_table(manufacturer_table, Dice.from_string('1d12').roll())

    def create_part_pool(self, tier):
        # Add (copy) parts to pool (list)
        pool = []
        for part in self.part_options:
            for i in range(part[1]):
                new_part = deepcopy(part[0])

                # Melee Attacks Part only provides bonus from Tier 5 onwards, exclude for lower Tiers
                if isinstance(new_part, relic_part_melee_attacks):
                    if tier >= 5:
                        pool.append(new_part)
                else:
                    pool.append(new_part)

        return pool


class RelicTenacity(Relic):
    name = 'Tenacity'

    part_options = [
        (relic_part_ffyl_duration(), 3),
        (relic_part_revive_healing(), 2),
    ]


class RelicVitality(Relic):
    name = 'Vitality'

    part_options = [
        (relic_part_max_health(), 2),
        (relic_part_health_regen(), 3),
    ]


class Relictypes:
    AGGRESSION = RelicAggression()
    ALLEGIANCE = RelicAllegiance()
    ELEMENTAL = RelicElemental()
    PROFICIENCY = RelicProficiency()
    PROTECTION = RelicProtection()
    RESISTANCE = RelicResistance()
    STOCKPILE = RelicStockpile()
    STRENGTH = RelicStrength()
    TENACITY = RelicTenacity()
    VITALITY = RelicVitality()
