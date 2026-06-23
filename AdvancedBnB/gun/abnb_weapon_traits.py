from util import EquipmentProperty
from util.common_modifiers import *

from AdvancedBnB.gun.abnb_weapon_modifiers import *

# Wrapper class
class WeaponTrait(EquipmentProperty):
    pass

# Anshin - Primary
class trait_do_no_harm(WeaponTrait):
    name = 'Do No Harm'
    effect = '-1 Hit on Glancing, Solid & Penetrating Attacks (to a minimum of 1)'

    def reload_modifiers(self):
        self.replace_modifiers([mod_burst(-1)])


class trait_caseless_ammunition(WeaponTrait):
    name = 'Caseless Ammunition'
    effect = '+1 Mag Size, +1 on Reload Checks'

    def reload_modifiers(self):
        self.replace_modifiers([
            mod_mag_size(1),
            mod_reload_check(1)
        ])


# Anshin - Secondary
class trait_medic(WeaponTrait):
    name = 'Medic'
    effect = 'When you Target an Ally, they regain Health.'

    def reload_modifiers(self):
        self.replace_modifiers([mod_medic()])


class trait_vampire(WeaponTrait):
    name = 'Vampire'
    effect = 'When you Damage an Enemy, you regain Health.'

    def reload_modifiers(self):
        self.replace_modifiers([mod_vampire()])

# Atlas - Primary
class trait_high_quality(WeaponTrait):
    name = 'High Quality'
    effect = 'Improved Parts on Average.'

    high_quality = {
        Rarity.COMMON: [mod_dmg_mod(1)],
        Rarity.UNCOMMON: [mod_dmg_mod(2), mod_reload_check(1)],
        Rarity.RARE: [mod_dmg_mod(3), mod_acc_mod(1), mod_reload_check(1)],
        Rarity.EPIC: [mod_dmg_mod(4), mod_acc_mod(1), mod_reload_check(2)],
        Rarity.LEGENDARY: [mod_dmg_mod(5), mod_acc_mod(1), mod_reload_check(2)],
        Rarity.PEARLESCENT: [mod_dmg_mod(6), mod_acc_mod(2), mod_reload_check(3)],
    }

    def reload_modifiers(self):
        new_properties = self.high_quality[self.linked_equipment.rarity]
        self.replace_modifiers(new_properties)


class trait_heavy_mags(WeaponTrait):
    name = 'Heavy Mags'
    effect = '+1 Mag Size, -1 Movement.'

    def reload_modifiers(self):
        new_properties = [mod_mag_size(1), mod_extra_movement(-1)]
        self.replace_modifiers(new_properties)


class trait_lock_on(WeaponTrait):
    name = 'Lock On'
    effect = 'In place of a Ranged Attack, fire a Homing Dart at a target. For the next 2 Turns, Attacks with this weapon against that target will treat an Accuracy Roll of 7 or lower (after Mods) as a Solid Attack.'

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, self.effect)
        new_modifier.situational = True
        self.replace_modifiers([new_modifier])


class trait_non_elemental(WeaponTrait):
    name = 'Non Elemental'
    effect = f"This Equipment can't be Elemental."

    def reload_modifiers(self):
        self.replace_modifiers([mod_non_elemental()])


# Bandit - Primary
class trait_big_mags(WeaponTrait):
    name = 'Big Mags'
    effect = '+3 Mag Size, +2 Fumble Range.'

    def reload_modifiers(self):
        self.replace_modifiers([
            mod_mag_size(3),
            mod_fumble_range(2)
        ])


class trait_pointy(WeaponTrait):
    name = 'Pointy'
    effect = "Always has the Bayonet Accessory. This part doesn't count towards the maximum number of Gun Parts."

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, self.effect)
        new_modifier.hidden = True
        self.replace_modifiers([
            new_modifier
        ])


class trait_overheat(WeaponTrait):
    name = 'Overheat'
    effect = "When Reloading: You and Adjacent Targets take Elemental Damage (Same Element as the Gun, Incendiary if Non Elemental)."

    def reload_modifiers(self):
        self.replace_modifiers([
            mod_overheat()
        ])


# Dahl - Primary
class trait_steady_aim(WeaponTrait):
    name = 'Steady Aim'
    effect = "While ADS: Burst +1."

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, self.effect)
        new_modifier.situational = True
        self.replace_modifiers([
            new_modifier
        ])


