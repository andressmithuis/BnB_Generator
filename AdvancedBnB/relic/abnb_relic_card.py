import os

from util.cards.card_basics import *
from util.cards.card_generation import *

card_front_template = {
    'fld_item_img': Field(0.24, 0.49, 0.30, 0.39, False),
    'fld_red_txt': Field(0.66, 0.68, 0.45, 0.08, False),

    'fld_part_name': Field(0.50, 0.5, 0.18, 0.50, False),
    'fld_part_effect': Field(0.76, 0.5, 0.32, 0.50, False),
}

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
    card_front = card_add_item_image(card_front, img_to_insert, alt_field=card_front_template['fld_item_img'])

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

    # Collecting column content
    header_col = []
    effect_col = []
    header_idx = [0]

    header_col.append(f"--Relic Parts--")
    header_col.append('')
    effect_col.append('')
    effect_col.append('')

    for i in range(len(dedup_list)):
        part = dedup_list[i]['part']
        new_header = f"{part.name}"
        if dedup_list[i]['count'] > 1:
            new_header += f" x{dedup_list[i]['count']}"
        new_header += ':'

        header_col.append(new_header)
        effect_col.append(f"{part.to_text(item_obj)}")

        while len(header_col) < len(effect_col):
            header_col.append('')

    header_col.append('')
    effect_col.append('')

    col_content = []
    for i in range(len(header_col)):
        col_content.append((header_col[i], effect_col[i]))

    card_front = card_add_column_text(
        card_front,
        col_content,
        alt_col1_field=card_front_template['fld_part_name'],
        alt_col2_field=card_front_template['fld_part_effect'],
        header_idx=header_idx
    )

    # Save Result
    card_front.show()

    card_front.save('test.bmp', 'BMP', quality=100)
