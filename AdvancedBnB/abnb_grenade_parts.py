from util import Modifier

# Delivery Mechanisms
class grn_delivery_exploder(Modifier):
    name = 'Exploder'
    effect = 'You Throw the Grenade. It Explodes when it Hits an Enemy.'
    situational = True


class grn_delivery_homing(Modifier):
    name = 'Homing'
    effect = 'The Grenade seeks out the closest Enemy, but will Detonate when it Hits an Obstacle.'
    situational = True


class grn_delivery_impact(Modifier):
    name = 'Impact'
    effect = 'You Throw the Grenade. It Explodes when it Hits anything.'
    situational = True


class grn_delivery_lobbed(Modifier):
    name = 'Lobbed'
    effect = 'You Throw the Grenade. It Explodes at the end of your Turn.'
    situational = True


class grn_delivery_longbow(Modifier):
    name = 'Longbow'
    effect = 'The Grenade Teleports to the Target, ignoring Cover.'
    situational = True


class grn_delivery_rubberized(Modifier):
    name = 'Rubberized'
    effect = 'You Throw the Grenade. After it Detonates, it Bounces 2 squares and Detonates again.'
    situational = True


# Payloads
class grn_payload_standard(Modifier):
    name = 'Trinket'
    effect = 'Looks cool, does nothing.'


class grn_payload_bouncy(Modifier):
    name = 'Bouncy'
    effect = 'Bounces 2 squares and Detonates +1/P extra times.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])

        return f"Bounces 2 squares and Detonates {n_parts} extra time{'s' if n_parts > 1 else ''}."


class grn_payload_jumping(Modifier):
    name = 'Jumping'
    effect = 'The Grenade Explodes in place at the end of the next 1/P turns.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])

        return f"The Grenade Explodes in place at the end of the next {n_parts} turn{'s' if n_parts > 1 else ''}."


class grn_payload_force(Modifier):
    name = 'Force'
    effect = 'The Grenade Knocks Back Enemies 1/P Squares.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])

        return f"The Grenade Knocks Back Enemies {n_parts} Square{'s' if n_parts > 1 else ''}."


class grn_payload_sticky(Modifier):
    name = 'Sticky'
    effect = 'Deals an Extra 1d12/P Damage to Enemies on Direct hit.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])

        return f"Deals an Extra {n_parts}d12 Damage to Enemies on Direct hit."


class grn_payload_singularity(Modifier):
    name = 'Singularity'
    effect = 'Pulls in all enemies within 1+1/P spaces 1/P spaces closer before exploding.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])

        return f"Pulls all Enemies within {n_parts + 1} spaces {n_parts} space{'s' if n_parts > 1 else ''} closer before exploding."


class grn_payload_roider(Modifier):
    name = 'Roider'
    effect = '+1d8/P Base Damage'

    def to_text(self, item):
        return f"Increases Grenade Damage."

    def apply(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])

        item.mod_stats['dmg_dice'].count += n_parts


class grn_payload_elemental(Modifier):
    name = 'Elemental'
    effect = 'Grenade gains 1d6/P Elemental Damage and +20%/P Elemental Effect Chance.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])

        return f"Gains {n_parts}d6 Elemental Damage. Increases Elemental Effect Chance."

    def apply(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])

        item.mod_stats.setdefault('mods', {}).setdefault('status_effect_chance', 0)
        item.mod_stats['mods']['status_effect_chance'] += n_parts * 20


class grn_payload_puddle_blight(Modifier):
    name = 'Puddle (Blight)'
    effect = 'Creates Radiation Puddles in Adjacent Spaces for 2 turns. If P is 2 or higher, gain +1 Elemental Damage Die and +10% Irradiation Chance for each P after the 1st.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])

        effect_str = f"Creates Radiation Puddles in Adjacent Spaces for 2 turns."
        if n_parts >= 2:
            effect_str += f" Gain +{n_parts-1} Elemental Damage Die and +{(n_parts-1) * 10}% Irradiation Chance."

        return effect_str


