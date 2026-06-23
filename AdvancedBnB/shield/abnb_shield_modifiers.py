from util.modifier import AdditiveModifier

class ShieldPartModifier(AdditiveModifier):
    name = '<Shield Part Name>'

    def __init__(self, mod_value=1):
        super().__init__(mod_value)


# --- Stat Modifiers ---
class mod_capacity(AdditiveModifier):
    name = 'Capacity'
    hidden = True


class mod_shield_regen(AdditiveModifier):
    name = 'Shield Regen'
    hidden = True


class mod_max_health(AdditiveModifier):
    name = 'Max Health'


class mod_health_regen(AdditiveModifier):
    name = 'Health Regen'


# --- Shield Part Modifiers ---
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
        return f"While Depleted: Reload Check +{2*self.value}."


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


class mod_fleet(ShieldPartModifier):
    name = 'Fleet'
    effect = 'While Depleted: gain +2/P Movement.'
    situational = True

    @property
    def effect(self):
        return f"While Depleted: Movement +{2*self.value}."


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


class mod_nova(ShieldPartModifier):
    name = 'Nova'
    effect = 'On Depletion: deal 2d6/P Elemental Damage to adjacent Enemies. Shield needs to have been fully Recharged for it to trigger again.'
    situational = True

    @property
    def effect(self):
        return f"On Depletion: deal {2 * self.value}d6 Elemental Damage to adjacent Enemies. Shield needs to have been fully Recharged for it to trigger again."


class mod_projected(ShieldPartModifier):
    name = 'Projected'
    effect = 'While ADS: gain 1d6/P Damage Reduction.'
    situational = True

    @property
    def effect(self):
        return f"While ADS: +{self.value}d6/P Damage Reduction."


class mod_reflect(ShieldPartModifier):
    name = 'Reflect'
    effect = 'When taking Ranged Damage: Roll a d100. 10%/P chance to Reflect Damage back to the Attacker. You take no Damage.'
    situational = True

    @property
    def effect(self):
        return f"When taking Ranged Damage: Roll a d100. On a {100 - (self.value * 10)}+: Reflect Damage back to the Attacker instead."


class mod_resistance(ShieldPartModifier):
    name = 'Resistant'
    effect = 'Gain an Extra 1d8/P Elemental Damage Reduction, up to a maximum of 3d8 per Element.'
    type = 'Unknown'
    situational = True

    @property
    def name(self):
        return f"Resistant ({self.type})"

    @property
    def effect(self):
        return f"+{min(self.value, 3)}d8 {self.type} Elemental Damage Reduction."


class mod_roid(ShieldPartModifier):
    name = 'Roid'
    effect = 'While Depleted: add +1/P Melee Die to you Melee Attacks.'
    situational = True

    @property
    def effect(self):
        return f"While Depleted: add +{self.value} Melee Die to you Melee Attacks."


class mod_spike(ShieldPartModifier):
    name = 'Spike'
    effect = 'On taking Melee Damage: deal 1d10/P Elemental Damage to the Attacker.'
    situational = True

    @property
    def effect(self):
        return f"On taking Melee Damage: deal {self.value}d10 Elemental Damage to the Attacker."


class mod_vagabond(ShieldPartModifier):
    name = 'Vagabond'
    effect = 'While Full: Gain +2/P Movement.'
    situational = True

    @property
    def effect(self):
        return f"While Full: Movement +{2 * self.value}."


class mod_symbiotic(ShieldPartModifier):
    name = 'Symbiotic'
    effect = 'While this shield is equipped it merges with you.'
    situational = True

    @property
    def effect(self):
        equipment = self.get_linked_equipment()
        return f"Health Tag: {equipment.tag.name} ({equipment.tag.effect}). Effects that would activate when Shield Depletes, now activate when Health falls below Half."




