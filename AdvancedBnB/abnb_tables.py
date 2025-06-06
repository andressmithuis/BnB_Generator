import numpy as np

from .abnb_weapon_parts import *
from .abnb_manufacturers import *
from .abnb_element import *
from util import Rarity

level_to_tiers = {
    (1, 6): 1,
    (7, 12): 2,
    (13, 18): 3,
    (19, 24): 4,
    (25, 30): 5,
    (31, 35): 6,
    (36, 40): 7,
    (41, 45): 8,
    (46, 50): 9,
    (51, np.inf): 10
}

manufacturer_table = {
    1: Manufacturers.ANSHIN,
    2: Manufacturers.ATLAS,
    3: Manufacturers.BANDIT,
    4: Manufacturers.ERIDIAN,
    5: Manufacturers.DAHL,
    6: Manufacturers.HYPERION,
    7: Manufacturers.JAKOBS,
    8: Manufacturers.MALIWAN,
    9: Manufacturers.PANGOLIN,
    10: Manufacturers.TEDIORE,
    11: Manufacturers.TORGUE,
    12: Manufacturers.VLADOF
}

rarity_tables = {
    'normal': {
        1: { 1: (Rarity.COMMON, False), 2: (Rarity.COMMON, True), 3: (Rarity.UNCOMMON, False), 4: (Rarity.UNCOMMON, True), 5: (Rarity.RARE, False), 6: (Rarity.RARE, True)},
        2: { 1: (Rarity.COMMON, True), 2: (Rarity.UNCOMMON, False), 3: (Rarity.UNCOMMON, True), 4: (Rarity.RARE, False), 5: (Rarity.RARE, True), 6: (Rarity.EPIC, True)},
        3: { 1: (Rarity.UNCOMMON, False), 2: (Rarity.UNCOMMON, True), 3: (Rarity.RARE, False), 4: (Rarity.RARE, True), 5: (Rarity.EPIC, False), 6: (Rarity.EPIC, True)},
        4: { 1: (Rarity.UNCOMMON, True), 2: (Rarity.RARE, False), 3: (Rarity.RARE, True), 4: (Rarity.EPIC, False), 5: (Rarity.EPIC, True), 6: (Rarity.LEGENDARY, True)},
    }
}

weapon_part_count = {
    Rarity.COMMON:         0,
    Rarity.UNCOMMON:       1,
    Rarity.RARE:           2,
    Rarity.EPIC:           3,
    Rarity.LEGENDARY:      4,
    Rarity.PEARLESCENT:    5
}

