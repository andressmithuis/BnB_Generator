import os

import numpy as np
from PIL import Image, ImageOps

from util.cards.card_generation import Field, draw_image_to_field, draw_text_to_field, draw_field_locations

gun_card_front_template = {
    'fld_name': Field(0.498, 0.095, 0.38, 0.10, False),
    'fld_gun_img': Field(0.66, 0.45, 0.45, 0.38, False),
    'fld_red_txt': Field(0.66, 0.68, 0.45, 0.08, False),

    'fld_rarity_txt': Field(0.14, 0.18, 0.15, 0.018, False),
    'fld_guild_logo': Field(0.14, 0.145, 0.15, 0.038, False),
    'fld_guntype_txt': Field(0.855, 0.18, 0.15, 0.018, False),
    'fld_guntype_logo': Field(0.855, 0.145, 0.15, 0.038, False),

    'fld_ammo_logo': Field(0.425, 0.72, 0.05, 0, True),
    'fld_ammo_cnt': Field(0.47, 0.74, 0.025, 0, True),

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

    'fld_quickref_name': Field(0.28, 0.78, 0.20, 0.035, False),
    'fld_quickref_effect': Field(0.64, 0.78, 0.50, 0.035, False),
}

gun_card_back_template = {
    'fld_name': Field(0.498, 0.095, 0.38, 0.10, False),

    'fld_rarity_txt': Field(0.14, 0.18, 0.15, 0.018, False),
    'fld_guild_logo': Field(0.14, 0.145, 0.15, 0.038, False),
    'fld_guntype_txt': Field(0.855, 0.18, 0.15, 0.018, False),
    'fld_guntype_logo': Field(0.855, 0.145, 0.15, 0.038, False),

    'fld_type_bonus_txt': Field(0.28, 0.72, 0.2, 0.05, False),
    'fld_type_bonus_effect': Field(0.535, 0.82, 0.71, 0.14, False),

    'fld_part_name': [],
    'fld_part_effect': [],

    'fld_mod_effects': []
}

gun_card_front_template['fld_quickref_name'] = []
gun_card_front_template['fld_quickref_effect'] = []
for i in range(6):
    gun_card_front_template['fld_quickref_name'].append(Field(0.28, 0.78 + i * 0.03, 0.20, 0.031, False))
    gun_card_front_template['fld_quickref_effect'].append(Field(0.64, 0.78 + i * 0.03, 0.50, 0.031, False))

gun_card_back_template['fld_part_name'] = []
gun_card_back_template['fld_part_effect'] = []
for i in range(14):
    gun_card_back_template['fld_part_name'].append(Field(0.17, 0.25 + i * 0.033, 0.18, 0.030, False))
    gun_card_back_template['fld_part_effect'].append(Field(0.41, 0.25 + i * 0.033, 0.3, 0.030, False))
    gun_card_back_template['fld_mod_effects'].append(Field(0.82, 0.25 + i * 0.033, 0.18, 0.030, False))

