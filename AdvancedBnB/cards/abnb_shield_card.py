import os

import numpy as np
from PIL import Image, ImageOps

from util.cards.card_generation import Field, draw_image_to_field, draw_text_to_field, draw_field_locations, recolor_image
from util import Rarity

shield_card_front_template = {
    'fld_name': Field(0.498, 0.095, 0.38, 0.10, False),
    'fld_gun_img': Field(0.66, 0.45, 0.45, 0.38, False),
    'fld_red_txt': Field(0.66, 0.68, 0.45, 0.08, False),

    'fld_rarity_txt': Field(0.14, 0.18, 0.15, 0.018, False),
    'fld_guild_logo': Field(0.14, 0.145, 0.15, 0.038, False),
    'fld_guntype_txt': Field(0.855, 0.18, 0.15, 0.018, False),
    'fld_guntype_logo': Field(0.855, 0.145, 0.15, 0.038, False),

    'fld_cap_icon': Field(0.18, 0.40, 0.12, 0.12, True),
    'fld_rr_icon': Field(0.18, 0.58, 0.12, 0.12, True),

    'fld_cap_val': Field(0.30, 0.40, 0.12, 0.12, True),
    'fld_rr_val': Field(0.30, 0.58, 0.12, 0.12, True),

    'fld_element': Field(0.115, 0.85, 0.11, 0.11, False),

    'fld_quickref_name': Field(0.28, 0.78, 0.20, 0.035, False),
    'fld_quickref_effect': Field(0.64, 0.78, 0.50, 0.035, False),
}

shield_card_back_template = {
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

shield_card_front_template['fld_quickref_name'] = []
shield_card_front_template['fld_quickref_effect'] = []
for i in range(6):
    shield_card_front_template['fld_quickref_name'].append(Field(0.28, 0.78 + i * 0.03, 0.20, 0.031, False))
    shield_card_front_template['fld_quickref_effect'].append(Field(0.64, 0.78 + i * 0.03, 0.50, 0.031, False))

shield_card_back_template['fld_part_name'] = []
shield_card_back_template['fld_part_effect'] = []
for i in range(14):
    shield_card_back_template['fld_part_name'].append(Field(0.17, 0.25 + i * 0.033, 0.18, 0.030, False))
    shield_card_back_template['fld_part_effect'].append(Field(0.41, 0.25 + i * 0.033, 0.3, 0.030, False))
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
        card_front = draw_field_locations(card_front, shield_card_front_template)
        card_back = draw_field_locations(card_back, shield_card_back_template)

    # Add Shield Image
    card_field = shield_card_front_template['fld_gun_img']
    img_to_insert = Image.open(shield_obj.asset['path_to_img'])
    card_front = draw_image_to_field(card_front, img_to_insert, card_field)

    # Add Manufacturer logo
    card_field = shield_card_front_template['fld_guild_logo']
    symbol = Image.open(f"img/guild_logo/AdvancedBnB/{shield_obj.manufacturer.logo_file}")
    card_front = draw_image_to_field(card_front, symbol, card_field)
    card_back = draw_image_to_field(card_back, symbol, card_field)

    # Add Gun type symbol
    card_field = shield_card_front_template['fld_guntype_logo']
    symbol = Image.open(f"img/gun_symbol/shield.png")
    card_front = draw_image_to_field(card_front, symbol, card_field)
    card_back = draw_image_to_field(card_back, symbol, card_field)

    # Add Element symbols
    if shield_obj.forced_elemental or not shield_obj.forced_non_elemental:
        card_field = shield_card_front_template['fld_element']

        n_symbols = len(shield_obj.elements)

        for i in range(n_symbols):
            _w = card_field.w / n_symbols
            _h = card_field.h
            _x = card_field.x
            if n_symbols == 2:
                _x = card_field.x + (i * _w) - (_w / 2)
            _y = card_field.y
            subfield = Field(_x, _y, _w, _h, True)

            el = shield_obj.elements[i]
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

    # Add shield name
    card_field = shield_card_front_template['fld_name']
    card_front = draw_text_to_field(card_front, card_field, f"{shield_obj.name_prefix + ' ' if shield_obj.name_prefix != '' else ''}{shield_obj.name}", 'rexlia rg.otf')
    card_back = draw_text_to_field(card_back, card_field,f"{shield_obj.name_prefix + ' ' if shield_obj.name_prefix != '' else ''}{shield_obj.name}",'rexlia rg.otf')

    # Add Rarity and Shield Type
    card_field = shield_card_front_template['fld_rarity_txt']
    card_front = draw_text_to_field(card_front, card_field, f"{shield_obj.rarity}".upper(), 'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf')
    card_back = draw_text_to_field(card_back, card_field, f"{shield_obj.rarity}".upper(),'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf')

    card_field = shield_card_front_template['fld_guntype_txt']
    card_front = draw_text_to_field(card_front, card_field, f"{shield_obj.shield_type}".upper(),'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf')
    card_back = draw_text_to_field(card_back, card_field, f"{shield_obj.shield_type}".upper(),'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf')

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

    # Collect Situational Parts
    quick_ref = []

    for part in shield_obj.parts:
        if part.situational:
            if part.name not in [x.name for x in quick_ref]:
                quick_ref.append(part)

    print(len(quick_ref))


    # Quick Reference
    idx = 0
    quick_ref = quick_ref[:5]
    for i in range(len(quick_ref)):
        ref = quick_ref[i]
        name_field = shield_card_front_template['fld_quickref_name'][idx]
        card_front = draw_text_to_field(card_front, name_field, f"{ref.name}:",'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf', align='left', font_size=25)

        ef_text = split_text_on_length(f"{ref.to_text(shield_obj)}", 70)
        for line in ef_text:
            if idx < 6:
                effect_field = shield_card_front_template['fld_quickref_effect'][idx]
            card_front = draw_text_to_field(card_front, effect_field, line, 'avenir-next-condensed-medium.otf', align='left', font_size=25)
            idx += 1

    # Shield Parts / Tag - Collecting column contents
    header_col = []
    effect_col = []
    header_idx = [0]

    header_col.append(f"--Shield Parts--")
    effect_col.append('')

    for i in range(len(shield_obj.parts)):
        part = shield_obj.parts[i]
        header_col.append(f"{part.name}:")

        ef_str = split_text_on_length(f"{part.effect}", 65)
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
        _offset = 0.462 / max([len(header_col), 12])
        name_field = Field(0.17, 0.25 + i * _offset, 0.18, 0.030, False)
        effect_field = Field(0.41, 0.25 + i * _offset, 0.3, 0.030, False)

        font = fonts['name']
        if i in header_idx:
            font = fonts['header']

        card_back = draw_text_to_field(card_back, name_field, header_col[i],font, align='left', font_size=22)
        card_back = draw_text_to_field(card_back, effect_field, effect_col[i], fonts['effect'], align='left',font_size=22)


    # Mods & Checks
    card_field = shield_card_back_template['fld_mod_effects'][0]
    card_back = draw_text_to_field(card_back, card_field, f"--Mods & Checks--", 'rexlia rg.otf', align='left', font_size=22)

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

