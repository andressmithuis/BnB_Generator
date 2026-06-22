from util.modifier import AdditiveModifier
from .abnb_shieldtypes import Shieldtypes

class ShieldPartModifier(AdditiveModifier):
    name = '<Shield Part Name>'

    def __init__(self, mod_value=1):
        super().__init__(mod_value)


class mod_absorb(ShieldPartModifier):
    name = 'Absorb'
    effect = 'When taking Ranged Damage: Roll a d100. 10%/P chance to take no Damage and gain 1 Ammo.'
    situational = True

    @property
    def effect(self):
        return f"When taking Ranged Damage: Roll a d100. On a {100 - (10*self.value)}+: take no Damage and gain 1 Ammo."


class mod_adaptive(ShieldPartModifier):
    name = 'Adaptive'
    effect = 'After taking Elemental Damage: gain 1d4/P Damage Reduction from that Element until you take Damage from a different Element.'
    situational = True

    @property
    def effect(self):
        return f"After taking Elemental Damage: gain {self.value}d4 Damage Reduction from that Element until you take Damage from a different Element."


class mod_adrenaline(ShieldPartModifier):
    name = 'Adrenaline'
    effect = 'While Depleted: Gain +2/P on Reload Checks.'
    situational = True

    @property
    def effect(self):
        return f"While Depleted: Gain +{2*self.value} on Reload Checks."


class mod_amp(ShieldPartModifier):
    name = 'Amp'
    effect = 'While Full: Your next Ranged Attack deals an Extra 1/P Hit. You then lose 10/P Shield.'
    situational = True

    @property
    def effect(self):
        return f"While Full: Your next Ranged Attack deals +{self.value} Hit. You then lose {10*self.value} Shield."


class mod_brimming(ShieldPartModifier):
    name = 'Brimming'
    effect = 'While Full: gain 5/P Health Regen.'
    situational = True

    @property
    def effect(self):
        return f"While Full: Health Regen +{5 * self.value}."

class mod_capacity(AdditiveModifier):
    name = 'Capacity'

class mod_max_health(AdditiveModifier):
    name = 'Max Health'

class mod_fleet(ShieldPartModifier):
    name = 'Fleet'
    effect = 'While Depleted: gain +2/P Movement.'
    situational = True

    @property
    def effect(self):
        return f"While Depleted: gain +{2*self.value} Movement."


class mod_health_booster(ShieldPartModifier):
    name = 'Charge (Health)'
    effect = 'When Damaged: Roll a d100. On a 75+, drop 1/P Common Health Potions (1d8).'
    situational = True

    @property
    def effect(self):
        return f"When Damaged: Roll a d100. On a 75+, drop {self.value} Common Health Potion{'s' if self.value != 1 else ''} (1d8)."


class mod_shield_booster(ShieldPartModifier):
    name = 'Charge (Shield)'
    effect = 'When Damaged: Roll a d100. On a 75+, drop 1/P Common Shield Potions (1d8).'
    situational = True

    @property
    def effect(self):
        return f"When Damaged: Roll a d100. On a 75+, drop {self.value} Common Shield Potion{'s' if self.value != 1 else ''} (1d8)."