class trait_tacticool(WeaponTrait):
    name = 'Tacti-cool'
    effect = "Gains extra Gun Parts."

    tacticool = {
        Rarity.COMMON: [mod_tacticool_firemodes(1), mod_fixed_scopes(1)],
        Rarity.UNCOMMON: [mod_tacticool_firemodes(1), mod_fixed_scopes(1), mod_extra_accessories(1)],
        Rarity.RARE: [mod_tacticool_firemodes(2), mod_fixed_scopes(1), mod_extra_accessories(1)],
        Rarity.EPIC: [mod_tacticool_firemodes(2), mod_fixed_scopes(2), mod_extra_accessories(1)],
        Rarity.LEGENDARY: [mod_tacticool_firemodes(2), mod_fixed_scopes(2), mod_extra_accessories(2)],
        Rarity.PEARLESCENT: [mod_tacticool_firemodes(2), mod_fixed_scopes(2), mod_extra_accessories(3)],
    }

    def reload_modifiers(self):
        equipment = self.linked_equipment
        self.replace_modifiers(self.tacticool[equipment.rarity])


class trait_reconfigure(WeaponTrait):
    name = 'Reconfigure'
    effect = "Swap between Fire Modes and/or Scopes. SPD 10 Check."

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, self.effect)
        new_modifier.situational = True
        self.replace_modifiers([
            new_modifier
        ])


# Dahl - Fire Modes
class trait_fm_single_fire(WeaponTrait):
    name = '(Fire Mode) Single Fire'
    effect = "+1 Range, +1 ACC MOD."

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, self.effect)
        new_modifier.hidden = True
        self.replace_modifiers([
            new_modifier
        ])


class trait_fm_burst_fire(WeaponTrait):
    name = '(Fire Mode) Burst Fire'
    effect = "+1 Burst, -3 ACC MOD, Consumes 2 Ammo."

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, self.effect)
        new_modifier.hidden = True
        self.replace_modifiers([
            new_modifier
        ])


class trait_fm_full_auto(WeaponTrait):
    name = '(Fire Mode) Full Auto'
    effect = "+2 Burst, -8 ACC MOD, Consumes 3 Ammo."

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, self.effect)
        new_modifier.hidden = True
        self.replace_modifiers([
            new_modifier
        ])


# Hyperion - Primary
class trait_recoil_control(WeaponTrait):
    name = 'Recoil Control'
    effect = 'Increased Accuracy at the cost of Damage.'

    recoil_control = {
        Rarity.COMMON: [mod_acc_mod(1), mod_dmg_mod(-2)],
        Rarity.UNCOMMON: [mod_acc_mod(2), mod_dmg_mod(-2)],
        Rarity.RARE: [mod_acc_mod(3), mod_dmg_mod(-2)],
        Rarity.EPIC: [mod_acc_mod(4), mod_dmg_mod(-2)],
        Rarity.LEGENDARY: [mod_acc_mod(5), mod_dmg_mod(-2)],
        Rarity.PEARLESCENT: [mod_acc_mod(6), mod_dmg_mod(-2)],
    }

    def reload_modifiers(self):
        new_modifiers = self.recoil_control[self.linked_equipment.rarity]
        self.replace_modifiers(new_modifiers)


class trait_gun_shield(WeaponTrait):
    name = 'Gun Shield'
    effect = 'While ADS: Gun provides an Extra Energy Shield. Capacity is half of a Balanced Shield. Recharges after every Encounter.'

    def reload_modifiers(self):
        self.replace_modifiers([mod_gun_shield()])


# Hyperion - Gun Shield Parts
class trait_shield_amp(WeaponTrait):
    name = '(Amped) Gun Shield'
    effect = 'While Gun Shield is Full: Next Ranged Attack +1 Hit. Gun Shield takes 10 DMG.'

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, self.effect)
        new_modifier.situational = True
        self.replace_modifiers([new_modifier])


class trait_shield_genesis(WeaponTrait):
    name = '(Genesis) Gun Shield'
    effect = 'When Gun Shield takes Ranged DMG: Roll a d100. On 90+, take no DMG and gain 1 Ammo.'

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, self.effect)
        new_modifier.situational = True
        self.replace_modifiers([new_modifier])

class trait_shield_redirect(WeaponTrait):
    name = '(Redirect) Gun Shield'
    effect = 'When Gun Shield takes Ranged DMG: Roll a d100. On 90+, DMG instead is Reflected back to the Attacker.'

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, self.effect)
        new_modifier.situational = True
        self.replace_modifiers([new_modifier])

