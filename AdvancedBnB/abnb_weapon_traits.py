import math

from util import Modifier
from util import Dice

from .abnb_element import Explosive
from util import Rarity

# Anshin - Primary
class trait_do_no_harm(Modifier):
    name = 'Do No Harm'
    effect = '-1 Hit on Glancing, Solid & Penetrating Attacks (to a minimum of 1)'

    def apply(self, gun):
        for atk in ['glance', 'solid', 'penetrate']:
            if gun.mod_stats['hits_crits'][atk]['hits'] > 1:
                gun.mod_stats['hits_crits'][atk]['hits'] -= 1

class trait_caseless_ammunition(Modifier):
    name = 'Caseless Ammunition'
    effect = '+1 Mag Size, +1 on Reload Checks'

    # TODO: How to integrate Reload Checks?
    def apply(self, gun):
        gun.mod_stats['mag_size'] += 1
        gun.mod_stats.setdefault('mods', {}).setdefault('reload_check', 0)
        gun.mod_stats['mods']['reload_check'] += 1

# Anshin - Secondary
healing = {
    Rarity.COMMON: 2,
    Rarity.UNCOMMON: 4,
    Rarity.RARE: 6,
    Rarity.EPIC: 8,
    Rarity.LEGENDARY: 10,
    Rarity.PEARLESCENT: 12
}

class trait_medic(Modifier):
    name = 'Medic'
    effect = 'When you Target an Ally, they regain Health.'
    situational = True

    def to_text(self, gun):
        amount = healing[gun.rarity]

        return f"When you Target an Ally, they regain Health ({amount}/Hit, {amount*2}/Crit)."


class trait_vampire(Modifier):
    name = 'Vampire'
    effect = 'When you Damage an Enemy, you regain Health.'
    situational = True

    def to_text(self, gun):
        amount = healing[gun.rarity]

        return f"When you Damage an Enemy, you regain Health ({amount}/Hit, {amount * 2}/Crit)."

# Atlas - Primary
high_quality = {
    Rarity.COMMON: {'dmg_mod': 1},
    Rarity.UNCOMMON: {'dmg_mod': 2, 'reload_check': 1},
    Rarity.RARE: {'dmg_mod': 3, 'acc_mod': 1, 'reload_check': 1},
    Rarity.EPIC: {'dmg_mod': 4, 'acc_mod': 1, 'reload_check': 2},
    Rarity.LEGENDARY: {'dmg_mod': 5, 'acc_mod': 1, 'reload_check': 2},
    Rarity.PEARLESCENT: {'dmg_mod': 6, 'acc_mod': 2, 'reload_check': 3},
}

class trait_high_quality(Modifier):
    name = 'High Quality'
    effect = 'Improved Parts on Average.'

    def apply(self, gun):
        for k, v in high_quality[gun.rarity].items():
            gun.mod_stats.setdefault('mods', {}).setdefault(k, 0)
            gun.mod_stats['mods'][k] += v

    def to_text(self, gun):
        bonus = high_quality[gun.rarity]

        str = f"Improved Parts on Average: +{bonus['dmg_mod']} DMG MOD"
        if 'acc_mod' in bonus:
            str += f", +{bonus['acc_mod']} ACC MOD"
        if 'reload_check' in bonus:
            str += f", +{bonus['reload_check']} Reload Check"
        str += '.'

        return str

class trait_heavy_mags(Modifier):
    name = 'Heavy Mags'
    effect = '+1 Mag Size, -1 Movement.'

    def apply(self, gun):
        gun.mod_stats['mag_size'] += 1
        gun.mod_stats.setdefault('mods', {}).setdefault('movement', 0)
        gun.mod_stats['mods']['movement'] -= 1

class trait_lock_on(Modifier):
    name = 'Lock On'
    effect = 'In place of a Ranged Attack, fire a Homing Dart at a target. For the next 2 Turns, Attacks with this weapon against that target will treat an Accuracy Roll of 7 or lower (after Mods) as a Solid Attack.'
    situational = True

class trait_non_elemental(Modifier):
    name = 'Non Elemental'
    effect = f"This Gun can't be Elemental."

    def apply(self, gun):
        gun.forced_non_elemental = True