elemental_table = {
    ( 1,  4):   { Rarity.COMMON: None, Rarity.UNCOMMON: None, Rarity.RARE: None,                 Rarity.EPIC: None,                             Rarity.LEGENDARY: None,                            Rarity.PEARLESCENT: None},
    ( 5,  8):   { Rarity.COMMON: None, Rarity.UNCOMMON: None, Rarity.RARE: None,                 Rarity.EPIC: Incendiary(),              Rarity.LEGENDARY: Incendiary(),             Rarity.PEARLESCENT: Incendiary(1)},
    ( 9, 12):   { Rarity.COMMON: None, Rarity.UNCOMMON: None, Rarity.RARE: None,                 Rarity.EPIC: Shock(),                   Rarity.LEGENDARY: Shock(),                  Rarity.PEARLESCENT: Shock(1)},
    (13, 16):   { Rarity.COMMON: None, Rarity.UNCOMMON: None, Rarity.RARE: None,                 Rarity.EPIC: Corrosive(),               Rarity.LEGENDARY: Corrosive(),              Rarity.PEARLESCENT: Corrosive(1)},
    (17, 20):   { Rarity.COMMON: None, Rarity.UNCOMMON: None, Rarity.RARE: Incendiary(),  Rarity.EPIC: Explosive(),               Rarity.LEGENDARY: Explosive(),              Rarity.PEARLESCENT: Explosive(1)},
    (21, 24):   { Rarity.COMMON: None, Rarity.UNCOMMON: None, Rarity.RARE: Shock(),       Rarity.EPIC: Slag(),                    Rarity.LEGENDARY: Slag(),                   Rarity.PEARLESCENT: Slag(1)},
    (25, 28):   { Rarity.COMMON: None, Rarity.UNCOMMON: None, Rarity.RARE: Corrosive(),   Rarity.EPIC: Cryo(),                    Rarity.LEGENDARY: Cryo(),                   Rarity.PEARLESCENT: Cryo(1)},
    (29, 32):   { Rarity.COMMON: None, Rarity.UNCOMMON: None, Rarity.RARE: Explosive(),   Rarity.EPIC: Radiation(),               Rarity.LEGENDARY: Radiation(),              Rarity.PEARLESCENT: Radiation(1)},
    (33, 36):   { Rarity.COMMON: None, Rarity.UNCOMMON: None, Rarity.RARE: Slag(),        Rarity.EPIC: Incendiary(1),     Rarity.LEGENDARY: Incendiary(1),   Rarity.PEARLESCENT: Incendiary(2)},
    (37, 40):   { Rarity.COMMON: None, Rarity.UNCOMMON: None, Rarity.RARE: Cryo(),        Rarity.EPIC: Shock(1),          Rarity.LEGENDARY: Shock(1),        Rarity.PEARLESCENT: Shock(2)},
    (41, 44):   { Rarity.COMMON: None, Rarity.UNCOMMON: None, Rarity.RARE: Radiation(),   Rarity.EPIC: Corrosive(1),      Rarity.LEGENDARY: Corrosive(1),    Rarity.PEARLESCENT: Corrosive(2)},
    (45, 48):   { Rarity.COMMON: None, Rarity.UNCOMMON: Incendiary(), Rarity.RARE: Incendiary(1),  Rarity.EPIC: Explosive(1),      Rarity.LEGENDARY: Explosive(1),    Rarity.PEARLESCENT: Explosive(2)},
    (49, 52):   { Rarity.COMMON: None, Rarity.UNCOMMON: Shock(), Rarity.RARE: Shock(1),       Rarity.EPIC: Slag(1),           Rarity.LEGENDARY: Slag(1),         Rarity.PEARLESCENT: Slag(2)},
    (53, 56):   { Rarity.COMMON: None, Rarity.UNCOMMON: Corrosive(), Rarity.RARE: Corrosive(1),   Rarity.EPIC: Cryo(1),           Rarity.LEGENDARY: Cryo(1),         Rarity.PEARLESCENT: Cryo(2)},
    (57, 60):   { Rarity.COMMON: None, Rarity.UNCOMMON: Explosive(), Rarity.RARE: Explosive(1),   Rarity.EPIC: Radiation(1),      Rarity.LEGENDARY: Radiation(1),    Rarity.PEARLESCENT: Radiation(2)},
    (61, 64):   { Rarity.COMMON: None, Rarity.UNCOMMON: Slag(), Rarity.RARE: Slag(1),                Rarity.EPIC: Incendiary(2), Rarity.LEGENDARY: Incendiary(2), Rarity.PEARLESCENT: Fusion()},
    (65, 68):   { Rarity.COMMON: None, Rarity.UNCOMMON: Cryo(), Rarity.RARE: Cryo(1),                Rarity.EPIC: Shock(2), Rarity.LEGENDARY: Shock(2),Rarity.PEARLESCENT: Fusion()},
    (69, 72):   { Rarity.COMMON: None, Rarity.UNCOMMON: Radiation(), Rarity.RARE: Radiation(1),           Rarity.EPIC: Corrosive(2),Rarity.LEGENDARY: Corrosive(2), Rarity.PEARLESCENT: Fusion()},
    (73, 76):   { Rarity.COMMON: Incendiary(), Rarity.UNCOMMON: Incendiary(1), Rarity.RARE: Incendiary(2), Rarity.EPIC: Explosive(2),Rarity.LEGENDARY: Explosive(2), Rarity.PEARLESCENT: Fusion()},
    (77, 80):   { Rarity.COMMON: Shock(), Rarity.UNCOMMON: Shock(1), Rarity.RARE: Shock(2),      Rarity.EPIC: Slag(2), Rarity.LEGENDARY: Slag(2), Rarity.PEARLESCENT: Fusion()},
    (81, 84):   { Rarity.COMMON: Corrosive(), Rarity.UNCOMMON: Corrosive(1), Rarity.RARE: Corrosive(2),  Rarity.EPIC: Cryo(2), Rarity.LEGENDARY: Cryo(2), Rarity.PEARLESCENT: Fusion()},
    (85, 88):   { Rarity.COMMON: Explosive(), Rarity.UNCOMMON: Explosive(1), Rarity.RARE: Explosive(2),  Rarity.EPIC: Radiation(2),Rarity.LEGENDARY: Radiation(2), Rarity.PEARLESCENT: Fusion()},
    (89, 92):   { Rarity.COMMON: Slag(), Rarity.UNCOMMON: Slag(1), Rarity.RARE: Slag(2),  Rarity.EPIC: Fusion(),Rarity.LEGENDARY: Fusion(), Rarity.PEARLESCENT: Fusion(1)},
    (93, 96):   { Rarity.COMMON: Cryo(), Rarity.UNCOMMON: Cryo(1), Rarity.RARE: Cryo(2),  Rarity.EPIC: Fusion(),Rarity.LEGENDARY: Fusion(), Rarity.PEARLESCENT: Fusion(1)},
    (97, 100):   { Rarity.COMMON: Radiation(), Rarity.UNCOMMON: Radiation(1), Rarity.RARE: Radiation(2),  Rarity.EPIC: Fusion(),Rarity.LEGENDARY: Fusion(), Rarity.PEARLESCENT: Fusion(1)},
}

fusion_table = {
    1: {1: None,        2: Plasma(),        3: Napalm(),    4: Blast(),     5: Chemical(),      6: Frostburn(), 7: Solar(),     8: 'special'},
    2: {1: Plasma(),    2: None,            3: Virus(),     4: Emp(),       5: Quicksilver(),   6: Frostbyte(), 7: Energy(),    8: 'special'},
    3: {1: Napalm(),    2: Virus(),         3: None,        4: Decay(),     5: Alkali(),        6: Gangrene(),  7: Fission(),   8: 'special'},
    4: {1: Blast(),     2: Emp(),           3: Decay(),     4: None,        5: Tincture(),      6: Void(),      7: Nuke(),      8: 'special'},
    5: {1: Chemical(),  2: Quicksilver(),   3: Alkali(),    4: Tincture(),  5: None,            6: Coolant(),   7: Force(),     8: 'special'},
    6: {1: Frostburn(), 2: Frostbyte(),     3: Gangrene(),  4: Void(),      5: Coolant(),       6: None,        7: Entropy(),   8: 'special'},
    7: {1: Solar(),     2: Energy(),        3: Fission(),   4: Nuke(),      5: Force(),         6: Entropy(),   7: None,        8: 'special'},
    8: {1: 'special',   2: 'special',       3: 'special',   4: 'special',   5: 'special',       6: 'special',   7: 'special',   8: 'special'},
}

