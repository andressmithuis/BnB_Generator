import math

from util import EquipmentProperty, Modifier, mod_template
from .abnb_weapon_modifiers import mod_splash


class WeaponBonus(EquipmentProperty):
    pass


class BonusPistol(WeaponBonus):
    name = 'Pistol Bonus'
    effect = 'You gain +2 on Swap Checks when swapping to or from a Pistol.'

    def reload_modifiers(self):
        new_mod = mod_template(self.name, self.effect)
        new_mod.situational = True
        self.replace_modifiers([new_mod])


class BonusSmg(WeaponBonus):
    name = 'Smg Bonus'
    effect = 'Smg has no Type Bonus.'

    def reload_modifiers(self):
        new_mod = mod_template(self.name, self.effect)
        new_mod.hidden = True
        self.replace_modifiers([new_mod])


class BonusRifle(WeaponBonus):
    name = 'Combat Rifle Bonus'
    effect = f"Combat Rifles always spawn with an Accessory Part. This Part doesn't count towards the maximum numer of Parts for this Gun."

    def reload_modifiers(self):
        self.replace_modifiers([
            wp_bonus_rifle()
        ])


class BonusSniper_scope(WeaponBonus):
    name = 'Sniper Rifle Bonus'
    effect = f"Sniper Rifle always spawn with a Scope Part. This Part counts against the maximum number of Parts for this Gun."

    def reload_modifiers(self):
        self.replace_modifiers([wp_bonus_sniper_scope()])


class BonusSniper_accuracy(WeaponBonus):
    name = 'Sniper Rifle Bonus'
    effect = f"When Attacking a Target over half the Sniper Rifles' Range (rounded up), gain an ACC Bonus equal to half it's Tier (rounded up)."

    def reload_modifiers(self):
        self.replace_modifiers([wp_bonus_sniper(self.linked_equipment.range, self.linked_equipment.tier)])


class BonusShotgun(WeaponBonus):
    name = 'Shotgun Bonus'
    effect = f"When Attacking a Target within half the Shotguns' Range (rounded down), gain a DMG Bonus equal to it's Tier."

    def reload_modifiers(self):
        self.replace_modifiers([wp_bonus_shotgun(self.linked_equipment.range, self.linked_equipment.tier)])


class BonusLauncher(WeaponBonus):
    name = 'Rocket Launcher Bonus'
    effect = f"Splash."

    def reload_modifiers(self):
        self.replace_modifiers([mod_splash()])


# --- Gun Bonus specififc Modifiers ---
class wp_bonus_rifle(Modifier):
    name = 'Combat Rifle Bonus'
    effect = f"Combat Rifles always spawn with an Accessory Part. This Part doesn't count towards the maximum numer of Parts for this Gun."
    hidden = True

    def __init__(self):
        self.accessory_part = None

    def apply_to_equipment(self, equipment):
        accessory_part = equipment.pick_weapon_accessory()
        equipment.add_property(accessory_part)
        self.accessory_part = accessory_part

    def revert_from_equipment(self, equipment):
        if self.accessory_part is not None:
            equipment.remove_property(self.accessory_part)
            self.accessory_part = None


class wp_bonus_sniper(Modifier):
    name = 'Sniper Rifle Bonus'
    effect = "When Attacking a Target over half the Sniper Rifles' Range (rounded up), gain an ACC Bonus equal to half it's Tier (rounded up)."
    situational = True

    def __init__(self, range, tier):
        range_prop = math.ceil(range/ 2)
        acc_bonus = math.ceil(tier / 2)
        self.effect = f"When Attacking a Target over {range_prop} Range, +{acc_bonus} ACC MOD."


class wp_bonus_sniper_scope(Modifier):
    name = 'Sniper Rifle Bonus'
    effect = f"Sniper Rifle always spawn with a Scope Part. This Part counts against the maximum number of Parts for this Gun."
    hidden = True

    def __init__(self):
        self.scope_part = None

    def apply_to_equipment(self, equipment):
        if equipment.n_scopes < equipment.max_scopes:
            scope_part = equipment.pick_weapon_scope()
            equipment.add_property(scope_part)
            equipment.n_scopes += 1
            equipment.n_parts += 1
            self.scope_part = scope_part

    def revert_from_equipment(self, equipment):
        if self.scope_part is not None:
            equipment.remove_property(self.scope_part)
            equipment.n_scopes -= 1
            equipment.n_parts -= 1
            self.scope_part = None


class wp_bonus_shotgun(Modifier):
    name = 'Shotgun Bonus'
    effect = f"When Attacking a Target within half the Shotguns' Range (rounded down), gain a DMG Bonus equal to it's Tier."
    situational = True

    def __init__(self, range, tier):
        range_prop = math.floor(range / 2)
        self.effect = f"When Attacking a Target within {range_prop} Range: +{tier} DMG MOD."
