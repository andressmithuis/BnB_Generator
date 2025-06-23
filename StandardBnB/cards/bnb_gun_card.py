import os
from PIL import Image

from util.cards.card_generation import Field, draw_image_to_field, draw_text_to_field, draw_field_locations, split_text_on_length

gun_card_template = {
    'fld_name': Field(0.498, 0.095, 0.38, 0.10, False),
    'fld_gun_img': Field(0.66, 0.45, 0.45, 0.38, False),
    'fld_red_txt': Field(0.66, 0.68, 0.45, 0.08, False),

    'fld_rarity_txt': Field(0.14, 0.18, 0.15, 0.018, False),
    'fld_guild_logo': Field(0.14, 0.145, 0.15, 0.038, False),
    'fld_guntype_txt': Field(0.855, 0.18, 0.15, 0.018, False),
    'fld_guntype_logo': Field(0.855, 0.145, 0.15, 0.038, False),

    'fld_acctop_h': Field(0.311, 0.344, 0.02, 0, True),
    'fld_acctop_c': Field(0.3578, 0.344, 0.02, 0, True),
    'fld_accmid_h': Field(0.311, 0.41, 0.02, 0, True),
    'fld_accmid_c': Field(0.3578, 0.41, 0.02, 0, True),
    'fld_accbot_h': Field(0.311, 0.477, 0.02, 0, True),
    'fld_accbot_c': Field(0.3578, 0.477, 0.02, 0, True),

    'fld_dmg_dice': Field(0.135, 0.63, 0.07, 0, True),
    'fld_dmg_dice_n': Field(0.17, 0.68, 0.02, 0, True),
    'fld_range': Field(0.255, 0.724, 0.02, 0, True),

    'fld_element': Field(0.115, 0.85, 0.11, 0.11, False),

    'fld_ef_name': Field(0.56, 0.82, 0.74, 0.09, False),
    'fld_ef_text': Field(0.56, 0.82, 0.74, 0.09, False)
}

def generate_gun_card(gun_obj):
    # Take gun card template (blank card) based on rarity
    path = f"./img/blank_cards/card_blank_{gun_obj.rarity.lower()}.webp"
    assert os.path.isfile(path), f"ERROR - Path to blank gun card file is not correct: <{path}>"

    card_img = Image.open(path)

    if False:
        card_img = draw_field_locations(card_img, gun_card_template)

    # Add Gun Image
    card_field = gun_card_template['fld_gun_img']
    img_to_insert = Image.open(gun_obj.asset['path_to_img'])
    card_img = draw_image_to_field(card_img, img_to_insert, card_field)

    # Add Manufacturer logo
    card_field = gun_card_template['fld_guild_logo']
    symbol = Image.open(f"img/guild_logo/StandardBnB/{gun_obj.guild.logo_file}")
    card_img = draw_image_to_field(card_img, symbol, card_field)

    # Add Gun type symbol
    card_field = gun_card_template['fld_guntype_logo']
    symbol = Image.open(f"img/gun_symbol/{gun_obj.type.img_file}")
    card_img = draw_image_to_field(card_img, symbol, card_field)

    # Add Damage Dice symbol
    card_field = gun_card_template['fld_dmg_dice']
    symbol = Image.open(f"img/dice_symbol/1d{gun_obj.hit_dice.sides}.png")
    card_img = draw_image_to_field(card_img, symbol, card_field)

    # Add Element symbols
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
    card_field = gun_card_template['fld_name']
    gun_name = f"{gun_obj.name}"
    if gun_obj.name_prefix is not None:
        gun_name = f"{gun_obj.name_prefix.name} {gun_obj.name}"
    card_img = draw_text_to_field(card_img, card_field, gun_name, 'rexlia rg.otf')

    # Add Rarity and Gun Type
    card_field = gun_card_template['fld_rarity_txt']
    card_img = draw_text_to_field(card_img, card_field, gun_obj.rarity.upper(), 'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf')

    card_field = gun_card_template['fld_guntype_txt']
    card_img = draw_text_to_field(card_img, card_field, gun_obj.type.name.upper(),'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf')

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

    # Modifier Texts
    ef_name = []
    ef_text = []

    # Gun Effects
    for ef in gun_obj.effects:
        ef_name.append(f"{ef.name}:")
        ef_lines = split_text_on_length(f"{ef.to_text(gun_obj)}", 65)
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
                ef_lines = split_text_on_length(f"{'+' if v > 0 else ''}{v}", 70)
                for line in ef_lines:
                    ef_text.append(line)

                while len(ef_name) < len(ef_text):
                    ef_name.append('')


    # Prepare Text Rows
    gun_card_template['fld_ef_name'] = []
    gun_card_template['fld_ef_text'] = []
    for i in range(max([len(ef_name), 6])):
        gun_card_template['fld_ef_name'].append(Field(0.28, 0.78 + i * 0.03, 0.20, 0.031, False))
        gun_card_template['fld_ef_text'].append(Field(0.64, 0.78 + i * 0.03, 0.50, 0.031, False))

    # Print Effects, Mods & Checks to the Card
    for i in range(len(ef_name)):
        name_field = gun_card_template['fld_ef_name'][i]
        text_field = gun_card_template['fld_ef_text'][i]

        card_img = draw_text_to_field(card_img, name_field, ef_name[i],'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf', align='left', font_size=25)
        card_img = draw_text_to_field(card_img, text_field, ef_text[i], 'avenir-next-condensed-medium.otf', align='left',font_size=25)

    #card_img.show()



    card_img.save('test.bmp', 'BMP', quality=100)
    card_img.save(os.path.join('app/static/generated', 'new_gun.bmp'), 'BMP', quality=100)
