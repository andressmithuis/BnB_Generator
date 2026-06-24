import math

from util import EquipmentProperty, mod_template
from .abnb_weapon_modifiers import *


class WeaponBonus(EquipmentProperty):
    pass


class BonusPistol(WeaponBonus):
    name = 'Pistol Bonus'
    effect = 'You gain +2 on Swap Checks when swapping to or from a Pistol.'

    def load_modifiers(self):
        new_mod = mod_template(self.name, self.effect)
        new_mod.situational = True
        self.attach_modifiers([new_mod])


class BonusSmg(WeaponBonus):
    name = 'Smg Bonus'
    effect = 'Smg has no Type Bonus.'

    def load_modifiers(self):
        new_mod = mod_template(self.name, self.effect)
        new_mod.hidden = True
        self.attach_modifiers([new_mod])


class BonusRifle(WeaponBonus):
    name = 'Combat Rifle Bonus'
    effect = f"Combat Rifles always spawn with an Accessory Part. This Part doesn't count towards the maximum numer of Parts for this Gun."

    def load_modifiers(self):
        self.attach_modifiers([
            mod_extra_accessories(1)
        ])

class BonusSniper_scope(WeaponBonus):
    name = 'Sniper Rifle Bonus'
    effect = f"Sniper Rifle always spawn with a Scope Part. This Part counts against the maximum number of Parts for this Gun."

    def load_modifiers(self):
        self.attach_modifiers([mod_fixed_scopes(1), mod_maximum_parts(-1)])


class BonusSniper_accuracy(WeaponBonus):
    name = 'Sniper Rifle Bonus'
    effect = f"When Attacking a Target over half the Sniper Rifles' Range (rounded up), gain an ACC Bonus equal to half it's Tier (rounded up)."

    def load_modifiers(self):
        self.attach_modifiers([wp_bonus_sniper()])


class BonusShotgun(WeaponBonus):
    name = 'Shotgun Bonus'
    effect = f"When Attacking a Target within half the Shotguns' Range (rounded down), gain a DMG Bonus equal to it's Tier."

    def load_modifiers(self):
        self.attach_modifiers([wp_bonus_shotgun()])


class BonusLauncher(WeaponBonus):
    name = 'Rocket Launcher Bonus'
    effect = f"Splash."

    def load_modifiers(self):
        self.attach_modifiers([mod_splash()])


# --- Gun Bonus specififc Modifiers ---
class wp_bonus_sniper(Modifier):
    name = 'Sniper Rifle Bonus'
    effect = "When Attacking a Target over half the Sniper Rifles' Range (rounded up), gain an ACC Bonus equal to half it's Tier (rounded up)."
    situational = True

    @property
    def effect(self):
        equipment = self.get_linked_equipment()
        range_value = math.ceil(equipment.range / 2)
        tier_value = math.ceil(equipment.tier / 2)
        return f"When Attacking a Target over {range_value} Range: ACC MOD +{tier_value}."


class wp_bonus_shotgun(Modifier):
    name = 'Shotgun Bonus'
    effect = f"When Attacking a Target within half the Shotguns' Range (rounded down), gain a DMG Bonus equal to it's Tier."
    situational = True

    @property
    def effect(self):
        equipment = self.get_linked_equipment()
        range_value = math.floor(equipment.range / 2)
        tier_value = equipment.tier
        return f"When Attacking a Target within {range_value} Range: DMG MOD +{tier_value} ."
