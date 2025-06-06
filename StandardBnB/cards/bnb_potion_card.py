import os
from PIL import Image, ImageFile, ImageDraw, ImageFont

from util.cards.card_generation import Field, draw_image_to_field, draw_text_to_field, draw_text_to_modfield, draw_field_locations

potion_card_template = {
    'fld_name': Field(0.498, 0.095, 0.38, 0.10, False),
    'fld_img': Field(0.5, 0.45, 0.85, 0.45, False),
    'fld_red_txt': Field(0.66, 0.68, 0.45, 0.08, False),

    'fld_rarity_txt': Field(0.14, 0.18, 0.15, 0.018, False),
    'fld_guild_logo': Field(0.14, 0.145, 0.15, 0.038, False),
    'fld_type_txt': Field(0.855, 0.18, 0.15, 0.018, False),
    'fld_type_icon': Field(0.855, 0.145, 0.15, 0.038, False),

    'fld_dice_img': Field(0.25, 0.45, 0.20, 0.24, False),

    'fld_element': Field(0.115, 0.85, 0.11, 0.11, False),

    'fld_mod_txt': Field(0.56, 0.82, 0.74, 0.09, False)
}

def generate_potion_card(potion_obj):
    # Take card template (blank card) based on rarity
    path = f"./img/blank_cards/shield_card_blank_{potion_obj.rarity.lower()}.webp"
    assert os.path.isfile(path), f"ERROR - Path to blank gun card file is not correct: <{path}>"

    card_img = Image.open(path)
    #card_img = draw_field_locations(card_img, potion_card_template)

    # Add potion name
    card_field = potion_card_template['fld_name']
    card_img = draw_text_to_field(card_img, card_field,f"{potion_obj.rarity} Health Potion",'rexlia rg.otf')

    # Add Potion Image
    card_field = potion_card_template['fld_img']
    img_to_insert = Image.open(potion_obj.asset['path_to_img'])
    card_img = draw_image_to_field(card_img, img_to_insert, card_field)

    # Effect Text
    card_field = potion_card_template['fld_mod_txt']
    mod_text = f"Recovers {potion_obj.dice}{ '+' + str(potion_obj.bonus) if potion_obj.bonus != 0 else ''} Health (up to Maximum Health)"
    card_img = draw_text_to_field(card_img, card_field, mod_text, 'avenir-next-condensed-medium.otf')

    # Add Rarity and Item Type
    card_field = potion_card_template['fld_rarity_txt']
    card_img = draw_text_to_field(card_img, card_field, potion_obj.rarity.upper(), 'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf')

    card_field = potion_card_template['fld_type_txt']
    card_img = draw_text_to_field(card_img, card_field, 'POTION', 'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf')

    card_field = potion_card_template['fld_type_icon']
    symbol = Image.open(f"img/gun_symbol/potion.png")
    card_img = draw_image_to_field(card_img, symbol, card_field)

    card_img.show()

    card_img.save('test.bmp', 'BMP', quality=100)
