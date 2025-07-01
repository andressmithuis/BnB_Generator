import os
import yaml

import StandardBnB
import AdvancedBnB
from util import Rarity


def load_item_config():
    props = {}

    # Load YAML file
    file_name = 'item_config.yaml'
    if os.path.isfile(file_name):
        with open(file_name, 'r') as file:
            yaml_config = yaml.safe_load(file)
    else:
        # No config file found, return empty properties
        return props


    if yaml_config is not None:
        # Item Name
        if 'item_name' in yaml_config:
            props['item_name'] = yaml_config['item_name']

        # Item Level
        if 'item_level' in yaml_config:
            props['item_level'] = yaml_config['item_level']

        # Manufacturer/Guild
        if 'manufacturer' in yaml_config:
            manufacturer_alias = {
                # Standard BnB Guilds
                'ashen': StandardBnB.Guilds.ASHEN,
                'alas': StandardBnB.Guilds.ALAS,
                'skulldugger': StandardBnB.Guilds.SKULLDUGGER,
                'dahlia': StandardBnB.Guilds.DAHLIA,
                'blackpowder': StandardBnB.Guilds.BLACKPOWDER,
                'malefactor': StandardBnB.Guilds.MALEFACTOR,
                'hyperius': StandardBnB.Guilds.HYPERIUS,
                'feriore': StandardBnB.Guilds.FERIORE,
                'torgue_sbnb': StandardBnB.Guilds.TORGUE,
                'stoker': StandardBnB.Guilds.STOKER,
                'pangoblin': StandardBnB.Guilds.PANGOBLIN,

                # Advanced BnB Manufacturers
                'anshin': AdvancedBnB.Manufacturers.ANSHIN,
                'atlas': AdvancedBnB.Manufacturers.ATLAS,
                'bandit': AdvancedBnB.Manufacturers.BANDIT,
                'dahl': AdvancedBnB.Manufacturers.DAHL,
                'eridian': AdvancedBnB.Manufacturers.ERIDIAN,
                'hyperion': AdvancedBnB.Manufacturers.HYPERION,
                'jakobs': AdvancedBnB.Manufacturers.JAKOBS,
                'maliwan': AdvancedBnB.Manufacturers.MALIWAN,
                'pangolin': AdvancedBnB.Manufacturers.PANGOLIN,
                'tediore': AdvancedBnB.Manufacturers.TEDIORE,
                'torgue_abnb': AdvancedBnB.Manufacturers.TORGUE,
                'vladof': AdvancedBnB.Manufacturers.VLADOF,
            }

            props['manufacturer'] = manufacturer_alias[yaml_config['manufacturer'].lower()]

        # Item (sub)type
        if 'item_type' in yaml_config:
            if 'use_abnb' in yaml_config and yaml_config['use_abnb'] is True:
                item_type_alias = {
                    # Advanced BnB Guntypes
                    'pistol': AdvancedBnB.Guntypes.PISTOL,
                    'smg': AdvancedBnB.Guntypes.SMG,
                    'rifle': AdvancedBnB.Guntypes.RIFLE,
                    'shotgun': AdvancedBnB.Guntypes.SHOTGUN,
                    'sniper': AdvancedBnB.Guntypes.SNIPER,
                    'launcher': AdvancedBnB.Guntypes.LAUNCHER,

                    # Advanced BnB Shield
                    'balanced': AdvancedBnB.Shieldtypes.BALANCED,
                    'high_capacity': AdvancedBnB.Shieldtypes.HIGHCAPACITY,
                    'fast': AdvancedBnB.Shieldtypes.FAST,
                }
            else:
                item_type_alias = {
                    # Standard BnB Guntypes
                    'pistol': StandardBnB.Guntypes.PISTOL,
                    'smg': StandardBnB.Guntypes.SMG,
                    'rifle': StandardBnB.Guntypes.RIFLE,
                    'shotgun': StandardBnB.Guntypes.SHOTGUN,
                    'sniper': StandardBnB.Guntypes.SNIPER,
                    'launcher': StandardBnB.Guntypes.LAUNCHER,
                }

            props['item_type'] = item_type_alias[yaml_config['item_type'].lower()]

        # Rarity
        if 'rarity' in yaml_config:
            rarity_alias = {
                'common': Rarity.COMMON,
                'uncommon': Rarity.UNCOMMON,
                'rare': Rarity.RARE,
                'epic': Rarity.EPIC,
                'legendary': Rarity.LEGENDARY,
                'pearlescent': Rarity.PEARLESCENT,
            }

            props['rarity'] = rarity_alias[yaml_config['rarity'].lower()]

    return props