# Bandit - Primary
class trait_big_mags(Modifier):
    name = 'Big Mags'
    effect = '+3 Mag Size, +2 Fumble Range.'

    def apply(self, gun):
        gun.mod_stats['mag_size'] += 3
        gun.mod_stats.setdefault('mods', {}).setdefault('fumble_range', 0)
        gun.mod_stats['mods']['fumble_range'] += 2

class trait_pointy(Modifier):
    name = 'Pointy'
    effect = "Always has the Bayonet Accessory. This part doesn't count towards the maximum number of Gun Parts."


overheat = {
    Rarity.COMMON: '1d4',
    Rarity.UNCOMMON: '1d6',
    Rarity.RARE: '1d8',
    Rarity.EPIC: '1d10',
    Rarity.LEGENDARY: '1d12',
    Rarity.PEARLESCENT: '2d8'
}
class trait_overheat(Modifier):
    name = 'Overheat'
    effect = "When Reloading: You and Adjacent Targets take Elemental Damage (Same Element as the Gun, Incendiary if Non Elemental)."
    situational = True

    def to_text(self, gun):
        dice_multi = 1
        if gun.tier >= 4:
            dice_multi = 2
        if gun.tier >= 7:
            dice_multi = 3
        if gun.tier >= 10:
            dice_multi = 4

        dmg_die = Dice.from_string(overheat[gun.rarity])
        dmg_die.count *= dice_multi

        str = f"When Reloading: You and Adjacent Targets take {dmg_die} Elemental Damage (Same Element as the Gun, Incendiary if Non Elemental)."

        return str

# Dahl - Primary
class trait_steady_aim(Modifier):
    name = 'Steady Aim'
    effect = "While ADS: Burst +1."
    situational = True

tacticool = {
    Rarity.COMMON: {'fire_modes': 1, 'scopes': 1},
    Rarity.UNCOMMON: {'fire_modes': 1, 'scopes': 1, 'accessories': 1},
    Rarity.RARE: {'fire_modes': 2, 'scopes': 1, 'accessories': 1},
    Rarity.EPIC: {'fire_modes': 2, 'scopes': 2, 'accessories': 1},
    Rarity.LEGENDARY: {'fire_modes': 2, 'scopes': 2, 'accessories': 2},
    Rarity.PEARLESCENT: {'fire_modes': 2, 'scopes': 2, 'accessories': 3},
}

class trait_Tacticool(Modifier):
    name = 'Tacti-cool'
    effect = "Gains extra Gun Parts."

    def to_text(self, gun):
        bonus = tacticool[gun.rarity]

        str = f"{bonus['fire_modes']} Fire Modes, {bonus['scopes']} Scope{'s' if bonus['scopes'] > 1 else ''}"
        if 'accessories' in bonus:
            str += f", +{bonus['accessories']} Accessories"
        str += '.'

        return str

class trait_reconfigure(Modifier):
    name = 'Reconfigure'
    effect = "Swap between Fire Modes and/or Scopes. SPD 10 Check."
    situational = True

# Dahl - Fire Modes
class trait_fm_single_fire(Modifier):
    name = '(Fire Mode) Single Fire'
    effect = "+1 Range, +1 ACC MOD."

class trait_fm_burst_fire(Modifier):
    name = '(Fire Mode) Burst Fire'
    effect = "+1 Burst, -3 ACC MOD, Consumes 2 Ammo."

class trait_fm_full_auto(Modifier):
    name = '(Fire Mode) Full Auto'
    effect = "+2 Burst, -8 ACC MOD, Consumes 3 Ammo."

# Hyperion - Primary
recoil_control = {
    Rarity.COMMON: {'acc_mod': 1, 'dmg_mod': -2},
    Rarity.UNCOMMON: {'acc_mod': 2, 'dmg_mod': -2},
    Rarity.RARE: {'acc_mod': 3, 'dmg_mod': -2},
    Rarity.EPIC: {'acc_mod': 4, 'dmg_mod': -2},
    Rarity.LEGENDARY: {'acc_mod': 5, 'dmg_mod': -2},
    Rarity.PEARLESCENT: {'acc_mod': 6, 'dmg_mod': -2},
}
class trait_recoil_control(Modifier):
    name = 'Recoil Control'
    effect = 'Increased Accuracy.'

    def apply(self, gun):
        bonus = recoil_control[gun.rarity]

        for k, v in bonus.items():
            gun.mod_stats.setdefault('mods', {}).setdefault(k, 0)
            gun.mod_stats['mods'][k] += v


    def to_text(self, gun):
        bonus = recoil_control[gun.rarity]

        str = f"+{bonus['acc_mod']} ACC MOD, -2 DMG MOD."

