from util import Modifier, Dice, Rarity

class mod_dmg_mod(Modifier):
    name = 'DMG MOD'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"DMG MOD {'+' if self.value > 0 else ''}{self.value}"


class mod_acc_mod(Modifier):
    name = 'ACC MOD'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"ACC MOD {'+' if self.value > 0 else ''}{self.value}"


class mod_range(Modifier):
    name = 'Range'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Range {'+' if self.value > 0 else ''}{self.value}"


class mod_hit_damage(Modifier):
    name = 'Hit Damage'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Hit Damage {'+' if self.value > 0 else ''}{self.value}"


class mod_crit_damage(Modifier):
    name = 'Crit Damage'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Crit Damage {'+' if self.value > 0 else ''}{self.value}"


class mod_burst(Modifier):
    name = 'Burst MOD'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Burst {'+' if self.value > 0 else ''}{self.value}"


class mod_ammo_cost(Modifier):
    name = 'Ammo per Attack'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Ammo per Attack {'+' if self.value > 0 else ''}{self.value}"


class mod_lethal_range(Modifier):
    name = 'Lethal range'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Lethal range {'+' if self.value > 0 else ''}{self.value}"


class mod_mag_size(Modifier):
    name = 'Magazine Size MOD'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Mag size {'+' if self.value > 0 else ''}{self.value}"


class mod_ads_range_min(Modifier):
    name = 'Minimum ADS Range'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Min ADS range {'+' if self.value > 0 else ''}{self.value}"


class mod_fumble_range(Modifier):
    name = 'Fumble Range'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Fumble range {'+' if self.value > 0 else ''}{self.value}"


class prop_movement_mod(Modifier):
    name = 'Movement MOD'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Movement {'+' if self.value > 0 else ''}{self.value}"


class mod_reload_check(Modifier):
    name = 'Reload Check'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Reload Check {'+' if self.value > 0 else ''}{self.value}"


class mod_swap_check(Modifier):
    name = 'Swap Check'
    additive = True

    def __init__(self, mod_value):
        self.value = mod_value
        self.effect = f"Swap Check {'+' if self.value > 0 else ''}{self.value}"


class prop_non_elemental(Modifier):
    name = 'Non Elemental'

    def __init__(self):
        self.effect = "Non Elemental"


class mod_splash(Modifier):
    name = 'Splash'

    def __init__(self):
        self.effect = "Splash"


# Anshin - Secondary Gun Properties
class prop_medic(Modifier):
    name = 'Medic'
    situational = True

    def __init__(self, healing):
        self.effect = f"When you Target an Ally, they regain Health ({healing}/Hit, {healing * 2}/Crit)."

class prop_vampire(Modifier):
    name = 'Vampire'
    situational = True

    def __init__(self, healing):
        self.effect = f"When you Damage an Enemy, you regain Health ({healing}/Hit, {healing * 2}/Crit)."


# Bandit
class mod_overheat(Modifier):
    name = 'Overheat'
    situational = True

    overheat = {
        Rarity.COMMON: '1d4',
        Rarity.UNCOMMON: '1d6',
        Rarity.RARE: '1d8',
        Rarity.EPIC: '1d10',
        Rarity.LEGENDARY: '1d12',
        Rarity.PEARLESCENT: '2d8'
    }

    def __init__(self, tier, rarity):
        dice_multi = 1
        if tier >= 4:
            dice_multi = 2
        if tier >= 7:
            dice_multi = 3
        if tier >= 10:
            dice_multi = 4

        dmg_die = Dice.from_string(self.overheat[rarity])
        dmg_die.count *= dice_multi

        self.effect = f"When Reloading: You and Adjacent Targets take {dmg_die} Elemental Damage (Same Element as the Gun, Incendiary if Non Elemental)."