# Jakobs - Primary
class trait_head_hunter(WeaponTrait):
    name = 'Head Hunter'
    effect = "Increased Crit DMG and ACC MOD."

    head_hunter = {
        Rarity.COMMON: [mod_acc_mod(2), mod_crit_damage(2)],
        Rarity.UNCOMMON: [mod_acc_mod(2), mod_crit_damage(4)],
        Rarity.RARE: [mod_acc_mod(2), mod_crit_damage(6)],
        Rarity.EPIC: [mod_acc_mod(2), mod_crit_damage(8)],
        Rarity.LEGENDARY: [mod_acc_mod(2), mod_crit_damage(10)],
        Rarity.PEARLESCENT: [mod_acc_mod(2), mod_crit_damage(12)],
    }

    def reload_modifiers(self):
        new_modifiers = self.head_hunter[self.linked_equipment.rarity]
        self.replace_modifiers(new_modifiers)

    @property
    def effect(self):
        mods = self.head_hunter[self.linked_equipment.rarity]
        return f"{mods[1].effect} and {mods[0].effect}"

# For Non-Elemental trait See trait_non_elemental

class trait_cumbersome(WeaponTrait):
    name = 'Cumbersome'
    effect = '-1 Mag Size'

    def reload_modifiers(self):
        self.replace_modifiers([mod_mag_size(-1)])


# Jakobs - Secondary
class trait_fan_the_hammer(WeaponTrait):
    name = 'Fan the Hammer'
    effect = "You can use your SPD MOD instead of ACC MOD for Accuracy rolls. If you do, gain an Extra Attack that has -3 Accuracy."

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, self.effect)
        new_modifier.situational = True
        self.replace_modifiers([new_modifier])


class trait_ricochet(WeaponTrait):
    name = 'Ricochet'
    effect = "Crits also deal DMG to one Adjacent Enemy."

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, self.effect)
        new_modifier.situational = True
        self.replace_modifiers([new_modifier])


class trait_percise(WeaponTrait):
    name = 'Percise'
    effect = "On Penetrating and Lethal Attacks: +1 Crit."

    def reload_modifiers(self):
        self.replace_modifiers([
            mod_penetrate_crits(1),
            mod_lethal_crits(1)
        ])


# Maliwan - Primary
class trait_elemental(WeaponTrait):
    name = 'Elemental'
    effect = 'Always Elemental (Non-Explosive).'

    def reload_modifiers(self):
        self.replace_modifiers([mod_is_elemental(), mod_non_explosive()])


class trait_proliferation(WeaponTrait):
    name = 'Proliferation'
    effect = 'Improved Elemental Scaling. Increase Gun generation Elemental rolls and when applying Elemental Status Effects.'
    situational = True

    proliferation = {
        Rarity.COMMON: [mod_elements_min(1), mod_elemental_roll_bonus(0)],
        Rarity.UNCOMMON: [mod_elements_min(1), mod_elemental_roll_bonus(10)],
        Rarity.RARE: [mod_elements_min(2), mod_elemental_roll_bonus(10)],
        Rarity.EPIC: [mod_elements_min(2), mod_elemental_roll_bonus(20)],
        Rarity.LEGENDARY: [mod_elements_min(2), mod_elemental_roll_bonus(30)],
        Rarity.PEARLESCENT: [mod_elements_min(2), mod_elemental_roll_bonus(40)]
    }

    def reload_modifiers(self):
        new_modifiers = self.proliferation[self.linked_equipment.rarity]
        self.replace_modifiers(new_modifiers)


class trait_mode_switch(WeaponTrait):
    name = 'Mode Switch'
    effect = 'Rare and higher Rarity can swap between 2 elements. SPD 10 Check.'
    situational = True

    def reload_modifiers(self):
        new_modifiers = []
        # Only applicable for equipment of Rare and higher rarity
        if not self.linked_equipment.rarity in [Rarity.COMMON, Rarity.UNCOMMON]:
            new_modifier = mod_template(self.name, '')
            new_modifier.effect = 'Swap between 2 Elements, SPD 10 Check.'
            new_modifier.situational = True

            new_modifiers = [new_modifier]

        self.replace_modifiers(new_modifiers)


