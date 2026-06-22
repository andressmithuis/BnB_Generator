from AdvancedBnB.shield.abnb_shieldtypes import Shieldtypes
from util import EquipmentProperty, mod_template
from .abnb_shield_modifiers import *


# Wrapper class
class ShieldPart(EquipmentProperty):
    def reload_modifiers(self):
        new_modifier = mod_template(self.name, self.effect)
        new_modifier.hidden = True
        self.replace_modifiers([new_modifier])


# --- Shield Parts ---
class shd_part_empty(ShieldPart):
    name = 'Trinket'
    effect = 'Looks cool. Does Nothing.'


class shd_part_absorb(ShieldPart):
    name = 'Absorb'
    effect = 'When taking Ranged Damage: Roll a d100. 10%/P chance to take no Damage and gain 1 Ammo.'

    def reload_modifiers(self):
        self.replace_modifiers([
            mod_absorb()
        ])


class shd_part_adaptive(ShieldPart):
    name = 'Adaptive'
    effect = 'Gain +10/P Max Health. After taking Elemental Damage: gain 1d4/P Damage Reduction from that Element until you take Damage from a different Element.'

    def reload_modifiers(self):
        self.replace_modifiers([
            mod_max_health(10),
            mod_adaptive()
        ])


class shd_part_adrenaline(ShieldPart):
    name = 'Adrenaline'
    effect = 'While Depleted: Gain +2/P on Reload Checks.'

    def reload_modifiers(self):
        self.replace_modifiers([
            mod_adrenaline()
        ])


class shd_part_amp(ShieldPart):
    name = 'Amp'
    effect = 'While Full: Your next Ranged Attack deals an Extra 1/P Hit. You then lose 10/P Shield.'
    situational = True

    def reload_modifiers(self):
        self.replace_modifiers([
            mod_amp()
        ])


class shd_part_brimming(ShieldPart):
    name = 'Brimming'
    effect = 'While Full: gain 5/P Health Regen.'

    def reload_modifiers(self):
        self.replace_modifiers([
            mod_brimming()
        ])


class shd_part_capacity(ShieldPart):
    name = 'Capacity'
    effect = 'Gain an extra (15/20/10)/P Shield Capacity (based on Shield Type)'

    def reload_modifiers(self):
        equipment = self.linked_equipment
        shieldtype_bonus = {
            Shieldtypes.BALANCED: 15,
            Shieldtypes.HIGHCAPACITY: 20,
            Shieldtypes.FAST: 10
        }
        self.replace_modifiers([
            mod_capacity(shieldtype_bonus[equipment.shield_type])
        ])


class shd_part_fleet(ShieldPart):
    name = 'Fleet'
    effect = 'While Depleted: gain +2/P Movement.'

    def reload_modifiers(self):
        self.replace_modifiers([
            mod_fleet()
        ])


class shd_part_health(ShieldPart):
    name = 'Health'
    effect = 'Gain +20/P Max Health.'

    def reload_modifiers(self):
        self.replace_modifiers([
            mod_max_health(20)
        ])


class shd_part_nova(ShieldPart):
    name = 'Nova'
    effect = 'On Depletion: deal 2d6/P Elemental Damage to adjacent Enemies. Shield needs to have been fully Recharged for it to trigger again.'
    situational = True

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        return f"On Depletion: deal {n_parts * 2}d6 Elemental Damage to adjacent Enemies. Shield needs to have been fully Recharged for it to trigger again."


class shd_part_projected(ShieldPart):
    name = 'Projected'
    effect = 'While ADS: gain 1d6/P Damage Reduction.'
    situational = True

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        return f"While ADS: gain {n_parts}d6 Damage Reduction."


class shd_part_recharge(ShieldPart):
    name = 'Recharge'
    effect = 'Gain an extra 10/P Shield Recharge.'

    def apply(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        item.mod_stats['charge_rate'] += (n_parts * 10)

    def to_text(self, item):
        return f"Increased Shield Recharge Rate."


class shd_part_reflect(ShieldPart):
    name = 'Reflect'
    effect = 'When taking Ranged Damage: Roll a d100. 10%/P chance to Reflect Damage back to the Attacker. You take no Damage.'
    situational = True

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        return f"When taking Ranged Damage: Roll a d100. On a {100 - (n_parts * 10)}+: Reflect Damage back to the Attacker. You take no Damage."


class shd_part_resistant(ShieldPart):
    name = 'Resistant'
    effect = 'Gain an Extra 1d8/P Elemental Damage Reduction.'
    type = 'Unknown'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        return f"Gain {n_parts}d8 {self.type} Elemental Damage Reduction."


class shd_part_roid(ShieldPart):
    name = 'Roid'
    effect = 'While Depleted: add +1/P Melee Die to you Melee Attacks.'
    situational = True

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        return f"While Depleted: add +{n_parts} Melee Die to you Melee Attacks."


class shd_part_charge_health(ShieldPart):
    name = 'Charge'
    effect = 'When Damaged: Roll a d100. On a 75+, drop 1/P Common Health Potions (1d8).'

    def reload_modifiers(self):
        self.replace_modifiers([
            mod_health_booster()
        ])


class shd_part_charge_shield(ShieldPart):
    name = 'Charge'
    effect = 'When Damaged: Roll a d100. On a 75+, drop 1/P Common Shield Potions (1d8).'

    def reload_modifiers(self):
        self.replace_modifiers([
            mod_shield_booster()
        ])


class shd_part_spike(ShieldPart):
    name = 'Spike'
    effect = 'On taking Melee Damage: deal 1d10/P Damage to the Attacker.'
    situational = True

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        return f"On taking Melee Damage: deal {n_parts}d10 Elemental Damage to the Attacker."


class shd_part_turtle(ShieldPart):
    name = 'Turtle'
    effect = 'Gain an Extra (30/40/20)/P Shield Capacity (based on Shield Type). -10/P Max Health.'

    def reload_modifiers(self):
        equipment = self.linked_equipment
        shieldtype_bonus = {
            Shieldtypes.BALANCED: 30,
            Shieldtypes.HIGHCAPACITY: 40,
            Shieldtypes.FAST: 20
        }
        self.replace_modifiers([
            mod_capacity(shieldtype_bonus[equipment.shield_type]),
            mod_max_health(-10)
        ])


class shd_part_vagabond(ShieldPart):
    name = 'Vagabond'
    effect = 'While Full: Gain +2/P Movement.'
    situational = True

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])
        return f"While Full: Gain +{n_parts * 2} Movement."


class shd_trait_reverse_engineer(ShieldPart):
    name = 'Reverse Engineer'
    effect = 'This Shield is made using a Shield from another Manufacturer as a base.'

class shd_trait_symbiotic(ShieldPart):
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


class shd_tag_energy(ShieldPart):
    name = 'Energy'
    effect = 'Weak to Shock Damage.'


class shd_tag_alloy(ShieldPart):
    name = 'Alloy'
    effect = 'Weak to Corrosive Damage.'


class shd_tag_bio(ShieldPart):
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