from util.common_traits import trait_forced_element
from .gun.abnb_guntypes import Guntypes
from .gun.abnb_weapon_parts import wp_part_bayonet
from .gun.abnb_weapon_traits import *
from .shield.abnb_shield_parts import *
from .shield.abnb_shieldtypes import Shieldtypes
from .grenade.abnb_grenade_parts import *

from util import lookup_in_table

class Manufacturer:
    name = ''

    def pick_secondary_weapon_trait(self, roll):
        return []

    def roll_for_secondary_weapon_trait(self, roll, table):
        trait = lookup_in_table(table, roll)
        print(f"Rolled a {roll}! Gun Trait <{trait.name}> added.")

        return trait

    def gun_part_exception(self, gun):
        return

    def __repr__(self):
        return f"{self.__class__.name}"


class Anshin(Manufacturer):
    name = 'Anshin'
    logo_file = 'Anshin.png'

    def __init__(self):
        self.makes = {
            'weapons': [Guntypes.PISTOL, Guntypes.SMG, Guntypes.SNIPER],
            'grenades': [],
            'shield': Shieldtypes.FAST,
            'relics': []
        }
        self.weapon_traits = {
            'primary': [trait_do_no_harm(), trait_caseless_ammunition()],
            'secondary': [trait_medic(), trait_vampire()]
        }
        self.shield_traits = {
            'tag': shd_tag_energy(),
            'parts': [shd_part_adaptive()]
        }

    def make_random_gun(self, dice_roll):
        table = {
            (1, 4):  self.makes['weapons'][0],  # Pistol
            (5, 8):  self.makes['weapons'][1],  # Smg
            (9, 12): self.makes['weapons'][2]   # Sniper
        }

        return lookup_in_table(table, dice_roll)

    def pick_secondary_weapon_trait(self, roll):
        table = {
            (1, 3): self.weapon_traits['secondary'][0],
            (4, 6): self.weapon_traits['secondary'][1]
        }

        return self.roll_for_secondary_weapon_trait(roll, table)

    def make_random_shield(self):
        return self.makes['shield'], self.shield_traits['tag'], self.shield_traits['parts']

    def edit_grenade(self, grenade_obj):
        # Delivery Mechanism: Any
        # Starting Part: Transfusion
        grenade_obj.delivery_system = grenade_delivery_mechanism[Dice.from_string('1d6').roll()]
        grenade_obj.parts.append(grn_payload_transfusion())


class Atlas(Manufacturer):
    name = 'Atlas'
    logo_file = 'Atlas.png'

    def __init__(self):
        self.makes = {
            'weapons': [Guntypes.RIFLE, Guntypes.PISTOL, Guntypes.LAUNCHER],
            'grenades': [],
            'shield': Shieldtypes.HIGHCAPACITY,
            'relics': []
        }
        self.weapon_traits = {
            'primary': [trait_high_quality(), trait_heavy_mags(), trait_lock_on(), trait_non_elemental()],
            'secondary': []
        }
        self.shield_traits = {
            'tag': shd_tag_alloy(),
            'parts': [shd_part_brimming(), trait_non_elemental()]
        }

    def make_random_gun(self, dice_roll):
        table = {
            (1, 4):  self.makes['weapons'][0],  # Combat Rifle
            (5, 8):  self.makes['weapons'][1],  # Pistol
            (9, 12): self.makes['weapons'][2]   # Rocket Launcher
        }

        return lookup_in_table(table, dice_roll)

    def make_random_shield(self):
        return self.makes['shield'], self.shield_traits['tag'], self.shield_traits['parts']

    def edit_grenade(self, grenade_obj):
        # Delivery Mechanism: Any
        # Starting Part: Link
        grenade_obj.delivery_system = grenade_delivery_mechanism[Dice.from_string('1d6').roll()]
        grenade_obj.parts.append(grn_payload_link())