# TODO: Move to Tables (circular import issue)
shield_stats_balanced = {
    1: {'capacity': 30, 'charge_rate': 10},
    2: {'capacity': 45, 'charge_rate': 15},
    3: {'capacity': 60, 'charge_rate': 20},
    4: {'capacity': 75, 'charge_rate': 25},
    5: {'capacity': 90, 'charge_rate': 30},
    6: {'capacity': 105, 'charge_rate': 35},
    7: {'capacity': 120, 'charge_rate': 40},
    8: {'capacity': 135, 'charge_rate': 45},
    9: {'capacity': 150, 'charge_rate': 50},
    10: {'capacity': 165, 'charge_rate': 55},
}
class trait_gun_shield(Modifier):
    name = 'Gun Shield'
    effect = 'While ADS: Gun provides an Extra Energy Shield. Capacity is half of a Balanced Shield. Recharges After every Encounter.'
    situational = True

    def to_text(self, gun):
        shield_cap = shield_stats_balanced[gun.tier]['charge_rate']
        shield_cap = math.floor(shield_cap / 2)

        str = f"While ADS: Gun gives an Extra Shield (Capacity: {shield_cap}). Recharges after Encounter."
        return str

# Hyperion - Gun Shield Parts
class trait_shield_amp(Modifier):
    name = '(Amped) Gun Shield'
    effect = 'While Gun Shield is Full: Next Ranged Attack +1 Hit. Gun Shield takes 10 DMG.'

class trait_shield_genesis(Modifier):
    name = '(Genesis) Gun Shield'
    effect = 'When taking Ranged DMG: Roll a d100. On 90+, DMG=0 and gain 1 Ammo.'

class trait_shield_redirect(Modifier):
    name = '(Redirect) Gun Shield'
    effect = 'When taking Ranged DMG: Roll a d100. On 90+, DMG instead is Reflected back to the Attacker.'

# Jakobs - Primary
head_hunter = {
    Rarity.COMMON: {'acc_mod': 2, 'crit_dmg': 2},
    Rarity.UNCOMMON: {'acc_mod': 2, 'crit_dmg': 4},
    Rarity.RARE: {'acc_mod': 2, 'crit_dmg': 6},
    Rarity.EPIC: {'acc_mod': 2, 'crit_dmg': 8},
    Rarity.LEGENDARY: {'acc_mod': 2, 'crit_dmg': 10},
    Rarity.PEARLESCENT: {'acc_mod': 2, 'crit_dmg': 12},
}

class trait_head_hunter(Modifier):
    name = 'Head Hunter'
    effect = "Increased Crit DMG and ACC MOD."

    def apply(self, gun):
        bonus = head_hunter[gun.rarity]

        for k, v in bonus.items():
            gun.mod_stats.setdefault('mods', {}).setdefault(k, 0)
            gun.mod_stats['mods'][k] += v

    def to_text(self, gun):
        bonus = head_hunter[gun.rarity]

        str = f"+{bonus['acc_mod']} ACC MOD, +{bonus['crit_dmg']} Crit DMG."
        return str

# For Non-Elemental trait See trait_non_elemental

class trait_cumbersome(Modifier):
    name = 'Cumbersome'
    effect = '-1 Mag Size'

    def apply(self, gun):
        if gun.mod_stats['mag_size'] > 1:
            gun.mod_stats['mag_size'] -= 1

# Jakobs - Secondary
class trait_fan_the_hammer(Modifier):
    name = 'Fan the Hammer'
    effect = "You can use your SPD MOD instead of ACC MOD for Accuracy rolls. If you do, gain an extra Attack that has -3 Accuracy."
    situational = True

class trait_ricochet(Modifier):
    name = 'Ricochet'
    effect = "Crits also deal DMG to one Adjacent Enemy."
    situational = True

class trait_percise(Modifier):
    name = 'Percise'
    effect = "On Penetrating and Lethal Attacks: +1 Crit."
    situational = True

# Maliwan - Primary

