from util import Rarity
from .bnb_guilds import Guilds
from .bnb_guntypes import Guntypes
from util.elements import *
from util import Dice

# Page 81
gun_table = [
    {"item_type": Guntypes.PISTOL, "guild": [Guilds.ALAS, Guilds.DAHLIA, Guilds.HYPERIUS, Guilds.MALEFACTOR, Guilds.FERIORE, Guilds.STOKER, Guilds.TORGUE, Guilds.BLACKPOWDER]},
    {"item_type": Guntypes.SMG, "guild": [Guilds.DAHLIA, Guilds.HYPERIUS, Guilds.MALEFACTOR, Guilds.FERIORE, Guilds.TORGUE, Guilds.DAHLIA, Guilds.HYPERIUS, Guilds.MALEFACTOR]},
    {"item_type": Guntypes.SHOTGUN, "guild": [Guilds.HYPERIUS, Guilds.MALEFACTOR, Guilds.SKULLDUGGER, Guilds.STOKER, Guilds.ALAS, Guilds.DAHLIA, Guilds.BLACKPOWDER, Guilds.FERIORE]},
    {"item_type": Guntypes.RIFLE, "guild": [Guilds.SKULLDUGGER, Guilds.DAHLIA, Guilds.BLACKPOWDER, Guilds.TORGUE, Guilds.STOKER, Guilds.SKULLDUGGER, Guilds.DAHLIA, Guilds.BLACKPOWDER]},
    {"item_type": Guntypes.SNIPER, "guild": [Guilds.DAHLIA, Guilds.HYPERIUS, Guilds.BLACKPOWDER, Guilds.MALEFACTOR, Guilds.STOKER, Guilds.DAHLIA, Guilds.HYPERIUS, Guilds.BLACKPOWDER]},
    {"item_type": Guntypes.LAUNCHER, "guild": [Guilds.SKULLDUGGER, Guilds.MALEFACTOR, Guilds.FERIORE, Guilds.TORGUE, Guilds.STOKER, Guilds.SKULLDUGGER, Guilds.MALEFACTOR, Guilds.FERIORE]},
    {"item_type": 'favored', "guild": ['choice', 'choice', 'choice', 'choice', 'choice', 'choice', 'choice', 'choice']},
    {"item_type": 'favored', "guild": ['choice', 'choice', 'choice', 'choice', 'choice', 'choice', 'choice', 'choice']}
]

# Gun Table Fixed version from ChaosMoss in Discord
gun_table_v2 = {
    1: (Guntypes.PISTOL,    {1:Guilds.SKULLDUGGER, 2:Guilds.FERIORE, 3:Guilds.DAHLIA, 4:Guilds.BLACKPOWDER, 5:Guilds.ALAS, 6:Guilds.MALEFACTOR, 7:Guilds.STOKER, 8:Guilds.HYPERIUS}),
    2: (Guntypes.SMG,       {1:Guilds.MALEFACTOR, 2:Guilds.SKULLDUGGER, 3:Guilds.HYPERIUS, 4:Guilds.FERIORE, 5:Guilds.TORGUE, 6:Guilds.DAHLIA, 7:Guilds.SKULLDUGGER, 8:Guilds.FERIORE}),
    3: (Guntypes.SHOTGUN,   {1:Guilds.HYPERIUS, 2:Guilds.BLACKPOWDER, 3:Guilds.SKULLDUGGER, 4:Guilds.FERIORE, 5:Guilds.TORGUE, 6:Guilds.STOKER, 7:Guilds.ALAS, 8:Guilds.MALEFACTOR}),
    4: (Guntypes.RIFLE,     {1:Guilds.FERIORE, 2:Guilds.DAHLIA, 3:Guilds.TORGUE, 4:Guilds.STOKER, 5:Guilds.HYPERIUS, 6:Guilds.ALAS, 7:Guilds.DAHLIA, 8:Guilds.ALAS}),
    5: (Guntypes.SNIPER,    {1:Guilds.SKULLDUGGER, 2:Guilds.ALAS, 3:Guilds.BLACKPOWDER, 4:Guilds.MALEFACTOR, 5:Guilds.DAHLIA, 6:Guilds.HYPERIUS, 7:Guilds.STOKER, 8:Guilds.TORGUE}),
    6: (Guntypes.LAUNCHER,  {1:Guilds.STOKER, 2:Guilds.TORGUE, 3:Guilds.MALEFACTOR, 4:Guilds.HYPERIUS, 5:Guilds.STOKER, 6:Guilds.TORGUE, 7:Guilds.MALEFACTOR, 8:Guilds.HYPERIUS}),
    7: ('rolled_a_7',       {1:Guilds.TORGUE, 2:Guilds.DAHLIA, 3:Guilds.BLACKPOWDER, 4:Guilds.SKULLDUGGER, 5:Guilds.BLACKPOWDER, 6:Guilds.FERIORE, 7:Guilds.BLACKPOWDER, 8:'choice'}),
    8: ('favored',          {1:'choice', 2:'choice', 3:'choice', 4:'choice', 5:'choice', 6:'choice', 7:'choice', 8:'choice'})
}