# Torgue - Primary
class trait_boom(WeaponTrait):
    name = 'Boom!'
    effect = 'Always Explosive, only Explosive, at the cost of Accuracy.'

    boom = {
        Rarity.COMMON: [mod_splash(), mod_knock_back(5), mod_acc_mod(-4)],
        Rarity.UNCOMMON: [mod_splash(), mod_knock_back(10), mod_acc_mod(-3)],
        Rarity.RARE: [mod_splash(), mod_knock_back(15), mod_acc_mod(-2)],
        Rarity.EPIC: [mod_splash(), mod_knock_back(20), mod_acc_mod(-1)],
        Rarity.LEGENDARY: [mod_splash(), mod_knock_back(25)],
        Rarity.PEARLESCENT: [mod_splash(), mod_knock_back(30)],
    }

    def reload_modifiers(self):
        new_modifiers = [Explosive()]
        new_modifiers += self.boom[self.linked_equipment.rarity]
        self.replace_modifiers(new_modifiers)


class trait_splasher(WeaponTrait):
    name = 'Splasher!'
    effect = 'Deals Full Splash Damage.'
    situational = True

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, self.effect)
        new_modifier.situational = True
        self.replace_modifiers([new_modifier])


class trait_explosions(WeaponTrait):
    name = 'Explosions!?'
    effect = 'Splash Range +1.'

    def reload_modifiers(self):
        self.replace_modifiers([mod_splash_range(1)])


class trait_concussive(WeaponTrait):
    name = 'Concussive!'
    effect = '+25% Knock Back.'

    def reload_modifiers(self):
        self.replace_modifiers([mod_knock_back(25)])


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

class trait_charge(WeaponTrait):
    name = 'Charge'
    effect = 'When you Target an Ally, they regain Shields.'

    def reload_modifiers(self):
        self.replace_modifiers([mod_charge()])


class trait_drain(WeaponTrait):
    name = 'Drain'
    effect = 'When you Damage an Enemy, you regain Shields.'

    def reload_modifiers(self):
        self.replace_modifiers([mod_drain()])


# Tediore - Primary
class trait_fire_and_forget(WeaponTrait):
    name = 'Fire & Forget'
    effect = 'When you Reload this Gun, you Throw it away instead and deal Damage.'

    fire_and_forget = {
        Rarity.COMMON: Dice(1,4),
        Rarity.UNCOMMON: Dice(1,6),
        Rarity.RARE: Dice(1,8),
        Rarity.EPIC: Dice(1,10),
        Rarity.LEGENDARY: Dice(1,12),
        Rarity.PEARLESCENT: Dice(2,8)
    }

    def reload_modifiers(self):
        bonus_dice = self.fire_and_forget[self.linked_equipment.rarity]
        new_modifier = mod_template(self.name, '')
        new_modifier.effect = f"When you Reload this Gun: You Throw it away instead, dealing {bonus_dice} DMG."
        new_modifier.situational = True
        self.replace_modifiers([new_modifier])


class trait_compact(WeaponTrait):
    name = 'Compact'
    effect = '-2 Mag Size (minimum of 1), +4 on Reload and Swap Checks.'

    def reload_modifiers(self):
        self.replace_modifiers([
            mod_mag_size(-2),
            mod_reload_check(4),
            mod_swap_check(4)
        ])


# Tediore - Secondary
class trait_turret(WeaponTrait):
    name = 'Turret'
    effect = 'When Thrown: the Gun turns into a Turret for 2 turns. Once per turn the Turret shoots the closest Enemy.'

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, self.effect)
        new_modifier.situational = True
        self.replace_modifiers([new_modifier])


class trait_bomb(WeaponTrait):
    name = 'Bomb'
    effect = 'When Thrown: the Gun turns into a Grenade dealing Splash Damage in the same Element as the Gun (Explosive if Non Elemental).'

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, self.effect)
        new_modifier.situational = True
        self.replace_modifiers([new_modifier])


# Vladof - Primary
class trait_wall_of_lead(WeaponTrait):
    name = 'Wall of Lead'
    effect = 'Extra Attacks at the cost of Accuracy.'

    fire_and_forget = {
        Rarity.COMMON: [mod_extra_attack(1), mod_acc_mod(-4)],
        Rarity.UNCOMMON: [mod_extra_attack(1), mod_acc_mod(-3)],
        Rarity.RARE: [mod_extra_attack(1), mod_acc_mod(-2)],
        Rarity.EPIC: [mod_extra_attack(1), mod_acc_mod(-1)],
        Rarity.LEGENDARY: [mod_extra_attack(1)],
        Rarity.PEARLESCENT: [mod_extra_attack(1), mod_extra_movement(1)],
    }

    def reload_modifiers(self):
        new_modifiers = self.fire_and_forget[self.linked_equipment.rarity]
        self.replace_modifiers(new_modifiers)


