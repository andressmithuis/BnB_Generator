import os
from PIL import Image, ImageFile, ImageDraw, ImageFont, ImageOps

from util import Rarity
from util.cards.card_generation import Field, draw_image_to_field, draw_text_to_field, draw_field_locations, split_text_on_length, recolor_image
from util.cards.card_basics import *

shield_card_template = {
    'fld_red_txt': Field(0.66, 0.68, 0.45, 0.08, False),

    'fld_cap_icon': Field(0.18, 0.40, 0.12, 0.12, True),
    'fld_rr_icon': Field(0.18, 0.58, 0.12, 0.12, True),

    'fld_cap_val': Field(0.30, 0.40, 0.12, 0.12, True),
    'fld_rr_val': Field(0.30, 0.58, 0.12, 0.12, True),
}

def generate_shield_card(shield_obj):
    # Take gun card template (blank card) based on rarity
    path = f"./img/blank_cards/shield_card_blank_{shield_obj.rarity.lower()}.webp"
    assert os.path.isfile(path), f"ERROR - Path to blank gun card file is not correct: <{path}>"

    card_img = Image.open(path)

    # Add Shield Image
    img_to_insert = Image.open(shield_obj.asset['path_to_img'])
    card_img = card_add_item_image(card_img, img_to_insert)

    # Add Manufacturer logo
    symbol = Image.open(f"img/guild_logo/StandardBnB/{shield_obj.guild.logo_file}")
    card_img = card_add_tl_logo(card_img, symbol)

    # Add Shield type symbol
    symbol = Image.open(f"img/gun_symbol/shield.png")
    card_img = card_add_tr_logo(card_img, symbol)

    # Add Element symbols
    card_img = card_add_element(card_img, shield_obj)

    # Add shield name
    item_name = f"{shield_obj.name_prefix + ' ' if shield_obj.name_prefix != '' else ''}{shield_obj.name}"
    card_img = card_add_item_name(card_img, item_name)

    # Add Rarity and Shield Type
    item_rarity = f"{shield_obj.rarity}".upper()
    card_img = card_add_tl_text(card_img, item_rarity)

    card_img = card_add_tr_text(card_img, "SHIELD")

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

    # Quick reference
    # Determine Font Size
    ef_buffer = []
    for ef in shield_obj.effects:
        ef_buffer.append(f"{ef.to_text(shield_obj)}")

    if 'mods' in shield_obj.mod_stats:
        mods = shield_obj.mod_stats['mods']
        for k, v in mods.items():
            if v != 0:
                ef_buffer.append(f"{'+' if v > 0 else ''}{v}")

    font_file = card_fonts['default']
    fnt_size = get_max_font_size(card_img, ef_buffer, basic_card_template['fld_quickref_effect'], font_file)
    font = ImageFont.truetype(f"fonts/{font_file}", fnt_size)

    # Shield Effects
    ef_name = []
    ef_text = []

    for ef in shield_obj.effects:
        ef_name.append(f"{ef.name}:")
        ef_lines = wrap_text(card_img, f"{ef.to_text(shield_obj)}", font, basic_card_template['fld_quickref_effect'])
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
                ef_lines = wrap_text(card_img, f"{'+' if v > 0 else ''}{v}", font, basic_card_template['fld_quickref_name'])
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