class grn_payload_puddle_chiller(Modifier):
    name = 'Puddle (Chiller)'
    effect = 'Creates Cryo Puddles in Adjacent Spaces for 2 turns. If P is 2 or higher, gain +1 Elemental Damage Die and +10% Slow Chance for each P after the 1st.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])

        effect_str = f"Creates Cryo Puddles in Adjacent Spaces for 2 turns."
        if n_parts >= 2:
            effect_str += f" Gain +{n_parts-1} Elemental Damage Die and +{(n_parts-1) * 10}% Slow Chance."

        return effect_str


class grn_payload_puddle_corrupter(Modifier):
    name = 'Puddle (Corrupter)'
    effect = 'Creates Corrosive Puddles in Adjacent Spaces for 2 turns. If P is 2 or higher, gain +1 Elemental Damage Die and +10% Melt Chance for each P after the 1st.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])

        effect_str = f"Creates Corrosive Puddles in Adjacent Spaces for 2 turns."
        if n_parts >= 2:
            effect_str += f" Gain +{n_parts-1} Elemental Damage Die and +{(n_parts-1) * 10}% Melt Chance."

        return effect_str


class grn_payload_puddle_flamer(Modifier):
    name = 'Puddle (Flamer)'
    effect = 'Creates Incendiary Puddles in Adjacent Spaces for 2 turns. If P is 2 or higher, gain +1 Elemental Damage Die and +10% Burn Chance for each P after the 1st.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])

        effect_str = f"Creates Incendiary Puddles in Adjacent Spaces for 2 turns."
        if n_parts >= 2:
            effect_str += f" Gain +{n_parts-1} Elemental Damage Die and +{(n_parts-1) * 10}% Burn Chance."

        return effect_str


class grn_payload_puddle_slagger(Modifier):
    name = 'Puddle (Slagger)'
    effect = 'Creates Slag Puddles in Adjacent Spaces for 2 turns. If P is 2 or higher, gain +1 Elemental Damage Die and +10% Slag Chance for each P after the 1st.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])

        effect_str = f"Creates Slag Puddles in Adjacent Spaces for 2 turns."
        if n_parts >= 2:
            effect_str += f" Gain +{n_parts-1} Elemental Damage Die and +{(n_parts-1) * 10}% Slag Chance."

        return effect_str


class grn_payload_puddle_tesla(Modifier):
    name = 'Puddle (Tesla)'
    effect = 'Creates Shock Puddles in Adjacent Spaces for 2 turns. If P is 2 or higher, gain +1 Elemental Damage Die and +10% Electrocute Chance for each P after the 1st.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])

        effect_str = f"Creates Shock Puddles in Adjacent Spaces for 2 turns."
        if n_parts >= 2:
            effect_str += f" Gain +{n_parts-1} Elemental Damage Die and +{(n_parts-1) * 10}% Electrocute Chance."

        return effect_str


class grn_payload_link(Modifier):
    name = 'Link'
    effect = 'Deals an extra 1d4/P Damage to all enemies, for each enemy damaged.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])

        return f"For each enemy Damaged by the Explosion, deals an extra {n_parts}d4 Damage to all enemies."


class grn_payload_money(Modifier):
    name = 'Money'
    effect = 'Gain 10g/P for each enemy damaged.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])

        return f"Gain {10 * n_parts}g for each Enemy Damaged."


class grn_payload_transfusion(Modifier):
    name = 'Transfusion'
    effect = 'After Detonating create 1/P Healing Orbs. Each moves to an Ally and restores Health equal to half the Damage dealt.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])

        return f"After Detonating create {n_parts} Healing Orb{'s' if n_parts > 0 else ''}. Each moves to an Ally and restores Health equal to half the Damage dealt."


class grn_payload_generator(Modifier):
    name = 'Generator'
    effect = 'After Detonating create 1/P Recharge Orbs. Each moves to an Ally and restores Shield equal to half the Damage dealt.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])

        return f"After Detonating create {n_parts} Recharge Orb{'s' if n_parts > 0 else ''}. Each moves to an Ally and restores Shield equal to half the Damage dealt."


