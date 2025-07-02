import os.path
import argparse

from resource_loading import load_resources
from load_item_config import load_item_config

from StandardBnB import HealthPotion, ShieldPotion


if __name__ == '__main__':
    # --- CLI Argument Parser ---
    cli_parser = argparse.ArgumentParser(description='Bunkers&Badasses Loot Generator')
    cli_subparsers = cli_parser.add_subparsers(dest='command', required=True)

    # Subcommand: load_resources
    parser_load = cli_subparsers.add_parser('load', help='Initiate loading of resources')
    parser_load.add_argument(
        '--games',
        nargs='+',
        choices=['bl1', 'bl2', 'bl3', 'bl-tps', 'bl-wl'],
        help='Which games to pull resources from',
        default=['bl3']
    )
    parser_load.add_argument(
        '--items',
        nargs='+',
        choices=['all', 'weapons', 'shields'],
        help='Which item category to pull',
        default=['all']
    )
    parser_load.add_argument('--reset', action='store_true', help='Removes any existing resources')

    # Subcommand: generate_item
    parser_create = cli_subparsers.add_parser('generate', help='Which item to generate a card for')
    parser_create.add_argument('item_type', choices=['gun', 'shield', 'health_potion', 'shield_potion'], help='Select what kind of item to generate a card for')
    parser_create.add_argument('--use-abnb', action='store_true', help='Enable Advanced Bunkers&Badasses')

    args = cli_parser.parse_args()

    if args.command == 'load':
        load_resources(args.games, args.items, args.reset)

    elif args.command == 'generate':
        # If the Assets are not loaded yet, exit
        if not os.path.isfile('assets.json'):
            print(f"Item Assets not loaded yet! Run: python main.py load <game selection>\n"
                  f" - Borderlands 1:   bl1\n"
                  f" - Borderlands 2:   bl2\n"
                  f" - Borderlands 3:   bl3\n"
                  f" - Borderlands TPS: bl-tps\n"
                  f" - Wonderlands:     bl-wl\n")
            exit(0)

        if args.use_abnb:
            from AdvancedBnB import Gun, Shield
        else:
            from StandardBnB import Gun, Shield

        # Load item_config.yaml file
        props = load_item_config()

        if args.item_type == 'gun':
            new_gun = Gun()
            new_gun.generate(props=props)
            print(new_gun)
            new_gun.generate_card()

        elif args.item_type == 'shield':
            new_shield = Shield()
            new_shield.generate(props=props)
            print(new_shield)
            new_shield.generate_card()

        elif args.item_type == 'health_potion':
            new_potion = HealthPotion(props=props)
            new_potion.generate_card()

        elif args.item_type == 'shield_potion':
            new_potion = ShieldPotion(props=props)
            new_potion.generate_card()
