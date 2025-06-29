import os.path
import random

from resource_loading import load_resources
from util import Rarity

from StandardBnB import HealthPotion

USE_ABNB_SYSTEM = False  # Set to True to generate equipment using the new Advanced BnB Loot Generation Rulesets

if USE_ABNB_SYSTEM:
    from AdvancedBnB import Gun, Shield
    from AdvancedBnB import Manufacturers, Guntypes
else:
    from StandardBnB import Gun, Shield


if __name__ == '__main__':
    # If the assets are not loaded in yet, start the download
    if not os.path.isfile('assets.json'):
        print(f"Item Assets not loaded yet. Start Loading...")
        load_resources()

    props = {
        # 'level': 30,
        # 'manufacturer': Manufacturers.ERIDIAN,
        # 'gun_type': Guntypes.RIFLE,
        # 'rarity': Rarity.PEARLESCENT,
    }

    # Generate Gun Card
    if True:
        new_gun = Gun()
        new_gun.generate(props=props)

        print(new_gun)
        new_gun.generate_card()

    #Generate Shield Card
    if False:
        new_shield = Shield()
        new_shield.generate(props=props)

        print(new_shield)
        new_shield.generate_card()

    # Generate Potion Card
    if False:
        new_potion = HealthPotion(Rarity.LEGENDARY)
        new_potion.generate_card()
