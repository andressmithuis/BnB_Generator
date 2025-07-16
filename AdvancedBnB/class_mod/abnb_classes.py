from .abnb_class_mods_combined import *

classes_table = {
    1: 'Assassin',
    2: 'Baroness',
    3: 'Beast Master',
    4: 'Berserker',
    5: 'Commando',
    6: 'Doppelganger',
    7: 'Enforcer',
    8: 'Gladiator',
    9: 'Gunner',
    10: 'Gunzerker',
    11: 'Hunter',
    12: 'Law Bringer',
    13: 'Mechromancer',
    14: 'Operative',
    15: 'Psycho',
    16: 'Siren Alpha',
    17: 'Siren Beta',
    18: 'Siren Gamma',
    19: 'Soldier',
    20: 'Wild Card'
}

class_mods_per_class = {
    'Assassin': {
        1: cm_aimbot(),
        2: cm_battery(),
        (3, 20): cm_battery(),
    }
}