import os
from PIL import Image

from util.cards.card_generation import Field, draw_image_to_field, draw_text_to_field, draw_field_locations, split_text_on_length
from util.cards.card_basics import *

gun_card_template = {
    'fld_red_txt': Field(0.66, 0.68, 0.45, 0.08, False),

    'fld_acctop_h': Field(0.311, 0.344, 0.02, 0, True),
    'fld_acctop_c': Field(0.3578, 0.344, 0.02, 0, True),
    'fld_accmid_h': Field(0.311, 0.41, 0.02, 0, True),
    'fld_accmid_c': Field(0.3578, 0.41, 0.02, 0, True),
    'fld_accbot_h': Field(0.311, 0.477, 0.02, 0, True),
    'fld_accbot_c': Field(0.3578, 0.477, 0.02, 0, True),

    'fld_dmg_dice': Field(0.135, 0.63, 0.07, 0, True),
    'fld_dmg_dice_n': Field(0.17, 0.68, 0.02, 0, True),
    'fld_range': Field(0.255, 0.724, 0.02, 0, True),
}

def generate_gun_card(gun_obj):
    # Take gun card template (blank card) based on rarity
    path = f"./img/blank_cards/card_blank_{gun_obj.rarity.lower()}.webp"
    assert os.path.isfile(path), f"ERROR - Path to blank gun card file is not correct: <{path}>"

    card_img = Image.open(path)

    if False:
        card_img = draw_field_locations(card_img, basic_card_template)
        card_img = draw_field_locations(card_img, gun_card_template)

    # Add Gun Image
    img_to_insert = Image.open(gun_obj.asset['path_to_img'])
    card_img = card_add_item_image(card_img, img_to_insert)

    # Add Manufacturer logo
    symbol = Image.open(f"img/guild_logo/StandardBnB/{gun_obj.guild.logo_file}")
    card_img = card_add_tl_logo(card_img, symbol)

    # Add Gun type symbol
    symbol = Image.open(f"img/gun_symbol/{gun_obj.type.img_file}")
    card_img = card_add_tr_logo(card_img, symbol)

    # Add Damage Dice symbol
    card_field = gun_card_template['fld_dmg_dice']
    symbol = Image.open(f"img/dice_symbol/1d{gun_obj.hit_dice.sides}.png")
    card_img = draw_image_to_field(card_img, symbol, card_field)

    # Add Element symbols
    card_img = card_add_element(card_img, gun_obj)

    if False:
        card_field = gun_card_template['fld_element']
        gun_elements = list(set(gun_obj.elements))[:6]
        el_symbols = [gun_elements]
        if len(gun_elements) > 3:
            split_idx = len(gun_elements) - int(len(gun_elements) / 2)
            el_symbols = [gun_elements[:split_idx], gun_elements[split_idx:]]

        for row in range(len(el_symbols)):
            for j in range(len(el_symbols[row])):
                _w = card_field.w / len(el_symbols[row])
                _h = card_field.h / len(el_symbols)
                _x = card_field.x - (card_field.w / 2) + (_w / 2) + (j * _w)
                _y = card_field.y - (card_field.h / 2) + (_h / 2) + (row * _h)
                subfield = Field(_x, _y, _w, _h, True)

                symbol = Image.open(f"img/element_symbol/{el_symbols[row][j].name}.png")
                card_img = draw_image_to_field(card_img, symbol, subfield)

    # Add gun name
    item_name = f"{gun_obj.name_prefix + ' ' if gun_obj.name_prefix != None else ''}{gun_obj.name}"
    card_img = card_add_item_name(card_img, item_name)

    # Add Rarity and Gun Type
    item_rarity = f"{gun_obj.rarity}".upper()
    card_img = card_add_tl_text(card_img, item_rarity)

    item_type = f"{gun_obj.type}".upper()
    card_img = card_add_tr_text(card_img, item_type)

    # Add Hits/Crits/Range
    card_field = gun_card_template['fld_acctop_h']
    card_img = draw_text_to_field(card_img, card_field, str(gun_obj.hits_crits['2-7']['hits']),'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf', color=(255, 255, 255))

    card_field = gun_card_template['fld_acctop_c']
    card_img = draw_text_to_field(card_img, card_field, str(gun_obj.hits_crits['2-7']['crits']), 'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf', color=(255, 255, 255))

    card_field = gun_card_template['fld_accmid_h']
    card_img = draw_text_to_field(card_img, card_field, str(gun_obj.hits_crits['8-15']['hits']), 'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf', color=(255, 255, 255))

    card_field = gun_card_template['fld_accmid_c']
    card_img = draw_text_to_field(card_img, card_field, str(gun_obj.hits_crits['8-15']['crits']), 'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf', color=(255, 255, 255))

    card_field = gun_card_template['fld_accbot_h']
    card_img = draw_text_to_field(card_img, card_field, str(gun_obj.hits_crits['16+']['hits']), 'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf', color=(255, 255, 255))

    card_field = gun_card_template['fld_accbot_c']
    card_img = draw_text_to_field(card_img, card_field, str(gun_obj.hits_crits['16+']['crits']), 'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf', color=(255, 255, 255))

    card_field = gun_card_template['fld_range']
    card_img = draw_text_to_field(card_img, card_field, str(gun_obj.range), 'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf')

    # Add Number of Damage Dice (if applicable)
    if gun_obj.hit_dice.count > 1:
        card_field = gun_card_template['fld_dmg_dice_n']
        card_img = draw_text_to_field(card_img, card_field, f"x{gun_obj.hit_dice.count}",'rexlia rg.otf', color=(255, 255, 255))

    # Quick reference
    # Determine Font Size
    ef_buffer = []
    for ef in gun_obj.effects:
        ef_buffer.append(f"{ef.to_text(gun_obj)}")

    if 'mods' in gun_obj.mod_stats:
        mods = gun_obj.mod_stats['mods']
        for k, v in mods.items():
            if v != 0:
                ef_buffer.append(f"{'+' if v > 0 else ''}{v}")

    font_file = card_fonts['default']
    fnt_size = get_max_font_size(card_img, ef_buffer, basic_card_template['fld_quickref_effect'], font_file)
    font = ImageFont.truetype(f"fonts/{font_file}", fnt_size)

    # Gun Effects
    ef_name = []
    ef_text = []

    for ef in gun_obj.effects:
        ef_name.append(f"{ef.name}:")
        ef_lines = wrap_text(card_img, f"{ef.to_text(gun_obj)}", font, basic_card_template['fld_quickref_effect'])
        for line in ef_lines:
            ef_text.append(line)

        while len(ef_name) < len(ef_text):
            ef_name.append('')

    # Stat Mods & Checks
    if 'mods' in gun_obj.mod_stats:
        mods = gun_obj.mod_stats['mods']
        for k, v in mods.items():
            if v != 0:
                w_parts = k.split('_')
                for i in range(len(w_parts)):
                    w = w_parts[i]
                    w = f"{w[0].upper()}{w[1:]}"

                    if w in ['Dmg', 'Ads', 'Acc', 'Mod']:
                        w = w.upper()

                    w_parts[i] = w

                ef_name.append(f"{' '.join(w_parts)}:")
                ef_lines = wrap_text(card_img,f"{'+' if v > 0 else ''}{v}", font, basic_card_template['fld_quickref_name'])
                for line in ef_lines:
                    ef_text.append(line)

                while len(ef_name) < len(ef_text):
                    ef_name.append('')

    # Print Quick Ref to Card
    y_offset = basic_card_template['fld_quickref_name'].h / max(len(ef_name), 6)
    for i in range(len(ef_name)):
        name_field = deepcopy(basic_card_template['fld_quickref_name'])
        effect_field = deepcopy(basic_card_template['fld_quickref_effect'])
        name_field.y = name_field.y - (name_field.h / 2) + (y_offset * i)
        effect_field.y = effect_field.y - (effect_field.h / 2) + (y_offset * i)

        card_img = draw_text_to_field(card_img, name_field, ef_name[i], card_fonts['bold'], align='left', font_size=fnt_size)
        card_img = draw_text_to_field(card_img, effect_field, ef_text[i], card_fonts['default'], align='left', font_size=fnt_size)

    # Card Output
    card_img.show()
    card_img.save('test.bmp', 'BMP', quality=100)
