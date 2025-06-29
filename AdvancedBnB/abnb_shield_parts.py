from AdvancedBnB.abnb_shieldtypes import Shieldtypes
from util import Modifier

class shd_part_empty(Modifier):
    name = 'Trinket'
    effect = 'Looks cool. Does Nothing.'


class shd_part_absorb(Modifier):
    name = 'Absorb'
    effect = 'When taking Ranged Damage: Roll a d100. 10%/P chance to take no Damage and gain 1 Ammo.'
    situational = True

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        return f"When taking Ranged Damage: Roll a d100. On a {100 - (10*n_parts)}+: take no Damage and gain 1 Ammo."


class shd_part_adaptive(Modifier):
    name = 'Adaptive'
    effect = 'Gain +10/P Max Health. After taking Elemental Damage: gain 1d4/P Damage Reduction from that Element until you take Damage from a different Element.'
    situational = True

    def apply(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        item.mod_stats.setdefault('mods', {}).setdefault('max_health', 0)
        item.mod_stats['mods']['max_health'] += (n_parts * 10)

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        return f"After taking Elemental Damage: gain {n_parts}d4 Damage Reduction from that Element until you take Damage from a different Element."


class shd_part_adrenaline(Modifier):
    name = 'Adrenaline'
    effect = 'While Depleted: Gain +2/P on Reload Checks.'
    situational = True

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        return f"While Depleted: Gain +{n_parts * 2} on Reload Checks."


class shd_part_amp(Modifier):
    name = 'Amp'
    effect = 'While Full: Your next Ranged Attack deals an Extra 1/P Hit. You then lose 10/P Shield.'
    situational = True

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        return f"While Full: Your next Ranged Attack deals an Extra {n_parts} Hit{'s' if n_parts > 1 else ''}. You then lose {10 * n_parts} Shield."


class shd_part_brimming(Modifier):
    name = 'Brimming'
    effect = 'While Full: gain 5/P Health Regen.'
    situational = True

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        return f"While Full: gain +{n_parts * 5} Health Regen."


class shd_part_capacity(Modifier):
    name = 'Capacity'
    effect = 'Gain an extra (15/20/10)/P Shield Capacity (based on Shield Type)'

    def apply(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        cap_bonus = {
            Shieldtypes.BALANCED: 15,
            Shieldtypes.HIGHCAPACITY: 20,
            Shieldtypes.FAST: 10
        }
        item.mod_stats['capacity'] += (cap_bonus[item.shield_type] * n_parts)

    def to_text(self, item):
        return f"Increased Shield Capacity."


class shd_part_fleet(Modifier):
    name = 'Fleet'
    effect = 'While Depleted: gain +2/P Movement.'
    situational = True

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        return f"While Depleted: gain +{n_parts * 2} Movement."


class shd_part_health(Modifier):
    name = 'Health'
    effect = 'Gain +20/P Max Health.'

    def apply(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        item.mod_stats.setdefault('mods', {}).setdefault('max_health', 0)
        item.mod_stats['mods']['max_health'] += (n_parts * 20)

    def to_text(self, item):
        return f"Increased Max Health."


class shd_part_nova(Modifier):
    name = 'Nova'
    effect = 'On Depletion: deal 2d6/P Elemental Damage to adjacent Enemies. Shield needs to have been fully Recharged for it to trigger again.'
    situational = True

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        return f"On Depletion: deal {n_parts * 2}d6 Elemental Damage to adjacent Enemies. Shield needs to have been fully Recharged for it to trigger again."


class shd_part_projected(Modifier):
    name = 'Projected'
    effect = 'While ADS: gain 1d6/P Damage Reduction.'
    situational = True

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        return f"While ADS: gain {n_parts}d6 Damage Reduction."


class shd_part_recharge(Modifier):
    name = 'Recharge'
    effect = 'Gain an extra 10/P Shield Recharge.'

    def apply(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        item.mod_stats['charge_rate'] += (n_parts * 10)

    def to_text(self, item):
        return f"Increased Shield Recharge Rate."


class shd_part_reflect(Modifier):
    name = 'Reflect'
    effect = 'When taking Ranged Damage: Roll a d100. 10%/P chance to Reflect Damage back to the Attacker. You take no Damage.'
    situational = True

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        return f"When taking Ranged Damage: Roll a d100. On a {100 - (n_parts * 10)}+: Reflect Damage back to the Attacker. You take no Damage."


class shd_part_resistant(Modifier):
    name = 'Resistant'
    effect = 'Gain an Extra 1d8/P Elemental Damage Reduction.'
    type = 'Unknown'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        return f"Gain {n_parts}d8 {self.type} Elemental Damage Reduction."


class shd_part_roid(Modifier):
    name = 'Roid'
    effect = 'While Depleted: add +1/P Melee Die to you Melee Attacks.'
    situational = True

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        return f"While Depleted: add +{n_parts} Melee Die to you Melee Attacks."


class shd_part_charge_health(Modifier):
    name = 'Charge'
    effect = 'When Damaged: Roll a d100. On a 75+, drop 1/P Common Health Potions (1d8).'
    situational = True

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        return f"When Damaged: Roll a d100. On a 75+, drop {n_parts} Common Health Potions (1d8)."


class shd_part_charge_shield(Modifier):
    name = 'Charge'
    effect = 'When Damaged: Roll a d100. On a 75+, drop 1/P Common Shield Potions (1d8).'
    situational = True

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        return f"When Damaged: Roll a d100. On a 75+, drop {n_parts} Common Shield Potions (1d8)."


class shd_part_spike(Modifier):
    name = 'Spike'
    effect = 'On taking Melee Damage: deal 1d10/P Damage to the Attacker.'
    situational = True

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        return f"On taking Melee Damage: deal {n_parts}d10 Elemental Damage to the Attacker."


class shd_part_turtle(Modifier):
    name = 'Turtle'
    effect = 'Gain an Extra (30/40/20)/P Shield Capacity (based on Shield Type). -10/P Max Health.'

    def apply(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        cap_bonus = {
            Shieldtypes.BALANCED: 30,
            Shieldtypes.HIGHCAPACITY: 40,
            Shieldtypes.FAST: 20
        }
        item.mod_stats['capacity'] += (n_parts * cap_bonus[item.shield_type])

        item.mod_stats.setdefault('mods', {}).setdefault('max_health', 0)
        item.mod_stats['mods']['max_health'] -= (n_parts * 10)

    def to_text(self, item):
        return f"Increased Shield Capacity. Decreased Max Health."


class shd_part_vagabond(Modifier):
    name = 'Vagabond'
    effect = 'While Full: Gain +2/P Movement.'
    situational = True

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        return f"While Full: Gain +{n_parts * 2} Movement."


class shd_trait_reverse_engineer(Modifier):
    name = 'Reverse Engineer'
    effect = 'This Shield is made using a Shield from another Manufacturer as a base.'

class shd_trait_symbiotic(Modifier):
    name = 'Symbiotic'
    effect = 'While this shield is equipped it merges with you.'
    situational = True

    def apply(self, item):
        # Health is increased by Shield Capacity. Health Tags change to that of Shield.
        # Health Regen is increased by Shield Recharge Rate
        # Effect that activate when shield depletes, now activate when Health falls below Half.
        item.mod_stats.setdefault('mods', {}).setdefault('max_health', 0)
        item.mod_stats['mods']['max_health'] += item.capacity

        item.mod_stats.setdefault('mods', {}).setdefault('health_regen', 0)
        item.mod_stats['mods']['health_regen'] += item.recharge_rate

    def to_text(self, item):
        return f"Health Tag: {item.tag.name} ({item.tag.effect}). Effects that would activate when Shield Depletes, now activate when Health falls below Half."


class shd_tag_energy(Modifier):
    name = 'Energy'
    effect = 'Weak to Shock Damage.'


class shd_tag_alloy(Modifier):
    name = 'Alloy'
    effect = 'Weak to Corrosive Damage.'


class shd_tag_bio(Modifier):
    name = 'Bio'
    effect = 'Weak to Incendiary Damage.'


shield_parts_table = {
    (1, 5): shd_part_empty(),
    (6, 10): shd_part_absorb(),
    (11, 15): shd_part_adaptive(),
    (16, 20): shd_part_adrenaline(),
    (21, 25): shd_part_amp(),
    (26, 30): shd_part_brimming(),
    (31, 35): shd_part_capacity(),
    (36, 40): shd_part_fleet(),
    (41, 45): shd_part_health(),
    (46, 50): shd_part_nova(),
    (51, 55): shd_part_projected(),
    (56, 60): shd_part_recharge(),
    (61, 65): shd_part_reflect(),
    (66, 70): shd_part_resistant(),
    (71, 75): shd_part_roid(),
    (76, 80): shd_part_charge_health(),
    (81, 85): shd_part_charge_shield(),
    (86, 90): shd_part_spike(),
    (91, 95): shd_part_turtle(),
    (96, 100): shd_part_vagabond(),
}