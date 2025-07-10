import os

from util.cards.card_basics import *
from util.cards.card_generation import *

card_front_template = {
    'fld_red_txt': Field(0.66, 0.68, 0.45, 0.08, False),
    
    'fld_dice_img': Field(0.25, 0.50, 0, 0.22, True),
    'fld_dice_cnt': Field(0.15, 0.575, 0, 0.12, True),
}

card_back_template = {
    'fld_type_bonus_txt': Field(0.28, 0.72, 0.2, 0.05, False),
    'fld_type_bonus_effect': Field(0.535, 0.82, 0.71, 0.14, False),

    'fld_part_name': Field(0.17, 0.25, 0.18, 0.030, False),
    'fld_part_effect': Field(0.41, 0.25, 0.3, 0.030, False),

    'fld_mod_effects': []
}

for i in range(14):
    card_back_template['fld_mod_effects'].append(Field(0.82, 0.25 + i * 0.033, 0.18, 0.030, False))

def generate_relic_card(item_obj):
    # Take card template (blank card) based on rarity
    str = f"{item_obj.rarity}".lower()
    path = f"./img/blank_cards/shield_card_blank_{str}.webp"
    assert os.path.isfile(path), f"ERROR - Path to blank card file is not correct: <{path}>"
    card_front = Image.open(path)

    if False:
        card_front = draw_field_locations(card_front, basic_card_template)
        card_front = draw_field_locations(card_front, card_front_template)

    # Add Relic Image
    img_to_insert = Image.open(item_obj.asset['path_to_img'])
    card_front = card_add_item_image(card_front, img_to_insert)

    # Add Manufacturer logo
    symbol = Image.open(f"img/guild_logo/AdvancedBnB/{item_obj.manufacturer.logo_file}")
    card_front = card_add_tl_logo(card_front, symbol)

    # Add Relic type symbol
    symbol = Image.open(f"img/item_icons/relic.png")
    card_front = card_add_tr_logo(card_front, symbol)

    # Add Element symbols
    card_front = card_add_element(card_front, item_obj)

    # Add Item name
    item_name = f"{item_obj.name_prefix + ' ' if item_obj.name_prefix != '' else ''}{item_obj.name}"
    card_front = card_add_item_name(card_front, item_name)

    # Add Rarity and Item Type
    item_rarity = f"{item_obj.rarity}".upper()
    card_front = card_add_tl_text(card_front, item_rarity)

    item_type = f"{item_obj.type.name} Relic".upper()
    card_front = card_add_tr_text(card_front, item_type)

    # Quick Reference
    quick_ref = []
    for part in item_obj.parts:
        if part.situational:
            if part.name not in [x.name for x in quick_ref]:
                quick_ref.append(part)

    card_front = card_add_quick_ref(card_front, quick_ref, item_obj)

    # Collect part count / deduplication of parts
    dedup_list = []
    for part in item_obj.parts:
        part_added = False
        for dedup_part in dedup_list:
            if part == dedup_part['part']:
                dedup_part['count'] += 1
                part_added = True
                break

        if not part_added:
            dedup_list.append({'part': part, 'count': 1})

    quick_ref = []
    for entry in dedup_list:
        part = entry['part']
        count = entry['count']
        if count > 1:
            part.name = f"{part.name} x{count}"

        quick_ref.append(part)

    card_front = card_add_quick_ref(card_front, quick_ref, item_obj)

    # Save Result
    card_front.show()

    card_front.save('test.bmp', 'BMP', quality=100)

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