class Bandit(Manufacturer):
    name = 'Bandit'
    logo_file = 'Bandit.png'

    def __init__(self):
        self.makes = {
            'weapons': [Guntypes.RIFLE, Guntypes.PISTOL, Guntypes.LAUNCHER, Guntypes.SHOTGUN, Guntypes.SMG],
            'grenades': [],
            'shield': Shieldtypes.BALANCED,
            'relics': []
        }
        self.weapon_traits = {
            'primary': [trait_big_mags(), trait_pointy(), wp_part_bayonet(), trait_overheat()],
            'secondary': []
        }
        self.shield_traits = {
            'tag': shd_tag_alloy(),
            'parts': [shd_part_roid()]
        }

    def make_random_gun(self, dice_roll):
        table = {
            (1, 2):  self.makes['weapons'][0],  # Combat Rifle
            (3, 5):  self.makes['weapons'][1],  # Pistol
            (11, 12): self.makes['weapons'][2],  # Rocket Launcher
            (6, 8): self.makes['weapons'][3],  # Shotgun
            (9, 10): self.makes['weapons'][4]   # SMG
        }

        return lookup_in_table(table, dice_roll)

    def make_random_shield(self):
        return self.makes['shield'], self.shield_traits['tag'], self.shield_traits['parts']

    def edit_grenade(self, grenade_obj):
        # Delivery Mechanism: Exploder
        # Starting Part: MIRV
        grenade_obj.delivery_system = grn_delivery_exploder()
        grenade_obj.parts.append(grn_payload_mirv())


class Dahl(Manufacturer):
    name = 'Dahl'
    logo_file = 'Dahl.png'

    def __init__(self):
        self.makes = {
            'weapons': [Guntypes.RIFLE, Guntypes.PISTOL, Guntypes.SNIPER, Guntypes.SMG],
            'grenades': [],
            'shield': Shieldtypes.FAST,
            'relics': []
        }
        self.weapon_traits = {
            'primary': [trait_steady_aim(), trait_tacticool(), trait_reconfigure()],
            'secondary': [trait_fm_single_fire(), trait_fm_burst_fire(), trait_fm_full_auto()]
        }
        self.shield_traits = {
            'tag': shd_tag_energy(),
            'parts': []
        }

    def make_random_gun(self, dice_roll):
        table = {
            (1, 3):  self.makes['weapons'][0],  # Combat Rifle
            (4, 6):  self.makes['weapons'][1],  # Pistol
            (7, 9): self.makes['weapons'][2],  # Sniper Rifle
            (10, 12): self.makes['weapons'][3]   # Smg
        }

        return lookup_in_table(table, dice_roll)

    def pick_secondary_weapon_trait(self, roll):
        return []

    def roll_for_secondary_weapon_trait(self, roll, table):
        trait = lookup_in_table(table, roll)
        print(f"Rolled a {roll}! Gun Trait <{trait.name}>")

        return trait

    def pick_fire_mode(self, dice_roller) -> WeaponTrait:
        table = {
            (1, 2): self.weapon_traits['secondary'][0],
            (3, 4): self.weapon_traits['secondary'][1],
            (5, 6): self.weapon_traits['secondary'][2]
        }
        roll = yield from dice_roller.roll('1d6', f"Roll 1d6 for DAHL Gun fire mode")

        return self.roll_for_secondary_weapon_trait(roll, table)

    def make_random_shield(self):
        starting_parts = {
            (1, 3): shd_part_charge_health(),
            (4, 6): shd_part_charge_shield()
        }
        d6 = Dice.from_string('1d6')
        starting_part = lookup_in_table(starting_parts, d6.roll())

        return self.makes['shield'], self.shield_traits['tag'], [starting_part]

    def edit_grenade(self, grenade_obj):
        # Delivery Mechanism: Any
        # Starting Part: Jumping
        grenade_obj.delivery_system = grenade_delivery_mechanism[Dice.from_string('1d6').roll()]
        grenade_obj.parts.append(grn_payload_jumping())


