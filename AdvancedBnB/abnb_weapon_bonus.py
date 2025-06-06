import math

from util import Modifier

class BonusPistol(Modifier):
    name = 'Pistol Bonus'
    effect = 'You gain +2 on Swap Checks when swapping to or from a Pistol.'

    def apply(self, gun):
        gun.mod_stats.setdefault('mods', {}).setdefault('swap_check', 0)
        gun.mod_stats['mods']['swap_check'] += 2

class BonusSmg(Modifier):
    name = 'Smg Bonus'
    effect = 'Smg has no Type Bonus.'

class BonusRifle(Modifier):
    name = 'Combat Rifle Bonus'
    effect = f"Combat Rifles always spawn with an Accessory Part. This Part doesn't count towards the maximum numer of Parts for this Gun."

class BonusSniper_scope(Modifier):
    name = 'Sniper Rifle Bonus'
    effect = f"Sniper Rifle always spawn with a Scope Part. This Part counts against the maximum number of Parts for this Gun."

class BonusSniper_accuracy(Modifier):
    name = 'Sniper Rifle Bonus'
    effect = f"When Attacking a Target over half the Sniper Rifles' Range (rounded up), gain an ACC Bonus equal to half it's Tier (rounded up)."
    situational = True

    def to_text(self, gun):
        range_prop = math.ceil(gun.range / 2)
        acc_bonus = math.ceil(gun.tier / 2)

        return f"When Attacking a Target over {range_prop} Range, +{acc_bonus} ACC MOD."

class BonusShotgun(Modifier):
    name = 'Shotgun Bonus'
    effect = f"When Attacking a Target within half the Shotguns' Range (rounded down), gain a DMG Bonus equal to it's Tier."
    situational = True

    def to_text(self, gun):
        range_prop = math.floor(gun.range / 2)

        return f"When Attacking a Target within {range_prop} Range: +{gun.tier} DMG MOD."

class BonusLauncher(Modifier):
    name = 'Rocket Launcher Bonus'
    effect = f"Splash."

    def apply(self, gun):
        gun.mod_stats.setdefault('mods', {}).setdefault('splash', 0)
        gun.mod_stats['mods']['splash'] = 1