class trait_elemental(Modifier):
    name = 'Elemental'
    effect = 'Always Elemental (Non-Explosive).'

    def apply(self, gun):
        #TODO: Make sure Explosive Element is left out
        gun.forced_elemental = True

class trait_proliferation(Modifier):
    name = 'Proliferation'
    effect = 'Improved Elemental Scaling. Increase Gun generation Elemental rolls and when applying Elemental Status Effects.'
    situational = True

    proliferation = {
        Rarity.COMMON: {'n_rolls': 1, 'roll_bonus': 0},
        Rarity.UNCOMMON: {'n_rolls': 1, 'roll_bonus': 10},
        Rarity.RARE: {'n_rolls': 2, 'roll_bonus': 10},
        Rarity.EPIC: {'n_rolls': 2, 'roll_bonus': 20},
        Rarity.LEGENDARY: {'n_rolls': 2, 'roll_bonus': 30},
        Rarity.PEARLESCENT: {'n_rolls': 2, 'roll_bonus': 40}
    }

    def apply(self, gun):
        bonus = self.proliferation[gun.rarity]

        gun.mod_stats.setdefault('mods', {}).setdefault('status_effect_chance', 0)
        gun.mod_stats['mods']['status_effect_chance'] += bonus['roll_bonus']

        gun.elemental_roll = bonus

    def to_text(self, gun):
        bonus = self.proliferation[gun.rarity]

        if bonus['roll_bonus'] != 0:
            return f"+{bonus['roll_bonus']}% Elemental Status Effect Chance."
        else:
            self.situational = False

class trait_mode_switch(Modifier):
    name = 'Mode Switch'
    effect = 'Rare and higher Rarity can swap between 2 elements. SPD 10 Check.'
    situational = True
    
    def apply(self, gun):
        # Remove trait when rarity is below Rare. Doesn't do anything for lower grade Guns
        if gun.rarity in [Rarity.COMMON, Rarity.UNCOMMON]:
            idx = gun.traits.index(self)
            gun.traits.pop(idx)

    def to_text(self, gun):
        return f"Can swap between 2 Elements. SPD 10 Check."

# Torgue - Primary
class trait_boom(Modifier):
    name = 'Boom!'
    effect = 'Always Explosive, only Explosive, at the cost of Accuracy.'

    boom = {
        Rarity.COMMON: {'knock_back': 5, 'acc_mod': -4},
        Rarity.UNCOMMON: {'knock_back': 10, 'acc_mod': -3},
        Rarity.RARE: {'knock_back': 15, 'acc_mod': -2},
        Rarity.EPIC: {'knock_back': 20, 'acc_mod': -1},
        Rarity.LEGENDARY: {'knock_back': 25, 'acc_mod': 0},
        Rarity.PEARLESCENT: {'knock_back': 30, 'acc_mod': 0},
    }

    def apply(self, gun):


        # Apply bonus stats
        bonus = self.boom[gun.rarity]

        gun.mod_stats.setdefault('mods', {}).setdefault('splash', 0)
        gun.mod_stats['mods']['splash'] = 1

        for k, v in bonus.items():
            gun.mod_stats.setdefault('mods', {}).setdefault(k, 0)
            gun.mod_stats['mods'][k] += v

    def finalize(self, gun):
        # Make sure Gun is Explosive and ONLY Explosive
        gun.manufacturer.gun_part_exception(gun)
        if len(gun.elements) == 0:
            gun.elements.append(Explosive())

    def to_text(self, gun):
        bonus = self.boom[gun.rarity]

        str = f"Splash. +{bonus['knock_back']}% Knock Back."
        if bonus['acc_mod'] != 0:
            str += f" -{bonus['acc_mod']} ACC MOD."


class trait_splasher(Modifier):
    name = 'Splasher!'
    effect = 'Deals Full Splash Damage.'
    situational = True


class trait_explosions(Modifier):
    name = 'Explosions!?'
    effect = 'Splash Range +1.'

    def apply(self, gun):
        gun.mod_stats.setdefault('mods', {}).setdefault('splash_range', 0)
        gun.mod_stats['mods']['splash_range'] += 1


class trait_concussive(Modifier):
    name = 'Concussive!'
    effect = '+25% Knock Back.'

    def apply(self, gun):
        gun.mod_stats.setdefault('mods', {}).setdefault('knock_back', 0)
        gun.mod_stats['mods']['knock_back'] += 25


