import os
from copy import deepcopy

import numpy as np
from PIL import Image, ImageOps

from util.cards.card_basics import *
from util.cards.card_generation import *
from util import Rarity

shield_card_front_template = {
    'fld_red_txt': Field(0.66, 0.68, 0.45, 0.08, False),

    'fld_cap_icon': Field(0.18, 0.40, 0.12, 0.12, True),
    'fld_rr_icon': Field(0.18, 0.58, 0.12, 0.12, True),

    'fld_cap_val': Field(0.30, 0.40, 0.12, 0.12, True),
    'fld_rr_val': Field(0.30, 0.58, 0.12, 0.12, True),
}

shield_card_back_template = {
    'fld_type_bonus_txt': Field(0.28, 0.72, 0.2, 0.05, False),
    'fld_type_bonus_effect': Field(0.535, 0.82, 0.71, 0.14, False),

    'fld_part_name': Field(0.17, 0.25, 0.18, 0.030, False),
    'fld_part_effect': Field(0.41, 0.25, 0.3, 0.030, False),

    'fld_mod_effects': []
}

for i in range(14):
    shield_card_back_template['fld_mod_effects'].append(Field(0.82, 0.25 + i * 0.033, 0.18, 0.030, False))

def generate_shield_card(shield_obj):
    # Take shield card template (blank card) based on rarity
    str = f"{shield_obj.rarity}".lower()
    path = f"./img/blank_cards/shield_card_blank_{str}.webp"
    assert os.path.isfile(path), f"ERROR - Path to blank gun card file is not correct: <{path}>"
    card_front = Image.open(path)

    path = f"./img/blank_cards/empty_card_blank_{str}.webp"
    assert os.path.isfile(path), f"ERROR - Path to blank gun card file is not correct: <{path}>"
    card_back = Image.open(path)

    if False:
        card_front = draw_field_locations(card_front, basic_card_template)
        card_front = draw_field_locations(card_front, shield_card_front_template)
        card_back = draw_field_locations(card_back, shield_card_back_template)

    # Add Shield Image
    img_to_insert = Image.open(shield_obj.asset['path_to_img'])
    card_front = card_add_item_image(card_front, img_to_insert)

    # Add Manufacturer logo
    symbol = Image.open(f"img/guild_logo/AdvancedBnB/{shield_obj.manufacturer.logo_file}")
    card_front = card_add_tl_logo(card_front, symbol)
    card_back = card_add_tl_logo(card_back, symbol)

    # Add Shield type symbol
    symbol = Image.open(f"img/gun_symbol/shield.png")
    card_front = card_add_tr_logo(card_front, symbol)
    card_back = card_add_tr_logo(card_back, symbol)

    # Add Element symbols
    card_front = card_add_element(card_front, shield_obj)

    # Add shield name
    item_name = f"{shield_obj.name_prefix + ' ' if shield_obj.name_prefix != '' else ''}{shield_obj.name}"
    card_front = card_add_item_name(card_front, item_name)
    card_back = card_add_item_name(card_back, item_name)

    # Add Rarity and Shield Type
    item_rarity = f"{shield_obj.rarity}".upper()
    card_front = card_add_tl_text(card_front, item_rarity)
    card_back = card_add_tl_text(card_back, item_rarity)

    item_type = f"{shield_obj.shield_type}".upper()
    card_front = card_add_tr_text(card_front, item_type)
    card_back = card_add_tr_text(card_back, item_type)

    # Capacity and Recharge Rate
    # Icons
    colors = {
        Rarity.COMMON: (191, 191, 191),
        Rarity.UNCOMMON: (0, 102, 0),
        Rarity.RARE: (0, 0, 179),
        Rarity.EPIC: (128, 0, 128),
        Rarity.LEGENDARY: (204, 122, 0),
        Rarity.PEARLESCENT: (0, 153, 153),
    }
    card_field = shield_card_front_template['fld_cap_icon']
    icon = Image.open(f"img/item_icons/shield_capacity.png")
    icon = recolor_image(icon, colors[shield_obj.rarity])
    card_front = draw_image_to_field(card_front, icon, card_field)

    card_field = shield_card_front_template['fld_rr_icon']
    icon = Image.open(f"img/item_icons/shield_rechargerate.png")
    icon = recolor_image(icon, colors[shield_obj.rarity])
    card_front = draw_image_to_field(card_front, icon, card_field)

    # Value
    card_field = shield_card_front_template['fld_cap_val']
    card_front = draw_text_to_field(card_front, card_field, f"{shield_obj.capacity}", 'rexlia rg.otf', color=(11, 121, 189),
                                  font_size=50)

    card_field = shield_card_front_template['fld_rr_val']
    card_front = draw_text_to_field(card_front, card_field, f"{shield_obj.recharge_rate}", 'rexlia rg.otf',
                                  color=(11, 121, 189), font_size=50)

    # Quick Reference
    quick_ref = []
    for part in shield_obj.parts:
        if part.situational:
            if part.name not in [x.name for x in quick_ref]:
                quick_ref.append(part)

    card_front = card_add_quick_ref(card_front, quick_ref, shield_obj)

    # Shield Parts / Tag
    # Collect part count / deduplication of parts
    dedup_list = []
    for part in shield_obj.parts:
        part_added = False
        for dedup_part in dedup_list:
            if part.name == dedup_part['part'].name:
                dedup_part['count'] += 1
                part_added = True
                break

        if not part_added:
            dedup_list.append({'part': part, 'count': 1})

    # Collecting column content
    header_col = []
    effect_col = []
    header_idx = [0]

    header_col.append(f"--Shield Parts--")
    effect_col.append('')

    for i in range(len(dedup_list)):
        part = dedup_list[i]['part']
        new_header = f"{part.name}"
        if dedup_list[i]['count'] > 1:
            new_header += f" x{dedup_list[i]['count']}"
        new_header += ':'

        header_col.append(new_header)

        ef_str = split_text_on_length(f"{part.to_text(shield_obj)}", 65)
        for ef in ef_str:
            effect_col.append(ef)

        while len(header_col) < len(effect_col):
            header_col.append('')

    header_col.append('')
    effect_col.append('')

    header_idx.append(len(header_col))
    header_col.append(f"--Shield Tag--")
    effect_col.append('')
    header_col.append(f"{shield_obj.tag.name}:")
    effect_col.append(f"{shield_obj.tag.effect}")

    # Printing column content to card
    fonts = {
        'header': 'rexlia rg.otf',
        'name': 'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf',
        'effect': 'avenir-next-condensed-medium.otf'
    }

    for i in range(len(header_col)):
        y_offset = 0.462 / max([len(header_col), 12])
        name_field = deepcopy(shield_card_back_template['fld_part_name'])
        effect_field = deepcopy(shield_card_back_template['fld_part_effect'])
        name_field.y += i * y_offset
        effect_field.y += i * y_offset

        font = fonts['name']
        if i in header_idx:
            font = fonts['header']

        card_back = draw_text_to_field(card_back, name_field, header_col[i],font, align='left', font_size=22)
        card_back = draw_text_to_field(card_back, effect_field, effect_col[i], fonts['effect'], align='left',font_size=22)


    # Mods & Checks
    card_field = shield_card_back_template['fld_mod_effects'][0]
    card_back = draw_text_to_field(card_back, card_field, f"--Mods & Checks--", 'rexlia rg.otf', align='left', font_size=22)

    if 'mods' in shield_obj.mod_stats:
        mods = shield_obj.mod_stats['mods']
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
                card_field = shield_card_back_template['fld_mod_effects'][1 + idx]
                card_back = draw_text_to_field(card_back, card_field, f"{k} {'+' if v > 0 else ''}{v}",'avenir-next-condensed-medium.otf', align='left', font_size=22)

                idx += 1

    # Merge front and back of card
    card_joined = card_merge_sideways(card_front, card_back)
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