rolled_a_7 = {
    1: Guntypes.PISTOL,
    2: Guntypes.SHOTGUN,
    3: Guntypes.PISTOL,
    4: Guntypes.SMG,
    5: Guntypes.SHOTGUN,
    6: Guntypes.RIFLE,
    7: Guntypes.SNIPER,
    8: Guntypes.LAUNCHER
}

# Page 81
rarity_table = {
    1: {1:(Rarity.COMMON, False),   2:(Rarity.COMMON, True),    3:(Rarity.COMMON, True),    4:(Rarity.UNCOMMON, False), 5:(Rarity.UNCOMMON, True),  6:(Rarity.RARE, False)},
    2: {1:(Rarity.COMMON, False),   2:(Rarity.COMMON, True),    3:(Rarity.UNCOMMON, False), 4:(Rarity.UNCOMMON, True),  5:(Rarity.RARE, True),      6:(Rarity.EPIC, False)},
    3: {1:(Rarity.UNCOMMON, True),  2:(Rarity.RARE, False),     3:(Rarity.RARE, True),      4:(Rarity.EPIC, False),     5:(Rarity.EPIC, True),      6:(Rarity.LEGENDARY, True)},
    4: {1:(Rarity.RARE, True),      2:(Rarity.RARE, True),      3:(Rarity.EPIC, True),      4:(Rarity.EPIC, True),      5:(Rarity.LEGENDARY, True), 6:(Rarity.LEGENDARY, True)}
}

# Page 82
elemental_table = {
    (1, 10):    {Rarity.COMMON: [],                Rarity.UNCOMMON: [],               Rarity.RARE: [],               Rarity.EPIC: [],                           Rarity.LEGENDARY: []},
    (11, 15):   {Rarity.COMMON: [],                Rarity.UNCOMMON: [],               Rarity.RARE: [],               Rarity.EPIC: [Radiation()],                Rarity.LEGENDARY: [Radiation()]},
    (16, 20):   {Rarity.COMMON: [],                Rarity.UNCOMMON: [],               Rarity.RARE: [],               Rarity.EPIC: [Corrosive()],                Rarity.LEGENDARY: [Corrosive()]},
    (21, 25):   {Rarity.COMMON: [],                Rarity.UNCOMMON: [],               Rarity.RARE: [],               Rarity.EPIC: [Shock()],                    Rarity.LEGENDARY: [Shock()]},
    (26, 30):   {Rarity.COMMON: [],                Rarity.UNCOMMON: [],               Rarity.RARE: [Radiation()],    Rarity.EPIC: [Explosive()],                Rarity.LEGENDARY: [Explosive()]},
    (31, 35):   {Rarity.COMMON: [],                Rarity.UNCOMMON: [],               Rarity.RARE: [Corrosive()],    Rarity.EPIC: [Incendiary()],               Rarity.LEGENDARY: [Incendiary()]},
    (36, 40):   {Rarity.COMMON: [],                Rarity.UNCOMMON: [],               Rarity.RARE: [Shock()],        Rarity.EPIC: [Cryo()],                     Rarity.LEGENDARY: [Cryo()]},
    (41, 45):   {Rarity.COMMON: [],                Rarity.UNCOMMON: [],               Rarity.RARE: [Explosive()],    Rarity.EPIC: [Radiation(1)],               Rarity.LEGENDARY: [Radiation(1)]},
    (46, 50):   {Rarity.COMMON: [],                Rarity.UNCOMMON: [],               Rarity.RARE: [Incendiary()],   Rarity.EPIC: [Corrosive(1)],               Rarity.LEGENDARY: [Corrosive(1)]},
    (51, 55):   {Rarity.COMMON: [],                Rarity.UNCOMMON: [],               Rarity.RARE: [Cryo()],         Rarity.EPIC: [Shock(1)],                   Rarity.LEGENDARY: [Shock(1)]},
    (56, 60):   {Rarity.COMMON: [],                Rarity.UNCOMMON: [Radiation()],    Rarity.RARE: [Radiation(1)],   Rarity.EPIC: [Explosive(1)],               Rarity.LEGENDARY: [Explosive(1)]},
    (61, 65):   {Rarity.COMMON: [],                Rarity.UNCOMMON: [Corrosive()],    Rarity.RARE: [Corrosive(1)],   Rarity.EPIC: [Incendiary(1)],              Rarity.LEGENDARY: [Incendiary(1)]},
    (66, 70):   {Rarity.COMMON: [],                Rarity.UNCOMMON: [Shock()],        Rarity.RARE: [Shock(1)],       Rarity.EPIC: [Cryo(1)],                    Rarity.LEGENDARY: [Cryo(1)]},
    (71, 75):   {Rarity.COMMON: [],                Rarity.UNCOMMON: [Explosive()],    Rarity.RARE: [Explosive(1)],   Rarity.EPIC: [Radiation(2)],               Rarity.LEGENDARY: [Radiation(2)]},
    (76, 80):   {Rarity.COMMON: [],                Rarity.UNCOMMON: [Incendiary()],   Rarity.RARE: [Incendiary(1)],  Rarity.EPIC: [Corrosive(2)],               Rarity.LEGENDARY: [Corrosive(2)]},
    (81, 85):   {Rarity.COMMON: [],                Rarity.UNCOMMON: [Cryo()],         Rarity.RARE: [Cryo(1)],        Rarity.EPIC: [Shock(2)],                   Rarity.LEGENDARY: [Shock(2)]},
    (86, 90):   {Rarity.COMMON: [Radiation()],     Rarity.UNCOMMON: [Radiation(1)],   Rarity.RARE: [Radiation(2)],   Rarity.EPIC: [Explosive(2)],               Rarity.LEGENDARY: [Explosive(2)]},
    (91, 92):   {Rarity.COMMON: [Corrosive()],     Rarity.UNCOMMON: [Corrosive(1)],   Rarity.RARE: [Corrosive(2)],   Rarity.EPIC: [Incendiary(2)],              Rarity.LEGENDARY: [Incendiary(2)]},
    (93, 94):   {Rarity.COMMON: [Shock()],         Rarity.UNCOMMON: [Shock(1)],       Rarity.RARE: [Shock(2)],       Rarity.EPIC: [Cryo(2)],                    Rarity.LEGENDARY: [Cryo(2)]},
    (95, 96):   {Rarity.COMMON: [Explosive()],     Rarity.UNCOMMON: [Explosive(1)],   Rarity.RARE: [Explosive(2)],   Rarity.EPIC: [Radiation(), Incendiary()],  Rarity.LEGENDARY: [Radiation(), Incendiary()]},
    (97, 98):   {Rarity.COMMON: [Incendiary()],    Rarity.UNCOMMON: [Incendiary(1)],  Rarity.RARE: [Incendiary(2)],  Rarity.EPIC: [Shock(), Corrosive()],       Rarity.LEGENDARY: [Shock(), Corrosive()]},
    (99, 100):  {Rarity.COMMON: [Cryo()],          Rarity.UNCOMMON: [Cryo(1)],        Rarity.RARE: [Cryo(2)],        Rarity.EPIC: [Explosive(), Cryo()],        Rarity.LEGENDARY: [Explosive(), Cryo()]},
}