# Pangolin - Primary
# See Anshin Primary Traits

# Pangolin - Secondary
battery = {
    Rarity.COMMON: 2,
    Rarity.UNCOMMON: 4,
    Rarity.RARE: 6,
    Rarity.EPIC: 8,
    Rarity.LEGENDARY: 10,
    Rarity.PEARLESCENT: 12
}

class trait_charge(Modifier):
    name = 'Charge'
    effect = 'When you Target an Ally, they regain Shields.'
    situational = True

    def to_text(self, gun):
        amount = healing[gun.rarity]

        return f"When you Target an Ally, they regain Shields ({amount}/Hit, {amount * 2}/Crit)."

class trait_drain(Modifier):
    name = 'Drain'
    effect = 'When you Damage an Enemy, you regain Shields.'
    situational = True

    def to_text(self, gun):
        amount = healing[gun.rarity]

        return f"When you Damage an Enemy, you regain Shields ({amount}/Hit, {amount * 2}/Crit)."

# Tediore - Primary
class trait_fire_and_forget(Modifier):
    name = 'Fire & Forget'
    effect = 'When you Reload this Gun, you Throw it away instead and deal Damage.'
    situational = True

    fire_and_forget = {
        Rarity.COMMON: Dice(1,4),
        Rarity.UNCOMMON: Dice(1,6),
        Rarity.RARE: Dice(1,8),
        Rarity.EPIC: Dice(1,10),
        Rarity.LEGENDARY: Dice(1,12),
        Rarity.PEARLESCENT: Dice(2,8)
    }

    def to_text(self, gun):
        bonus_dice = self.fire_and_forget[gun.rarity]
        bonus_dice.count *= gun.tier

        str = f"When you Reload this Gun: You Throw it away instead, dealing {bonus_dice} DMG."
        return str


class trait_compact(Modifier):
    name = 'Compact'
    effect = '-2 Mag Size (minimum of 1), +4 on Reload and Swap Checks.'

    def apply(self, gun):
        gun.mod_stats['mag_size'] -= 2
        if gun.mod_stats['mag_size'] < 1:
            gun.mod_stats['mag_size'] = 1

        gun.mod_stats.setdefault('mods', {}).setdefault('reload_check', 0)
        gun.mod_stats['mods']['reload_check'] += 4

        gun.mod_stats.setdefault('mods', {}).setdefault('swap_check', 0)
        gun.mod_stats['mods']['swap_check'] += 4


# Tediore - Secondary
class trait_turret(Modifier):
    name = 'Turret'
    effect = 'When Thrown: the Gun turns into a Turret for 2 turns. Once per turn the Turret shoots the closest Enemy.'
    situational = True


class trait_bomb(Modifier):
    name = 'Bomb'
    effect = 'When Thrown: the Gun turns into a Grenade dealing Splash Damage in the same Element as the Gun (Explosive if Non Elemental).'
    situational = True


# Vladof - Primary
class trait_wall_of_lead(Modifier):
    name = 'Wall of Lead'
    effect = 'Extra Attacks at the cost of Accuracy.'

    fire_and_forget = {
        Rarity.COMMON: {'extra_attack': 1, 'acc_mod': -4},
        Rarity.UNCOMMON: {'extra_attack': 1, 'acc_mod': -3},
        Rarity.RARE: {'extra_attack': 1, 'acc_mod': -2},
        Rarity.EPIC: {'extra_attack': 1, 'acc_mod': -1},
        Rarity.LEGENDARY: {'extra_attack': 1},
        Rarity.PEARLESCENT: {'extra_attack': 1, 'extra_movement': 1},
    }

    def apply(self, gun):
        bonus = self.fire_and_forget[gun.rarity]

        for k, v in bonus.items():
            gun.mod_stats.setdefault('mods', {}).setdefault(k, 0)
            gun.mod_stats['mods'][k] += v


class trait_extended_mags(Modifier):
    name = 'Extended Mags'
    effect = '+2 Mag Size.'

    def apply(self, gun):
        gun.mod_stats['mag_size'] += 2


class trait_endless_fire(Modifier):
    name = 'Endless Fire'
    effect = "On an Accuracy Roll of 5, 10, 15 or 20 (before Mods): this Attack doesn't consume Ammo."
    situational = True