class trait_extended_mags(WeaponTrait):
    name = 'Extended Mags'
    effect = '+2 Mag Size.'

    def reload_modifiers(self):
        self.replace_modifiers([mod_mag_size(2)])


class trait_endless_fire(WeaponTrait):
    name = 'Endless Fire'
    effect = "On an Accuracy Roll of 5, 10, 15 or 20 (before Mods): this Attack doesn't consume Ammo."

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, self.effect)
        new_modifier.situational = True
        self.replace_modifiers([new_modifier])


# Vladof - Secondary
class trait_grenade_launcher(WeaponTrait):
    name = 'Grenade Launcher'
    effect = '(1/Encounter) Shoot a 1d8/Tier Explosive Grenade at a point within 5 squares.'

    def reload_modifiers(self):
        self.replace_modifiers([mod_grenade_launcher()])


class trait_taser(WeaponTrait):
    name = 'Taser'
    effect = '(1/Encounter) When used: Each Enemy within a 3 square Cone takes 1d4/Tier Shock Damage and is Dazed.'

    def reload_modifiers(self):
        self.replace_modifiers([mod_taser()])


class trait_bipod(WeaponTrait):
    name = 'Bipod'
    effect = 'While Active: +2 ACC MOD on Ranged Attacks, -1 Movement. You can (de)activate the Bipod once on your turn.'

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, self.effect)
        new_modifier.situational = True
        self.replace_modifiers([new_modifier])


# Eridian - Primary
class trait_reverse_engineer(WeaponTrait):
    name = 'Reverse Engineer'
    effect = 'This Alien Gun is made using a Gun from another Manufacturer as a base.'

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, self.effect)
        new_modifier.hidden = True
        self.replace_modifiers([new_modifier])


class trait_alien_ammo(WeaponTrait):
    name = 'Alien Ammo'
    effect = 'Consumes 2 Ammo per Attack, +2 Mag Size.'

    def reload_modifiers(self):
        self.replace_modifiers([
            mod_ammo_cost(2),
            mod_mag_size(2)
        ])


# Eridian - Gun Type Traits
class trait_dart(WeaponTrait):
    name = 'Dart'
    effect = '+2 Range, Ignores Cover.'

    def reload_modifiers(self):
        new_modifier = mod_template(self.name, '')
        new_modifier.effect = 'Ignores Cover'
        new_modifier.situational = True
        self.replace_modifiers([mod_range(2), new_modifier])


class trait_plasma_caster(WeaponTrait):
    name = 'Plasma Caster'
    effect = '+1 Range, +2 Burst.'

    def reload_modifiers(self):
        self.replace_modifiers([mod_range(1), mod_burst(2)])


class trait_splat(WeaponTrait):
    name = 'Splat'
    effect = '-1 Range, Splash, +1 Burst.'

    def reload_modifiers(self):
        self.replace_modifiers([
            mod_range(-1),
            mod_splash(),
            mod_burst(1)
        ])


class trait_blaster(WeaponTrait):
    name = 'Blaster'
    effect = '+1 Range, +2 Burst, +3 Mag Size.'

    def reload_modifiers(self):
        self.replace_modifiers([
            mod_range(1),
            mod_burst(2),
            mod_mag_size(3)
        ])


class trait_railer(WeaponTrait):
    name = 'Railer'
    effect = '+2 Range, +1 Burst, Pierces 1 Enemy or Object.'


    def reload_modifiers(self):
        new_modifier = mod_template(self.name, '')
        new_modifier.effect = 'Pierces 1 Enemy or Object.'
        self.replace_modifiers([
            mod_range(2),
            mod_burst(1),
            new_modifier
        ])


class trait_plasma_cannon(WeaponTrait):
    name = 'Plasma Cannon'
    effect = '+1 Range, +1 Burst, +1 Splash Radius.'

    def reload_modifiers(self):
        self.replace_modifiers([
            mod_range(1),
            mod_burst(1),
            mod_splash_range(1)
        ])
