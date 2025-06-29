import os
from PIL import Image, ImageFile, ImageDraw, ImageFont

from util.cards.card_generation import Field, draw_image_to_field, draw_text_to_field, draw_text_to_modfield, draw_field_locations
from util.cards.card_basics import *

potion_card_template = {
    'fld_red_txt': Field(0.66, 0.68, 0.45, 0.08, False),

    'fld_dice_img': Field(0.215, 0.50, 0.12, 0.18, True),
    'fld_dice_cnt': Field(0.13, 0.50, 0.10, 0.10, True),
    'fld_dice_bonus': Field(0.33, 0.50, 0.10, 0.10, True),
}

def generate_potion_card(potion_obj):
    # Take card template (blank card) based on rarity
    path = f"./img/blank_cards/shield_card_blank_{potion_obj.rarity.lower()}.webp"
    assert os.path.isfile(path), f"ERROR - Path to blank gun card file is not correct: <{path}>"

    card_img = Image.open(path)

    if False:
        card_img = draw_field_locations(card_img, basic_card_template)
        card_img = draw_field_locations(card_img, potion_card_template)

    # Add potion name
    item_name = f"{potion_obj.rarity} Health Potion"
    card_img = card_add_item_name(card_img, item_name)

    # Add Potion Image
    img_to_insert = Image.open(potion_obj.asset['path_to_img'])
    card_img = card_add_item_image(card_img, img_to_insert)

    # Add Potion type symbol
    symbol = Image.open(f"img/gun_symbol/potion.png")
    card_img = card_add_tr_logo(card_img, symbol)

    # Add Dice Symbol
    card_field = potion_card_template['fld_dice_img']
    symbol = Image.open(f"img/dice_symbol/1d{potion_obj.dice.sides}.png")
    card_img = draw_image_to_field(card_img, symbol, card_field)

    # Add Dice Texts
    card_field = potion_card_template['fld_dice_cnt']
    card_img = draw_text_to_field(card_img, card_field, f"{potion_obj.dice.count}", 'rexlia rg.otf', color=(255, 255, 255), font_size=60)

    if potion_obj.bonus != 0:
        card_field = potion_card_template['fld_dice_bonus']
        card_img = draw_text_to_field(card_img, card_field, f"+{potion_obj.bonus}", 'rexlia rg.otf', color=(255, 255, 255), font_size=60)

    # Add Rarity and Item Type
    item_rarity = f"{potion_obj.rarity}".upper()
    card_img = card_add_tl_text(card_img, item_rarity)

    card_img = card_add_tr_text(card_img, "POTION")

    # Card Output
    card_img.show()
    card_img.save('test.bmp', 'BMP', quality=100)
