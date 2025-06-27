import os
from PIL import Image, ImageFile, ImageDraw, ImageFont, ImageOps

from util import Rarity
from util.cards.card_generation import Field, draw_image_to_field, draw_text_to_field, draw_field_locations, split_text_on_length, recolor_image

shield_card_template = {
    'fld_name': Field(0.498, 0.095, 0.38, 0.10, False),
    'fld_img': Field(0.66, 0.45, 0.45, 0.38, False),
    'fld_red_txt': Field(0.66, 0.68, 0.45, 0.08, False),

    'fld_rarity_txt': Field(0.14, 0.18, 0.15, 0.018, False),
    'fld_guild_logo': Field(0.14, 0.145, 0.15, 0.038, False),
    'fld_guntype_txt': Field(0.855, 0.18, 0.15, 0.018, False),
    'fld_shield_icon': Field(0.855, 0.145, 0.15, 0.038, False),

    'fld_element': Field(0.115, 0.85, 0.11, 0.11, False),

    'fld_cap_icon': Field(0.18, 0.40, 0.12, 0.12, True),
    'fld_rr_icon': Field(0.18, 0.58, 0.12, 0.12, True),

    'fld_cap_val': Field(0.30, 0.40, 0.12, 0.12, True),
    'fld_rr_val': Field(0.30, 0.58, 0.12, 0.12, True),

    'fld_mod_txt': Field(0.56, 0.82, 0.74, 0.09, False)
}

def generate_shield_card(shield_obj):
    # Take gun card template (blank card) based on rarity
    path = f"./img/blank_cards/shield_card_blank_{shield_obj.rarity.lower()}.webp"
    assert os.path.isfile(path), f"ERROR - Path to blank gun card file is not correct: <{path}>"

    card_img = Image.open(path)
    #card_img = draw_field_locations(card_img, shield_card_template)

    # Add Shield Image
    card_field = shield_card_template['fld_img']
    img_to_insert = Image.open(shield_obj.asset['path_to_img'])
    card_img = draw_image_to_field(card_img, img_to_insert, card_field)

    # Add Manufacturer logo
    card_field = shield_card_template['fld_guild_logo']
    symbol = Image.open(f"img/guild_logo/StandardBnB/{shield_obj.guild.logo_file}")
    card_img = draw_image_to_field(card_img, symbol, card_field)

    # Add Shield type symbol
    card_field = shield_card_template['fld_shield_icon']
    symbol = Image.open(f"img/gun_symbol/shield.png")
    card_img = draw_image_to_field(card_img, symbol, card_field)

    # Add Element symbols
    card_field = shield_card_template['fld_element']
    gun_elements = list(set(shield_obj.elements))[:6]
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

    # Add shield name
    card_field = shield_card_template['fld_name']
    card_img = draw_text_to_field(card_img, card_field, f"{shield_obj.name_prefix + ' ' if shield_obj.name_prefix != '' else ''}{shield_obj.name}", 'rexlia rg.otf')

    # Add Rarity and Gun Type
    card_field = shield_card_template['fld_rarity_txt']
    card_img = draw_text_to_field(card_img, card_field, shield_obj.rarity.upper(), 'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf')

    card_field = shield_card_template['fld_guntype_txt']
    card_img = draw_text_to_field(card_img, card_field, 'SHIELD', 'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf')

    # Capacity and Recharge Rate
    # Icons
    colors = {
        Rarity.COMMON: (191, 191, 191),
        Rarity.UNCOMMON: (0, 102, 0),
        Rarity.RARE: (0, 0, 179),
        Rarity.EPIC: (128, 0, 128),
        Rarity.LEGENDARY: (204, 122, 0),
    }
    card_field = shield_card_template['fld_cap_icon']
    icon = Image.open(f"img/item_icons/shield_capacity.png")
    icon = recolor_image(icon, colors[shield_obj.rarity])
    card_img = draw_image_to_field(card_img, icon, card_field)

    card_field = shield_card_template['fld_rr_icon']
    icon = Image.open(f"img/item_icons/shield_rechargerate.png")
    icon = recolor_image(icon, colors[shield_obj.rarity])
    card_img = draw_image_to_field(card_img, icon, card_field)

    # Value
    card_field = shield_card_template['fld_cap_val']
    card_img = draw_text_to_field(card_img, card_field, f"{shield_obj.capacity}", 'rexlia rg.otf', color=(11, 121, 189), font_size=50)

    card_field = shield_card_template['fld_rr_val']
    card_img = draw_text_to_field(card_img, card_field, f"{shield_obj.recharge_rate}",'rexlia rg.otf', color=(11, 121, 189), font_size=50)

    # Modifier Texts
    ef_name = []
    ef_text = []

    # Gun Effects
    for ef in shield_obj.effects:
        ef_name.append(f"{ef.name}:")
        ef_lines = split_text_on_length(f"{ef.to_text(shield_obj)}", 65)
        for line in ef_lines:
            ef_text.append(line)

        while len(ef_name) < len(ef_text):
            ef_name.append('')

    # Stat Mods & Checks
    if 'mods' in shield_obj.mod_stats:
        mods = shield_obj.mod_stats['mods']
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
    shield_card_template['fld_ef_name'] = []
    shield_card_template['fld_ef_text'] = []
    for i in range(max([len(ef_name), 6])):
        shield_card_template['fld_ef_name'].append(Field(0.28, 0.78 + i * 0.03, 0.20, 0.031, False))
        shield_card_template['fld_ef_text'].append(Field(0.64, 0.78 + i * 0.03, 0.50, 0.031, False))

    # Print Effects, Mods & Checks to the Card
    for i in range(len(ef_name)):
        name_field = shield_card_template['fld_ef_name'][i]
        text_field = shield_card_template['fld_ef_text'][i]

        card_img = draw_text_to_field(card_img, name_field, ef_name[i], 'Avenir-Next-LT-Pro-Demi-Condensed_5186.ttf',
                                      align='left', font_size=25)
        card_img = draw_text_to_field(card_img, text_field, ef_text[i], 'avenir-next-condensed-medium.otf',
                                      align='left', font_size=25)

    card_img.show()

    card_img.save('test.bmp', 'BMP', quality=100)

def draw_text_to_modfield(img: ImageFile, field: Field, text: str, font_file: str, color=(0, 0, 0)):
    # TODO: Fit font_size to text width
    # Convert image to PIL
    draw = ImageDraw.Draw(img)

    # Resize font until it fits the field
    tl, br = field.get_bbox(img)
    field_w = br[0] - tl[0]
    field_h = br[1] - tl[1]

    font_size = int(round(field_h / 3 * 0.91))
    spacing = int(round(0.5 * font_size))
    font = ImageFont.truetype('fonts/' + font_file, font_size)

    field_bb = field.get_bbox(img)
    text_origin = field_bb[0]

    draw.text(text_origin, text, font=font, fill=color, align='left', spacing=spacing)

    return img