class Hyperion(Manufacturer):
    name = 'Hyperion'
    logo_file = 'Hyperion.png'

    def __init__(self):
        self.makes = {
            'weapons': [Guntypes.PISTOL, Guntypes.SMG, Guntypes.SHOTGUN, Guntypes.SNIPER],
            'grenades': [],
            'shield': Shieldtypes.FAST,
            'relics': []
        }
        self.weapon_traits = {
            'primary': [trait_recoil_control(), trait_gun_shield()],
            'secondary': [trait_shield_amp(), trait_shield_genesis(), trait_shield_redirect()]
        }
        self.shield_traits = {
            'tag': shd_tag_energy(),
            'parts': [shd_part_amp()]
        }

    def make_random_gun(self, dice_roll):
        table = {
            (1, 3):  self.makes['weapons'][0],  # Pistol
            (4, 6):  self.makes['weapons'][1],  # Smg
            (7, 9): self.makes['weapons'][2],   # Shotgun
            (10, 12): self.makes['weapons'][3]  # Sniper
        }

        return lookup_in_table(table, dice_roll)

    def pick_secondary_weapon_trait(self, roll):
        table = {
            (1, 2): self.weapon_traits['secondary'][0],
            (3, 4): self.weapon_traits['secondary'][1],
            (5, 6): self.weapon_traits['secondary'][2]
        }

        return self.roll_for_secondary_weapon_trait(roll, table)

    def make_random_shield(self):
        return self.makes['shield'], self.shield_traits['tag'], self.shield_traits['parts']

    def edit_grenade(self, grenade_obj):
        # Delivery Mechanism: Longbow
        # Starting Part: Singularity
        grenade_obj.delivery_system = grn_delivery_longbow()
        grenade_obj.parts.append(grn_payload_singularity())


class Jakobs(Manufacturer):
    name = 'Jakobs'
    logo_file = 'Jakobs.png'

    def __init__(self):
        self.makes = {
            'weapons': [Guntypes.RIFLE, Guntypes.PISTOL, Guntypes.SHOTGUN, Guntypes.SNIPER],
            'grenades': [],
            'shield': Shieldtypes.HIGHCAPACITY,
            'relics': []
        }
        self.weapon_traits = {
            'primary': [trait_head_hunter(), trait_non_elemental(), trait_cumbersome()],
            'secondary': [trait_fan_the_hammer(), trait_ricochet(), trait_percise()]
        }
        self.shield_traits = {
            'tag': shd_tag_bio(),
            'parts': [shd_part_health(), trait_non_elemental()]
        }

    def make_random_gun(self, dice_roll):
        table = {
            (1, 3):  self.makes['weapons'][0],  # Combat Rifle
            (4, 6):  self.makes['weapons'][1],  # Pistol
            (7, 9): self.makes['weapons'][2],   # Shotgun
            (10, 12): self.makes['weapons'][3]  # Sniper
        }

        return lookup_in_table(table, dice_roll)

    def pick_secondary_weapon_trait(self, roll):
        table = {
            (1, 2): self.weapon_traits['secondary'][0],
            (3, 4): self.weapon_traits['secondary'][1],
            (5, 6): self.weapon_traits['secondary'][2]
        }

        return self.roll_for_secondary_weapon_trait(roll, table)

    def make_random_shield(self):
        return self.makes['shield'], self.shield_traits['tag'], self.shield_traits['parts']

    def edit_grenade(self, grenade_obj):
        # Delivery Mechanism: Lobbed
        # Starting Part: Force
        grenade_obj.delivery_system = grn_delivery_lobbed()
        grenade_obj.parts.append(grn_payload_force())


