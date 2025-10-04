from util.modifier import Modifier
from util import Rarity
from util import Dice

class BonusShotgun(Modifier):
    name = 'Shotgun Bonus'
    effect = 'If Range 2 or Less: +2 DMG MOD.'
    situational = True


class BonusSniper(Modifier):
    name = 'Sniper Bonus'
    effect = 'If Range 3+: +3 ACC MOD.'
    situational = True

class BonusCrappy(Modifier):
    name = 'Starting Gun Bonus'
    effect = '-2 DMG MOD.'

    def apply(self, gun):
        gun.name_prefix = 'Crappy'
        gun.mod_stats.setdefault('mods', {}).setdefault('dmg_mod', 0)
        gun.mod_stats['mods']['dmg_mod'] -= 2


class trait_overheat(Modifier):
    name = 'Overheat'
    effect = 'When Reloading: Take Incendiary Damage.'

    bonus_table = {
        Rarity.COMMON: Dice.from_string('1d4'),
        Rarity.UNCOMMON: Dice.from_string('1d6'),
        Rarity.RARE: Dice.from_string('1d8'),
        Rarity.EPIC: Dice.from_string('1d10'),
        Rarity.LEGENDARY: Dice.from_string('1d12'),
    }

    def to_text(self, gun):
        bonus = self.bonus_table[gun.rarity]

        str = f"When Reloading: Take {bonus} Incendiary Damage."
        return str


class trait_swap_reload(Modifier):
    name = 'Swap/Reload'
    effect = 'On Swap/Reload: Gun is Thrown like a Grenade, dealing Damage.'

    bonus_table = {
        Rarity.COMMON: Dice.from_string('1d4'),
        Rarity.UNCOMMON: Dice.from_string('1d6'),
        Rarity.RARE: Dice.from_string('1d8'),
        Rarity.EPIC: Dice.from_string('1d10'),
        Rarity.LEGENDARY: Dice.from_string('1d12'),
    }

    def to_text(self, gun):
        dmg_dice = self.bonus_table[gun.rarity]

        str = f"On Swap/Reload: The Gun is Thrown like a Grenade and deals {dmg_dice} Damage."
        return str

class trait_extra_movement(Modifier):
    name = 'Extra Movement'
    effect = 'Gain an Extra Movement Action.'

class trait_extra_attack(Modifier):
    name = 'Extra Attack'
    effect = 'Gain an Extra Attack Action.'

class trait_splash(Modifier):
    name = 'Splash'
    effect = 'Deals Half Damage to Adjacent Targets.'