class grn_payload_large(Modifier):
    name = 'Large'
    effect = 'The Grenade gains +1/P Splash.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])

        return f"The Grenade gains +{n_parts} Splash."

    def apply(self, item):
        item.mod_stats.setdefault('mods', {}).setdefault('splash', 0)
        item.mod_stats['mods']['splash'] = 1


class grn_payload_mirv(Modifier):
    name = 'MIRV'
    effect = 'After detonating Releases 1/P Child Grenades in adjacent spaces that deal 1d6 Damage (+1d6 Damage at Tier 3, 5, 7, and 9).'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])

        n_dice = 1
        if item.tier >= 9:
            n_dice += 1
        if item.tier >= 7:
            n_dice += 1
        if item.tier >= 5:
            n_dice += 1
        if item.tier >= 3:
            n_dice += 1

        return f"After detonating Releases {n_parts} Child Grenade{'s' if n_parts > 1 else ''} in Adjacent Spaces that each deal {n_dice}d6 Damage."


class grn_payload_mini_mirv(Modifier):
    name = 'Mini MIRV'
    effect = 'If you have no MIRV Parts gain MIRV, otherwise; Child Grenades Releases 1/P Baby Grenades in adjacent spaces, that deal 1d4 Damage (+1d4 Damage at Tier 3, 5, 7, and 9).'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])

        n_dice = 1
        if item.tier >= 9:
            n_dice += 1
        if item.tier >= 7:
            n_dice += 1
        if item.tier >= 5:
            n_dice += 1
        if item.tier >= 3:
            n_dice += 1

        return f"MIRV Child Grenades Releases {n_parts} Baby Grenade{'s' if n_parts > 1 else ''} in Adjacent Spaces that each deal {n_dice}d4 Damage."


class grn_payload_nuke(Modifier):
    name = 'Nuke'
    effect = "Consumes +1/P Grenade when thrown. Increase the Grenade's Damage by half of the it's Base Damage. If P is 2 Double the base Damage."

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])

        return f"Consumes +{n_parts} Grenade{'s' if n_parts > 1 else ''} when Thrown. Increases Damage."

    def apply(self, item):
        dice_count = item.base_stats['dmg_dice'].count
        n_parts = len([x for x in item.parts if x.name == self.name])

        item.mod_stats['dmg_dice'].count += round(n_parts * 0.5 * dice_count)


class grn_payload_divider(Modifier):
    name = 'Divider'
    effect = 'The Grenade splits into 2 when Thrown. They land in Adjacent Squares.'


grenade_base_stats = {
    1: '1d8',
    2: '2d8',
    3: '3d8',
    4: '4d8',
    5: '5d8',
    6: '6d8',
    7: '7d8',
    8: '8d8',
    9: '9d8',
    10: '10d8'
}

grenade_delivery_mechanism = {
    1: grn_delivery_exploder(),
    2: grn_delivery_homing(),
    3: grn_delivery_impact(),
    4: grn_delivery_lobbed(),
    5: grn_delivery_longbow(),
    6: grn_delivery_rubberized()
}

grenade_payload_table = {
    (1, 5): grn_payload_standard(),
    (6, 10): grn_payload_bouncy(),
    (11, 15): grn_payload_jumping(),
    (16, 20): grn_payload_force(),
    (21, 25): grn_payload_sticky(),
    (26, 30): grn_payload_singularity(),
    (31, 35): grn_payload_roider(),
    (36, 40): grn_payload_elemental(),
    (41, 43): grn_payload_puddle_blight(),
    (44, 46): grn_payload_puddle_chiller(),
    (47, 49): grn_payload_puddle_corrupter(),
    (50, 52): grn_payload_puddle_flamer(),
    (53, 55): grn_payload_puddle_slagger(),
    (56, 58): grn_payload_puddle_tesla(),
    (59, 63): grn_payload_link(),
    (64, 68): grn_payload_money(),
    (69, 73): grn_payload_transfusion(),
    (74, 78): grn_payload_generator(),
    (79, 83): grn_payload_large(),
    (84, 88): grn_payload_mirv(),
    (89, 92): grn_payload_mini_mirv(),
    (93, 96): grn_payload_nuke(),
    (97, 100): grn_payload_divider()
}
