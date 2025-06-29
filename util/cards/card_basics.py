import numpy as np
from copy import deepcopy

from util.cards.card_generation import *

basic_card_template = {
    'fld_item_name': Field(0.498, 0.095, 0.38, 0.10, False),
    'fld_item_img': Field(0.66, 0.45, 0.45, 0.38, False),

    # Top Left Box
    'fld_guild_logo': Field(0.14, 0.145, 0.15, 0.038, False),
    'fld_rarity_txt': Field(0.14, 0.18, 0.15, 0.018, False),

    # Top Right Box
    'fld_item_logo': Field(0.855, 0.145, 0.15, 0.038, False),
    'fld_type_txt': Field(0.855, 0.18, 0.15, 0.018, False),

    # Element Icon
    'fld_element': Field(0.115, 0.85, 0.11, 0.11, False),

    # Bottom Box
    'fld_quickref_name': Field(0.28, 0.84, 0.20, 0.151, False),
    'fld_quickref_effect': Field(0.655, 0.84, 0.54, 0.151, False),

}

card_fonts = {
    'header': 'rexlia rg.otf',
    'top_side_box_text': 'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf',
    'bold': 'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf',
    'default': 'avenir-next-condensed-medium.otf'
}

# Item Name, Image
def card_add_item_image(card_img, item_img):
    card_field = basic_card_template['fld_item_img']
    return draw_image_to_field(card_img, item_img, card_field)

def card_add_item_name(card_img, name):
    card_field = basic_card_template['fld_item_name']
    return draw_text_to_field(card_img, card_field, name, card_fonts['header'])

# Top Left Box
def card_add_tl_logo(card_img, logo_img):
    card_field = basic_card_template['fld_guild_logo']
    return draw_image_to_field(card_img, logo_img, card_field)

def card_add_tl_text(card_img, text):
    card_field = basic_card_template['fld_rarity_txt']
    return draw_text_to_field(card_img, card_field, text, card_fonts['top_side_box_text'])

# Top Right Box
def card_add_tr_logo(card_img, logo_img):
    card_field = basic_card_template['fld_item_logo']
    return draw_image_to_field(card_img, logo_img, card_field)

def card_add_tr_text(card_img, text):
    card_field = basic_card_template['fld_type_txt']
    return draw_text_to_field(card_img, card_field, text, card_fonts['top_side_box_text'])

# Element Symbol
def card_add_element(card_img, item_obj):
    if len(item_obj.elements) > 0:
        card_field = basic_card_template['fld_element']

        n_symbols = len(item_obj.elements)

        for i in range(n_symbols):
            _w = card_field.w / n_symbols
            _h = card_field.h
            _x = card_field.x
            if n_symbols == 2:
                _x = card_field.x + (i * _w) - (_w / 2)
            _y = card_field.y
            subfield = Field(_x, _y, _w, _h, True)

            el = item_obj.elements[i]
            if el.is_fusion:
                symbols = []
                for sub_el in el.fusion_elements:
                    filename = sub_el.name.lower()
                    symbols.append(Image.open(f"img/element_symbol/{filename}.png"))

                # Resize both images to biggest of the 2
                # Take half of both and stitch together
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
            else:
                filename = el.name.lower()
                symbol = Image.open(f"img/element_symbol/{filename}.png")

            card_img = draw_image_to_field(card_img, symbol, subfield)

            # Element bonus
            if el.bonus != 0:
                subfield.h = subfield.h / 4
                subfield.y += subfield.h * 0.75
                subfield.x += subfield.w * 0.25

                card_img = draw_text_to_field(card_img, subfield, f"+{el.bonus}", 'rexlia rg.otf', font_size=25)

    return card_img

# Quick Reference Info
def card_add_quick_ref(card_img, item_parts, item_obj):
    # Quick Reference n Rows and Font Size
    font_file = card_fonts['default']
    fnt_size = get_max_font_size(card_img, [x.to_text(item_obj) for x in item_parts], basic_card_template['fld_quickref_effect'], font_file)
    font = ImageFont.truetype(f"fonts/{font_file}", fnt_size)

    name_col = []
    effect_col = []
    for part in item_parts:
        name_col.append(f"{part.name}:")

        ef_text = wrap_text(card_img, part.to_text(item_obj), font, basic_card_template['fld_quickref_effect'])
        for line in ef_text:
            effect_col.append(line)

        while len(name_col) < len(effect_col):
            name_col.append('')

    # Print Quick Ref to Card
    y_offset = basic_card_template['fld_quickref_name'].h / max(len(name_col), 6)
    for i in range(len(name_col)):
        name_field = deepcopy(basic_card_template['fld_quickref_name'])
        effect_field = deepcopy(basic_card_template['fld_quickref_effect'])
        name_field.y = name_field.y - (name_field.h / 2) + (y_offset * i)
        effect_field.y = effect_field.y - (effect_field.h / 2) + (y_offset * i)

        card_img = draw_text_to_field(card_img, name_field, name_col[i],card_fonts['bold'], align='left', font_size=fnt_size)
        card_img = draw_text_to_field(card_img, effect_field, effect_col[i], card_fonts['default'],align='left', font_size=fnt_size)

    return card_img

def card_merge_sideways(card_left, card_right):
    # Merge front and back of card
    w1, h1 = card_left.size
    w2, h2 = card_right.size

    new_w = w1 + w2
    new_h = max(h1, h2)

    card_joined = Image.new("RGB", (new_w, new_h))
    card_joined.paste(card_left, (0, 0))
    card_joined.paste(card_right, (w1, 0))

    return card_joined