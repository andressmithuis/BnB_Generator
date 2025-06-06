import os.path
import random

from resource_loading import load_resources
from util import Rarity

from StandardBnB import HealthPotion, Shield

USE_ABNB_SYSTEM = False  # Set to True to generate equipment using the new Advanced BnB Loot Generation Rulesets

if USE_ABNB_SYSTEM:
    from AdvancedBnB import Gun
else:
    from StandardBnB import Gun


if __name__ == '__main__':
    # If the assets are not loaded in yet, start the download
    if not os.path.isfile('assets.json'):
        print(f"Item Assets not loaded yet. Start Loading...")
        load_resources()

    # Generate Gun Card
    if True:
        props = {
            # 'level': 1,
            # 'manufacturer': Manufacturers.ERIDIAN,
            # 'gun_type': Guntypes.PISTOL,
            # 'rarity': Rarity.LEGENDARY,
        }

        new_gun = Gun()
        new_gun.generate(props=props)

        print(new_gun)
        new_gun.generate_card()

    #Generate Shield Card
    if False:
        new_shield = Shield()
        new_shield.generate(level=random.randint(1, 30))

        print(new_shield)
        new_shield.generate_card()

    # Generate Potion Card
    if False:
        new_potion = HealthPotion(Rarity.COMMON)
        new_potion.generate_card()