# Vladof - Secondary
class trait_grenade_launcher(Modifier):
    name = 'Grenade Launcher'
    effect = '(1/Encounter) Shoot a 1d8/Tier Explosive Grenade at a point within 5 squares.'
    situational = True

    def to_text(self, gun):
        dmg_dice = Dice(1, 8)
        dmg_dice.count *= gun.tier

        return f"(1/Encounter): Shoot a {dmg_dice} Explosive Grenade at a point within 5 squares."


class trait_taser(Modifier):
    name = 'Taser'
    effect = '(1/Encounter) When used: Each Enemy within a 3 square Cone takes 1d4/Tier Shock Damage and is Dazed.'
    situational = True

    def to_text(self, gun):
        dmg_dice = Dice(1, 4)
        dmg_dice.count *= gun.tier

        return f"(1/Encounter) When used: Each Enemy within a 3 square Cone takes {dmg_dice} Shock Damage and is Dazed."


class trait_bipod(Modifier):
    name = 'Bipod'
    effect = 'While Active: +2 ACC MOD on Ranged Attacks, -1 Movement. You can (de)activate the Bipod once on your turn.'
    situational = True


# Eridian - Primary
class trait_reverse_engineer(Modifier):
    name = 'Reverse Engineer'
    effect = 'This Alien Gun is made using a Gun from another Manufacturer as a base.'

class trait_alien_ammo(Modifier):
    name = 'Alien Ammo'
    effect = 'Consumes 2 Ammo per Attack, +2 Mag Size.'

    def apply(self, gun):
        gun.mod_stats['mag_size'] += 2

        gun.mod_stats.setdefault('mods', {}).setdefault('ammo_per_attack', 0)
        gun.mod_stats['mods']['ammo_per_attack'] += 1

# Eridian - Gun Type Traits
class trait_dart(Modifier):
    name = 'Dart'
    effect = '+2 Range, Ignores Cover.'
    situational = True

    def apply(self, gun):
        gun.mod_stats['range'] += 2

    def to_text(self, gun):
        return 'Ignores Cover'


class trait_plasma_caster(Modifier):
    name = 'Plasma Caster'
    effect = '+1 Range, +2 Burst.'

    def apply(self, gun):
        gun.mod_stats['range'] += 1

        for atk in ['glance', 'solid', 'penetrate']:
            gun.mod_stats['hits_crits'][atk]['hits'] += 2


class trait_splat(Modifier):
    name = 'Splat'
    effect = '-1 Range, Splash, +1 Burst.'

    def apply(self, gun):
        gun.mod_stats['range'] -= 1

        for atk in ['glance', 'solid', 'penetrate']:
            gun.mod_stats['hits_crits'][atk]['hits'] += 1

        gun.mod_stats.setdefault('mods', {}).setdefault('splash', 0)
        gun.mod_stats['mods']['splash'] = 1


class trait_blaster(Modifier):
    name = 'Blaster'
    effect = '+1 Range, +2 Burst, +3 Mag Size.'

    def apply(self, gun):
        gun.mod_stats['range'] += 1

        for atk in ['glance', 'solid', 'penetrate']:
            gun.mod_stats['hits_crits'][atk]['hits'] += 2

        gun.mod_stats['mag_size'] += 3


class trait_railer(Modifier):
    name = 'Railer'
    effect = '+2 Range, +1 Burst, Pierces 1 Enemy or Object.'
    situational = True

    def apply(self, gun):
        gun.mod_stats['range'] += 2

        for atk in ['glance', 'solid', 'penetrate']:
            gun.mod_stats['hits_crits'][atk]['hits'] += 1

    def to_text(self, gun):
        return f"Pierces 1 Enemy or Object."


class trait_plasma_cannon(Modifier):
    name = 'Plasma Cannon'
    effect = '+1 Range, +1 Burst, +1 Splash Radius.'

    def apply(self, gun):
        gun.mod_stats['range'] += 1

        for atk in ['glance', 'solid', 'penetrate']:
            gun.mod_stats['hits_crits'][atk]['hits'] += 1

        gun.mod_stats.setdefault('mods', {}).setdefault('splash_range', 0)
        gun.mod_stats['mods']['splash_range'] += 1




