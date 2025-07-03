from util import Modifier

# Delivery Mechanisms
class grn_delivery_exploder(Modifier):
    name = 'Exploder'
    effect = 'You Throw the Grenade. It Explodes when it Hits an Enemy.'


class grn_delivery_homing(Modifier):
    name = 'Homing'
    effect = 'The Grenade automatically Hits the closest Enemy.'


class grn_delivery_impact(Modifier):
    name = 'Impact'
    effect = 'You Throw the Grenade. It Explodes when it Hits anything.'


class grn_delivery_lobbed(Modifier):
    name = 'Lobbed'
    effect = 'You Throw the Grenade. It Explodes at the end of your Turn.'


class grn_delivery_longbow(Modifier):
    name = 'Longbow'
    effect = 'The Grenade Teleports to the target, ignoring Cover.'


class grn_delivery_rubberized(Modifier):
    name = 'Rubberized'
    effect = 'You Throw the Grenade. After it Detonates, it Bounces 2 squares and Detonates again.'


# Payloads
class grn_payload_standard(Modifier):
    name = 'Standard'
    effect = 'No Special Effects.'


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


class grn_payload_transfusion(Modifier):
    name = 'Transfusion'
    effect = 'After Detonating create 1/P Healing Orbs. Each moves to an Ally and restores Health equal to half the Damage dealt.'

    def to_text(self, item):
        n_parts = len([x for x in item.parts if x.name == self.name])

        return f"After Detonating create {n_parts} Healing Orb{'s' if n_parts > 0 else ''}. Each moves to an Ally and restores Health equal to half the Damage dealt."


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
    (16, 20): grn_payload_force()
}