def generate_gun_card(gun_obj):
    # Take gun card template (blank card) based on rarity
    str = f"{gun_obj.rarity}".lower()
    path = f"./img/blank_cards/card_blank_{str}.webp"
    assert os.path.isfile(path), f"ERROR - Path to blank gun card file is not correct: <{path}>"
    card_front = Image.open(path)

    path = f"./img/blank_cards/shield_card_blank_{str}.webp"
    assert os.path.isfile(path), f"ERROR - Path to blank gun card file is not correct: <{path}>"
    card_back = Image.open(path)

    if False:
        card_front = draw_field_locations(card_front, gun_card_front_template)
        card_back = draw_field_locations(card_back, gun_card_back_template)

    # Add Gun Image
    card_field = gun_card_front_template['fld_gun_img']
    img_to_insert = Image.open(gun_obj.asset['path_to_img'])
    card_front = draw_image_to_field(card_front, img_to_insert, card_field)

    # Add Manufacturer logo
    card_field = gun_card_front_template['fld_guild_logo']
    symbol = Image.open(f"img/guild_logo/AdvancedBnB/{gun_obj.manufacturer.logo_file}")
    card_front = draw_image_to_field(card_front, symbol, card_field)
    card_back = draw_image_to_field(card_back, symbol, card_field)

    # Add Gun type symbol
    card_field = gun_card_front_template['fld_guntype_logo']
    symbol = Image.open(f"img/gun_symbol/{gun_obj.gun_type.asset_dir}.png")
    card_front = draw_image_to_field(card_front, symbol, card_field)
    card_back = draw_image_to_field(card_back, symbol, card_field)

    # Add Damage Dice symbol
    card_field = gun_card_front_template['fld_dmg_dice']
    symbol = Image.open(f"img/dice_symbol/1d{gun_obj.hit_dice.sides}.png")
    card_front = draw_image_to_field(card_front, symbol, card_field)

    # Add Ammo counter
    card_field = gun_card_front_template['fld_ammo_logo']
    symbol = Image.open(f"img/gun_symbol/ammo.png")
    for i in range(gun_obj.mag_size):
        if i > 0:
            card_field.x += 0.05
        card_front = draw_image_to_field(card_front, symbol, card_field)

    # Add Element symbols
    if gun_obj.forced_elemental or not gun_obj.forced_non_elemental:
        card_field = gun_card_front_template['fld_element']

        n_symbols = len(gun_obj.elements)

        for i in range(n_symbols):
            _w = card_field.w / n_symbols
            _h = card_field.h
            _x = card_field.x
            if n_symbols == 2:
                _x = card_field.x + (i * _w) - (_w / 2)
            _y = card_field.y
            subfield = Field(_x, _y, _w, _h, True)

            el = gun_obj.elements[i]
            if el.is_fusion:
                symbols = []
                for sub_el in el.fusion_elements:
                    filename = sub_el.name.lower()
                    symbols.append(Image.open(f"img/element_symbol/{filename}.png"))

                # Resize both images to biggest of the 2
                # Take half of bot and stitch together
                w1, h1 = symbols[0].size
                w2, h2 = symbols[1].size

                a1 = w1 * h1
                a2 = w2 * h2

                if a1 > a2:
                    symbols[2] = ImageOps.contain(symbols[2], (w1, h1), method=Image.Resampling.LANCZOS)
                else:
                    symbols[1] = ImageOps.contain(symbols[1], (w1, h1), method=Image.Resampling.LANCZOS)

                mask_array = np.zeros((h1, w1), dtype=np.uint8)
                for y in range(h1):
                    for x in range(w1):
                        if x + y < w1:
                            mask_array[y, x] = 255

                mask = Image.fromarray(mask_array, mode='L')

                symbol = Image.composite(symbols[0], symbols[1], mask)

                #symbol = Image.new("RGBA", (w1, h1))
                #symbol.paste(symbols[0], (0, 0))
                #symbol.paste(symbols[1].crop((w1 // 2, 0, w1, h1)), (w1 // 2, 0))

            else:
                filename = el.name.lower()
                symbol = Image.open(f"img/element_symbol/{filename}.png")

            card_front = draw_image_to_field(card_front, symbol, subfield)

            # Element bonus
            if el.bonus != 0:
                subfield.h = subfield.h / 4
                subfield.y += subfield.h * 0.75
                subfield.x += subfield.w * 0.25

                card_front = draw_text_to_field(card_front, subfield, f"+{el.bonus}", 'rexlia rg.otf', font_size=25)

    # Add gun name
    card_field = gun_card_front_template['fld_name']
    card_front = draw_text_to_field(card_front, card_field, f"{gun_obj.name_prefix + ' ' if gun_obj.name_prefix != '' else ''}{gun_obj.name}", 'rexlia rg.otf')
    card_back = draw_text_to_field(card_back, card_field,f"{gun_obj.name_prefix + ' ' if gun_obj.name_prefix != '' else ''}{gun_obj.name}",'rexlia rg.otf')

    # Add Rarity and Gun Type
    card_field = gun_card_front_template['fld_rarity_txt']
    card_front = draw_text_to_field(card_front, card_field, f"{gun_obj.rarity}".upper(), 'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf')
    card_back = draw_text_to_field(card_back, card_field, f"{gun_obj.rarity}".upper(),'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf')

    card_field = gun_card_front_template['fld_guntype_txt']
    card_front = draw_text_to_field(card_front, card_field, f"{gun_obj.gun_type}".upper(),'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf')
    card_back = draw_text_to_field(card_back, card_field, f"{gun_obj.gun_type}".upper(),'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf')

    # Add Hits/Crits/Range
    card_field = gun_card_front_template['fld_acctop_h']
    card_front = draw_text_to_field(card_front, card_field, f"{gun_obj.hits_crits['glance']['hits']}",'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf', color=(255, 255, 255))

    card_field = gun_card_front_template['fld_acctop_c']
    card_front = draw_text_to_field(card_front, card_field, f"{gun_obj.hits_crits['glance']['crits']}", 'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf', color=(255, 255, 255))

    card_field = gun_card_front_template['fld_accmid_h']
    card_front = draw_text_to_field(card_front, card_field, f"{gun_obj.hits_crits['solid']['hits']}", 'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf', color=(255, 255, 255))

    card_field = gun_card_front_template['fld_accmid_c']
    card_front = draw_text_to_field(card_front, card_field, f"{gun_obj.hits_crits['solid']['crits']}", 'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf', color=(255, 255, 255))

    card_field = gun_card_front_template['fld_accbot_h']
    card_front = draw_text_to_field(card_front, card_field, f"{gun_obj.hits_crits['penetrate']['hits']}", 'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf', color=(255, 255, 255))

    card_field = gun_card_front_template['fld_accbot_c']
    card_front = draw_text_to_field(card_front, card_field, f"{gun_obj.hits_crits['penetrate']['crits']}", 'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf', color=(255, 255, 255))

    card_field = gun_card_front_template['fld_range']
    card_front = draw_text_to_field(card_front, card_field, f"{gun_obj.range}", 'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf')

    # Add Number of Damage Dice (if applicable)
    if gun_obj.hit_dice.count > 1:
        card_field = gun_card_front_template['fld_dmg_dice_n']
        card_front = draw_text_to_field(card_front, card_field, f"x{gun_obj.hit_dice.count}",'rexlia rg.otf', color=(255, 255, 255))

    # Collect Situational Traits, Parts and Bonuses
    quick_ref = []
    for trait in gun_obj.traits:
        if trait.situational:
            quick_ref.append(trait)

    for part in gun_obj.parts:
        if part.situational:
            quick_ref.append(part)

    for bonus in gun_obj.gun_type.weapon_bonus:
        if bonus.situational:
            quick_ref.append(bonus)

    # Quick Reference
    idx = 0
    for i in range(len(quick_ref)):
        ref = quick_ref[i]
        name_field = gun_card_front_template['fld_quickref_name'][idx]
        card_front = draw_text_to_field(card_front, name_field, f"{ref.name}:",'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf', align='left', font_size=25)

        ef_text = split_text_on_length(f"{ref.to_text(gun_obj)}", 70)
        for line in ef_text:
            effect_field = gun_card_front_template['fld_quickref_effect'][idx]
            card_front = draw_text_to_field(card_front, effect_field, line, 'avenir-next-condensed-medium.otf', align='left', font_size=25)
            idx += 1

    # Gun Parts & Gun Traits - Collecting column contents
    header_col = []
    effect_col = []
    header_idx = [0]

    header_col.append(f"--Gun Parts--")
    effect_col.append('')

    for i in range(len(gun_obj.parts)):
        part = gun_obj.parts[i]
        header_col.append(f"{part.name}:")

        ef_str = split_text_on_length(f"{part.effect}", 65)
        for ef in ef_str:
            effect_col.append(ef)

        while len(header_col) < len(effect_col):
            header_col.append('')

    effect_col.append('')
    header_col.append('')
    
    # Gun Traits
    header_idx.append(len(header_col))
    header_col.append(f"--Gun Traits--")
    effect_col.append('')

    for i in range(len(gun_obj.traits)):
        part = gun_obj.traits[i]
        header_col.append(f"{part.name}:")

        ef_str = split_text_on_length(f"{part.effect}", 65)
        for ef in ef_str:
            effect_col.append(ef)

        while len(header_col) < len(effect_col):
            header_col.append('')

    # Printing column content to card
    fonts = {
        'header': 'rexlia rg.otf',
        'name': 'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf',
        'effect': 'avenir-next-condensed-medium.otf'
    }

    for i in range(len(header_col)):
        _offset = 0.462 / max([len(header_col), 12])
        name_field = Field(0.17, 0.25 + i * _offset, 0.18, 0.030, False)
        effect_field = Field(0.41, 0.25 + i * _offset, 0.3, 0.030, False)

        font = fonts['name']
        if i in header_idx:
            font = fonts['header']

        card_back = draw_text_to_field(card_back, name_field, header_col[i],font, align='left', font_size=22)
        card_back = draw_text_to_field(card_back, effect_field, effect_col[i], fonts['effect'], align='left',font_size=22)


    # Mods & Checks
    card_field = gun_card_back_template['fld_mod_effects'][0]
    card_back = draw_text_to_field(card_back, card_field, f"--Mods & Checks--", 'rexlia rg.otf', align='left', font_size=22)

    mods = gun_obj.mod_stats['mods']
    idx = 0
    for k, v in mods.items():
        if v != 0:
            w_parts = k.split('_')
            for i in range(len(w_parts)):
                w = w_parts[i]
                w = f"{w[0].upper()}{w[1:]}"

                if w in ['Dmg', 'Ads', 'Acc', 'Mod']:
                    w = w.upper()

                w_parts[i] = w
            k = ' '.join(w_parts)
            card_field = gun_card_back_template['fld_mod_effects'][1 + idx]
            card_back = draw_text_to_field(card_back, card_field, f"{k} {'+' if v > 0 else ''}{v}",'avenir-next-condensed-medium.otf', align='left', font_size=22)

            idx += 1


    # Gun Type Bonus
    card_field = gun_card_back_template['fld_type_bonus_txt']
    card_back = draw_text_to_field(card_back, card_field, f"--{gun_obj.gun_type.weapon_bonus[0].name}--", 'rexlia rg.otf', align='left', font_size=28)

    card_field = gun_card_back_template['fld_type_bonus_effect']

    bonus_txt = ' <nl> '.join([b.to_text(gun_obj) for b in gun_obj.gun_type.weapon_bonus])
    lines = split_text_on_length(bonus_txt, 75)
    while len(lines) < 4:
        lines.append('')
    str_out = '\n'.join(lines)
    card_back = draw_text_to_field(card_back, card_field, f"{str_out}", 'avenir-next-condensed-medium.otf', align='left', font_size=28)


    # Merge front and back of card
    if True:
        w1, h1 = card_front.size
        w2, h2 = card_back.size

        new_w = w1 + w2
        new_h = max(h1, h2)

        card_joined = Image.new("RGB", (new_w, new_h))
        card_joined.paste(card_front, (0, 0))
        card_joined.paste(card_back, (w1, 0))

    card_joined.show()

    card_joined.save('test.bmp', 'BMP', quality=100)

def split_text_on_length(text: str, length:int):
    ret = ['']

    words = text.split(' ')
    for w in words:
        if w == '<nl>':
            ret.append('')
            continue

        if ret[-1] == '':
            ret[-1] = w
        elif len(ret[-1]) + len(w) >= length:
            ret.append(w)
        else:
            ret[-1] += f" {w}"

    return ret