class Maliwan(Manufacturer):
    name = 'Maliwan'
    logo_file = 'Maliwan.png'

    def __init__(self):
        self.makes = {
            'weapons': [Guntypes.PISTOL, Guntypes.SMG, Guntypes.SNIPER, Guntypes.LAUNCHER],
            'grenades': [],
            'shield': Shieldtypes.BALANCED,
            'relics': []
        }
        self.weapon_traits = {
            'primary': [trait_maliwan_elemental(), trait_proliferation(), trait_mode_switch()],
            'secondary': []
        }
        self.shield_traits = {
            'tag': shd_tag_energy(),
            'parts': [shd_part_health(), trait_non_elemental()]
        }

    def make_random_gun(self, dice_roll):
        table = {
            (1, 3):  self.makes['weapons'][0],  # Pistol
            (4, 6):  self.makes['weapons'][1],  # Smg
            (7, 9): self.makes['weapons'][2],   # Sniper Rifle
            (10, 12): self.makes['weapons'][3]  # Rocket Launcher
        }

        return lookup_in_table(table, dice_roll)

    def make_random_shield(self):
        starting_parts = {
            (1, 3): shd_part_spike(),
            (4, 6): shd_part_nova()
        }
        d6 = Dice.from_string('1d6')
        starting_part = lookup_in_table(starting_parts, d6.roll())

        return self.makes['shield'], self.shield_traits['tag'], [starting_part, trait_maliwan_elemental()]

    def edit_grenade(self, grenade_obj):
        # Delivery Mechanism: Any
        # Starting Part: Elemental
        grenade_obj.delivery_system = grenade_delivery_mechanism[Dice.from_string('1d6').roll()]
        grenade_obj.parts.append(grn_payload_elemental())


class Torgue(Manufacturer):
    name = 'Torgue'
    logo_file = 'Torgue.png'

    def __init__(self):
        self.makes = {
            'weapons': [Guntypes.PISTOL, Guntypes.RIFLE, Guntypes.SHOTGUN, Guntypes.LAUNCHER],
            'grenades': [],
            'shield': Shieldtypes.BALANCED,
            'relics': []
        }
        self.weapon_traits = {
            'primary': [trait_boom()],
            'secondary': [trait_splasher(), trait_explosions(), trait_concussive()]
        }
        self.shield_traits = {
            'tag': shd_tag_alloy(),
            'parts': []
        }

    def make_random_gun(self, dice_roll):
        table = {
            (1, 3):  self.makes['weapons'][0],  # Pistol
            (4, 6):  self.makes['weapons'][1],  # Combat Rifle
            (7, 9): self.makes['weapons'][2],   # Shotgun
            (10, 12): self.makes['weapons'][3]  # Rocket Launcher
        }

        return lookup_in_table(table, dice_roll)

    def pick_secondary_weapon_trait(self, roll):
        table = {
            (1, 2): self.weapon_traits['secondary'][0],
            (3, 4): self.weapon_traits['secondary'][1],
            (5, 6): self.weapon_traits['secondary'][2]
        }

        return self.roll_for_secondary_weapon_trait(roll, table)

    def make_random_shield(self):
        starting_parts = {
            (1, 3): shd_part_spike(),
            (4, 6): shd_part_nova()
        }
        d6 = Dice.from_string('1d6')
        starting_part = lookup_in_table(starting_parts, d6.roll())

        forced_explosive = trait_forced_element()
        forced_explosive.type = Explosive()

        return self.makes['shield'], self.shield_traits['tag'], [starting_part, forced_explosive]

    def edit_grenade(self, grenade_obj):
        # Delivery Mechanism: Any
        # Starting Part: Nuke or Large
        grenade_obj.delivery_system = grenade_delivery_mechanism[Dice.from_string('1d6').roll()]
        starting_part = {
            (1, 3): grn_payload_large(),
            (4, 6): grn_payload_nuke()
        }

        grenade_obj.parts.append(lookup_in_table(starting_part, Dice.from_string('1d6').roll()))


