from .abnb_element import FusionElement
from .abnb_guntypes import Guntypes
from .abnb_weapon_parts import weapon_accessories_table
from .abnb_weapon_traits import *
from .abnb_shield_parts import *
from .abnb_shieldtypes import Shieldtypes
from .abnb_grenade_parts import *

from util import roll_on_table

class Manufacturer:
    name = ''

    def pick_secondary_weapon_trait(self, user_roll=False):
        return

    def roll_for_secondary_weapon_trait(self, table, user_roll=False):
        roll = Dice(1, 6).roll(user_roll)
        trait = roll_on_table(table, roll)
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

    def make_random_gun(self, dice_roll):
        table = {
            (1, 4):  self.makes['weapons'][0],  # Pistol
            (5, 8):  self.makes['weapons'][1],  # Smg
            (9, 12): self.makes['weapons'][2]   # Sniper
        }

        return roll_on_table(table, dice_roll)

    def pick_secondary_weapon_trait(self, user_roll=False):
        table = {
            (1, 3): self.weapon_traits['secondary'][0],
            (4, 6): self.weapon_traits['secondary'][1]
        }

        return self.roll_for_secondary_weapon_trait(table, user_roll=user_roll)

    def edit_shield(self, shield_obj):
        shield_obj.shield_type = self.makes['shield']
        shield_obj.tag = shd_tag_energy()
        shield_obj.parts.append(shd_part_adaptive())

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

    def make_random_gun(self, dice_roll):
        table = {
            (1, 4):  self.makes['weapons'][0],  # Combat Rifle
            (5, 8):  self.makes['weapons'][1],  # Pistol
            (9, 12): self.makes['weapons'][2]   # Rocket Launcher
        }

        return roll_on_table(table, dice_roll)

    def edit_shield(self, shield_obj):
        shield_obj.shield_type = self.makes['shield']
        shield_obj.tag = shd_tag_alloy()
        shield_obj.parts.append(shd_part_brimming())
        shield_obj.forced_non_elemental = True

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
            'primary': [trait_big_mags(), trait_pointy(), trait_overheat()],
            'secondary': []
        }

    def make_random_gun(self, dice_roll):
        table = {
            (1, 2):  self.makes['weapons'][0],  # Combat Rifle
            (3, 5):  self.makes['weapons'][1],  # Pistol
            (11, 12): self.makes['weapons'][2],  # Rocket Launcher
            (6, 8): self.makes['weapons'][3],  # Shotgun
            (9, 10): self.makes['weapons'][4]   # SMG
        }

        return roll_on_table(table, dice_roll)

    def gun_part_exception(self, gun):
        # Bandit weapons always spawn with a Bayonet Accessory. This does NOT count towards number of Gun Parts
        if gun.manufacturer == self:
            part = roll_on_table(weapon_accessories_table, 1)
            gun.parts.append(part)

    def edit_shield(self, shield_obj):
        shield_obj.shield_type = self.makes['shield']
        shield_obj.tag = shd_tag_alloy()
        shield_obj.parts.append(shd_part_roid())


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
            'primary': [trait_steady_aim(), trait_Tacticool(), trait_reconfigure()],
            'secondary': [trait_fm_single_fire(), trait_fm_burst_fire(), trait_fm_full_auto()]
        }

    def make_random_gun(self, dice_roll):
        table = {
            (1, 3):  self.makes['weapons'][0],  # Combat Rifle
            (4, 6):  self.makes['weapons'][1],  # Pistol
            (7, 9): self.makes['weapons'][2],  # Sniper Rifle
            (10, 12): self.makes['weapons'][3]   # Smg
        }

        return roll_on_table(table, dice_roll)

    def pick_secondary_weapon_trait(self, user_roll=False):
        table = {
            (1, 2): self.weapon_traits['secondary'][0],
            (3, 4): self.weapon_traits['secondary'][1],
            (5, 6): self.weapon_traits['secondary'][2]
        }

        return self.roll_for_secondary_weapon_trait(table, user_roll=user_roll)

    def gun_part_exception(self, gun):
        if gun.manufacturer == self:
            # Resolve 'Tacti-cool' Trait?
            bonus = tacticool[gun.rarity]

            gun.max_scopes = 2 # Dahl Guns might come with 2 scopes

            # Add Scopes
            for _ in range(bonus['scopes']):
                if gun.n_scopes >= gun.max_scopes:
                    break
                part = gun.pick_weapon_scope()
                gun.parts.append(part)
                gun.n_scopes += 1
                gun.n_parts += 1

            # Add Bonus Accessories
            if 'accessories' in bonus:
                for _ in range(bonus['accessories']):
                    part = gun.pick_weapon_accessory()
                    gun.parts.append(part)

            # Add Fire Modes
            for _ in range(bonus['fire_modes']):
                while True:
                    trait = self.pick_secondary_weapon_trait(gun.user_rolls)
                    if trait not in gun.traits:
                        gun.traits.append(trait)
                        break

    def edit_shield(self, shield_obj):
        shield_obj.shield_type = self.makes['shield']
        shield_obj.tag = shd_tag_energy()
        starting_part = {
            (1, 3): shd_part_charge_health(),
            (4, 6): shd_part_charge_shield()
        }
        d6 = Dice.from_string('1d6')
        shield_obj.parts.append(roll_on_table(starting_part, d6.roll()))

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

    def make_random_gun(self, dice_roll):
        table = {
            (1, 3):  self.makes['weapons'][0],  # Pistol
            (4, 6):  self.makes['weapons'][1],  # Smg
            (7, 9): self.makes['weapons'][2],   # Shotgun
            (10, 12): self.makes['weapons'][3]  # Sniper
        }

        return roll_on_table(table, dice_roll)

    def pick_secondary_weapon_trait(self, user_roll=False):
        table = {
            (1, 2): self.weapon_traits['secondary'][0],
            (3, 4): self.weapon_traits['secondary'][1],
            (5, 6): self.weapon_traits['secondary'][2]
        }

        return self.roll_for_secondary_weapon_trait(table, user_roll=user_roll)

    def edit_shield(self, shield_obj):
        shield_obj.shield_type = self.makes['shield']
        shield_obj.tag = shd_tag_energy()
        shield_obj.parts.append(shd_part_amp())

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

    def make_random_gun(self, dice_roll):
        table = {
            (1, 3):  self.makes['weapons'][0],  # Combat Rifle
            (4, 6):  self.makes['weapons'][1],  # Pistol
            (7, 9): self.makes['weapons'][2],   # Shotgun
            (10, 12): self.makes['weapons'][3]  # Sniper
        }

        return roll_on_table(table, dice_roll)

    def pick_secondary_weapon_trait(self, user_roll=False):
        table = {
            (1, 2): self.weapon_traits['secondary'][0],
            (3, 4): self.weapon_traits['secondary'][1],
            (5, 6): self.weapon_traits['secondary'][2]
        }

        return self.roll_for_secondary_weapon_trait(table, user_roll=user_roll)

    def edit_shield(self, shield_obj):
        shield_obj.shield_type = self.makes['shield']
        shield_obj.tag = shd_tag_bio()
        shield_obj.parts.append(shd_part_health())
        shield_obj.forced_non_elemental = True

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
            'primary': [trait_elemental(), trait_proliferation(), trait_mode_switch()],
            'secondary': []
        }

    def make_random_gun(self, dice_roll):
        table = {
            (1, 3):  self.makes['weapons'][0],  # Pistol
            (4, 6):  self.makes['weapons'][1],  # Smg
            (7, 9): self.makes['weapons'][2],   # Sniper Rifle
            (10, 12): self.makes['weapons'][3]  # Rocket Launcher
        }

        return roll_on_table(table, dice_roll)

    def edit_shield(self, shield_obj):
        shield_obj.shield_type = self.makes['shield']
        shield_obj.tag = shd_tag_energy()
        starting_part = {
            (1, 3): shd_part_spike(),
            (4, 6): shd_part_nova()
        }
        d6 = Dice.from_string('1d6')
        shield_obj.parts.append(roll_on_table(starting_part, d6.roll()))
        # Force an Element because of the Spike or Nova part, but make sure no more elements can be rolled after
        shield_obj.forced_elemental = True
        shield_obj.roll_for_element()
        shield_obj.forced_elemental = False
        shield_obj.forced_non_elemental = True

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

    def make_random_gun(self, dice_roll):
        table = {
            (1, 3):  self.makes['weapons'][0],  # Pistol
            (4, 6):  self.makes['weapons'][1],  # Combat Rifle
            (7, 9): self.makes['weapons'][2],   # Shotgun
            (10, 12): self.makes['weapons'][3]  # Rocket Launcher
        }

        return roll_on_table(table, dice_roll)

    def pick_secondary_weapon_trait(self, user_roll=False):
        table = {
            (1, 2): self.weapon_traits['secondary'][0],
            (3, 4): self.weapon_traits['secondary'][1],
            (5, 6): self.weapon_traits['secondary'][2]
        }

        return self.roll_for_secondary_weapon_trait(table, user_roll=user_roll)

    def gun_part_exception(self, gun):
        if gun.manufacturer == self:
            fixed_elements = []
            for element in gun.elements:
                print(element)
                if isinstance(element, Explosive):
                    fixed_elements.append(element)

                #if type(element) == FusionElement:
                if isinstance(element, FusionElement):
                    for sub_element in element.fusion_elements:
                        print(sub_element)
                        if isinstance(sub_element, Explosive):
                            fixed_elements.append(element)
                            break

            gun.elements = fixed_elements

    def edit_shield(self, shield_obj):
        shield_obj.shield_type = self.makes['shield']
        shield_obj.tag = shd_tag_alloy()
        starting_part = {
            (1, 3): shd_part_spike(),
            (4, 6): shd_part_nova()
        }
        d6 = Dice.from_string('1d6')
        shield_obj.parts.append(roll_on_table(starting_part, d6.roll()))
        # Force Explosive Element
        shield_obj.forced_elemental = True
        shield_obj.roll_for_element()
        shield_obj.forced_elemental = False
        shield_obj.forced_non_elemental = True

        # Check if Element is Explosive, else replace
        has_explosive = False
        for el in shield_obj.elements:
            if isinstance(el, FusionElement):
                for sub_el in el:
                    if isinstance(sub_el, Explosive):
                        has_explosive = True
            else:
                if isinstance(el, Explosive):
                    has_explosive = True

        if not has_explosive:
            shield_obj.elements = [Explosive()]


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

    def make_random_gun(self, dice_roll):
        table = {
            (1, 4):  self.makes['weapons'][0],  # Pistol
            (5, 8):  self.makes['weapons'][1],  # Combat Rifle
            (9, 12): self.makes['weapons'][2],   # Shotgun
        }

        return roll_on_table(table, dice_roll)

    def pick_secondary_weapon_trait(self, user_roll=False):
        table = {
            (1, 3): self.weapon_traits['secondary'][0],
            (4, 6): self.weapon_traits['secondary'][1],
        }

        return self.roll_for_secondary_weapon_trait(table, user_roll=user_roll)

    def edit_shield(self, shield_obj):
        shield_obj.shield_type = self.makes['shield']
        shield_obj.tag = shd_tag_energy()
        shield_obj.parts.append(shd_part_turtle())


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

    def make_random_gun(self, dice_roll):
        table = {
            (1, 3):  self.makes['weapons'][0],  # Pistol
            (4, 6):  self.makes['weapons'][1],  # Smg
            (7, 9): self.makes['weapons'][2],   # Shotgun
            (10, 12): self.makes['weapons'][3]  # Rocket Launcher
        }

        return roll_on_table(table, dice_roll)

    def pick_secondary_weapon_trait(self, user_roll=False):
        table = {
            (1, 3): self.weapon_traits['secondary'][0],
            (4, 6): self.weapon_traits['secondary'][1],
        }

        return self.roll_for_secondary_weapon_trait(table, user_roll=user_roll)

    def edit_shield(self, shield_obj):
        shield_obj.shield_type = self.makes['shield']
        shield_obj.tag = shd_tag_energy()
        shield_obj.parts.append(shd_part_recharge())


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

    def make_random_gun(self, dice_roll):
        table = {
            (1, 3):  self.makes['weapons'][0],  # Pistol
            (4, 6):  self.makes['weapons'][1],  # Combat Rifle
            (7, 9): self.makes['weapons'][2],   # Sniper
            (10, 12): self.makes['weapons'][3]  # Rocket Launcher
        }

        return roll_on_table(table, dice_roll)

    def pick_secondary_weapon_trait(self, user_roll=False):
        table = {
            (1, 3): self.weapon_traits['secondary'][0],
            (4, 6): self.weapon_traits['secondary'][1],
        }

        return self.roll_for_secondary_weapon_trait(table, user_roll=user_roll)

    def edit_shield(self, shield_obj):
        shield_obj.shield_type = self.makes['shield']
        shield_obj.tag = shd_tag_energy()
        starting_part = {
            (1, 3): shd_part_absorb(),
            (4, 6): shd_part_reflect()
        }
        d6 = Dice.from_string('1d6')
        shield_obj.parts.append(roll_on_table(starting_part, d6.roll()))


class Eridian(Manufacturer):
    name = 'Eridian'
    logo_file = 'Eridian.png'

    def __init__(self):
        self.makes = {
            'weapons': [],
            'grenades': [],
            'shields': [],
            'relics': []
        }
        self.weapon_traits = {
            'primary': [trait_reverse_engineer(), trait_alien_ammo()],
            'secondary': []
        }

    def gun_part_exception(self, gun):
        if gun.manufacturer == Manufacturers.ERIDIAN:
            # Apply Eridian Primary Traits
            eridian_traits = [trait for trait in self.weapon_traits['primary']]
            for trait in eridian_traits:
                gun.traits.append(trait)
                trait.apply(gun)

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
            gun.traits.append(trait)
            trait.apply(gun)

    def pick_secondary_weapon_trait(self, user_roll=False):
        table = {
            (1, 3): self.weapon_traits['secondary'][0],
            (4, 6): self.weapon_traits['secondary'][1],
        }
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