# Page 93 ~ 98
guilds_per_weapon = {
    Guntypes.PISTOL: [Guilds.ALAS, Guilds.SKULLDUGGER, Guilds.DAHLIA, Guilds.BLACKPOWDER, Guilds.MALEFACTOR, Guilds.HYPERIUS, Guilds.FERIORE, Guilds.TORGUE, Guilds.STOKER],
    Guntypes.SMG: [Guilds.SKULLDUGGER, Guilds.DAHLIA, Guilds.MALEFACTOR, Guilds.HYPERIUS, Guilds.FERIORE, Guilds.TORGUE],
    Guntypes.SHOTGUN: [Guilds.ALAS, Guilds.SKULLDUGGER, Guilds.DAHLIA, Guilds.BLACKPOWDER, Guilds.MALEFACTOR, Guilds.HYPERIUS, Guilds.HYPERIUS, Guilds.TORGUE, Guilds.STOKER],
    Guntypes.RIFLE: [Guilds.ALAS, Guilds.DAHLIA, Guilds.HYPERIUS, Guilds.FERIORE, Guilds.TORGUE, Guilds.STOKER],
    Guntypes.SNIPER: [Guilds.ALAS, Guilds.SKULLDUGGER, Guilds.DAHLIA, Guilds.BLACKPOWDER, Guilds.MALEFACTOR, Guilds.HYPERIUS, Guilds.TORGUE, Guilds.STOKER],
    Guntypes.LAUNCHER: [Guilds.MALEFACTOR, Guilds.HYPERIUS, Guilds.TORGUE, Guilds.STOKER]
}

# Page 88
shield_guild_table = {
    1: Guilds.ASHEN,
    2: Guilds.ALAS,
    3: Guilds.DAHLIA,
    4: Guilds.FERIORE,
    5: Guilds.MALEFACTOR,
    6: Guilds.PANGOBLIN,
    7: Guilds.STOKER,
    8: Guilds.TORGUE
}