class Pangolin(Manufacturer):
    name = 'Pangolin'
    logo_file = 'Pangolin.png'

    def __init__(self):
        self.makes = {
            'weapons': [Guntypes.PISTOL, Guntypes.RIFLE, Guntypes.SHOTGUN],
            'grenades': [],
            'shield': Shieldtypes.HIGHCAPACITY,
            'relics': []
        }
        self.weapon_traits = {
            'primary': [trait_do_no_harm(), trait_caseless_ammunition()],
            'secondary': [trait_charge(), trait_drain()]
        }
        self.shield_traits = {
            'tag': shd_tag_energy(),
            'parts': [shd_part_turtle()]
        }

    def make_random_gun(self, dice_roll):
        table = {
            (1, 4):  self.makes['weapons'][0],  # Pistol
            (5, 8):  self.makes['weapons'][1],  # Combat Rifle
            (9, 12): self.makes['weapons'][2],   # Shotgun
        }

        return lookup_in_table(table, dice_roll)

    def pick_secondary_weapon_trait(self, roll):
        table = {
            (1, 3): self.weapon_traits['secondary'][0],
            (4, 6): self.weapon_traits['secondary'][1],
        }

        return self.roll_for_secondary_weapon_trait(roll, table)

    def make_random_shield(self):
        return self.makes['shield'], self.shield_traits['tag'], self.shield_traits['parts']

    def edit_grenade(self, grenade_obj):
        # Delivery Mechanism: Any
        # Starting Part: Generator
        grenade_obj.delivery_system = grenade_delivery_mechanism[Dice.from_string('1d6').roll()]
        grenade_obj.parts.append(grn_payload_generator())


class Tediore(Manufacturer):
    name = 'Tediore'
    logo_file = 'Tediore.png'

    def __init__(self):
        self.makes = {
            'weapons': [Guntypes.PISTOL, Guntypes.SMG, Guntypes.SHOTGUN, Guntypes.LAUNCHER],
            'grenades': [],
            'shield': Shieldtypes.FAST,
            'relics': []
        }
        self.weapon_traits = {
            'primary': [trait_fire_and_forget(), trait_compact()],
            'secondary': [trait_turret(), trait_bomb()]
        }
        self.shield_traits = {
            'tag': shd_tag_energy(),
            'parts': [shd_part_recharge()]
        }

    def make_random_gun(self, dice_roll):
        table = {
            (1, 3):  self.makes['weapons'][0],  # Pistol
            (4, 6):  self.makes['weapons'][1],  # Smg
            (7, 9): self.makes['weapons'][2],   # Shotgun
            (10, 12): self.makes['weapons'][3]  # Rocket Launcher
        }

        return lookup_in_table(table, dice_roll)

    def pick_secondary_weapon_trait(self, roll):
        table = {
            (1, 3): self.weapon_traits['secondary'][0],
            (4, 6): self.weapon_traits['secondary'][1],
        }

        return self.roll_for_secondary_weapon_trait(roll, table)

    def make_random_shield(self):
        return self.makes['shield'], self.shield_traits['tag'], self.shield_traits['parts']

    def edit_grenade(self, grenade_obj):
        # Delivery Mechanism: Lobbed
        # Starting Part: Sticky
        grenade_obj.delivery_system = grn_delivery_lobbed()
        grenade_obj.parts.append(grn_payload_sticky())


class Vladof(Manufacturer):
    name = 'Vladof'
    logo_file = 'Vladof.png'

    def __init__(self):
        self.makes = {
            'weapons': [Guntypes.PISTOL, Guntypes.RIFLE, Guntypes.SNIPER, Guntypes.LAUNCHER],
            'grenades': [],
            'shield': Shieldtypes.BALANCED,
            'relics': []
        }
        self.weapon_traits = {
            'primary': [trait_wall_of_lead(), trait_extended_mags(), trait_endless_fire()],
            'secondary': [trait_grenade_launcher(), trait_taser(), trait_bipod()]
        }
        self.shield_traits = {
            'tag': shd_tag_energy(),
            'parts': []
        }

    def make_random_gun(self, dice_roll):
        table = {
            (1, 3):  self.makes['weapons'][0],  # Pistol
            (4, 6):  self.makes['weapons'][1],  # Combat Rifle
            (7, 9): self.makes['weapons'][2],   # Sniper
            (10, 12): self.makes['weapons'][3]  # Rocket Launcher
        }

        return lookup_in_table(table, dice_roll)

    def pick_secondary_weapon_trait(self, roll):
        table = {
            (1, 3): self.weapon_traits['secondary'][0],
            (4, 6): self.weapon_traits['secondary'][1],
        }

        return self.roll_for_secondary_weapon_trait(roll, table)

    def make_random_shield(self):
        starting_parts = {
            (1, 3): shd_part_absorb(),
            (4, 6): shd_part_reflect()
        }
        d6 = Dice.from_string('1d6')
        starting_part = lookup_in_table(starting_parts, d6.roll())

        return self.makes['shield'], self.shield_traits['tag'], [starting_part]

    def edit_grenade(self, grenade_obj):
        # Delivery Mechanism: Any
        # Starting Part: Puddle
        grenade_obj.delivery_system = grenade_delivery_mechanism[Dice.from_string('1d6').roll()]

        starting_part = {
            1: grn_payload_puddle_blight(),
            2: grn_payload_puddle_chiller(),
            3: grn_payload_puddle_corrupter(),
            4: grn_payload_puddle_flamer(),
            5: grn_payload_puddle_slagger(),
            6: grn_payload_puddle_tesla(),
        }
        grenade_obj.parts.append(starting_part[Dice.from_string('1d6').roll()])


class Eridian(Manufacturer):
    name = 'Eridian'
    logo_file = 'Eridian.png'

    def __init__(self):
        self.makes = {
            'weapons': [],
            'shields': [],
            'relics': []
        }
        self.weapon_traits = {
            'primary': [trait_reverse_engineer(), trait_alien_ammo()],
            'secondary': []
        }
        self.shield_traits = {
            'tag': None,
            'parts': [shd_trait_reverse_engineer(), shd_trait_symbiotic()]
        }

    def gun_part_exception(self, gun):
        if gun.manufacturer == Manufacturers.ERIDIAN:
            # Apply Eridian Primary Traits
            eridian_traits = [trait for trait in self.weapon_traits['primary']]
            for trait in eridian_traits:
                trait.attach(gun)

            # Apply Eridian Gun Type Trait
            eridian_gun_traits = {
                Guntypes.PISTOL: trait_dart(),
                Guntypes.SMG: trait_plasma_caster(),
                Guntypes.SHOTGUN: trait_splat(),
                Guntypes.RIFLE: trait_blaster(),
                Guntypes.SNIPER: trait_railer(),
                Guntypes.LAUNCHER: trait_plasma_cannon()
            }

            trait = eridian_gun_traits[gun.gun_type]
            trait.attach(gun)

    def pick_secondary_weapon_trait(self, roll):
        return


class Manufacturers:
    ANSHIN = Anshin()
    ATLAS = Atlas()
    BANDIT = Bandit()
    DAHL = Dahl()
    ERIDIAN = Eridian()
    HYPERION = Hyperion()
    JAKOBS = Jakobs()
    MALIWAN = Maliwan()
    PANGOLIN = Pangolin()
    TEDIORE = Tediore()
    TORGUE = Torgue()
    VLADOF = Vladof()


manufacturer_table = {
    1: Manufacturers.ANSHIN,
    2: Manufacturers.ATLAS,
    3: Manufacturers.BANDIT,
    4: Manufacturers.ERIDIAN,
    5: Manufacturers.DAHL,
    6: Manufacturers.HYPERION,
    7: Manufacturers.JAKOBS,
    8: Manufacturers.MALIWAN,
    9: Manufacturers.PANGOLIN,
    10: Manufacturers.TEDIORE,
    11: Manufacturers.TORGUE,
    12: Manufacturers.VLADOF
}
