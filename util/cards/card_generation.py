from PIL import Image, ImageFont, ImageDraw, ImageFile, ImageOps


class Field:
    def __init__(self, x, y, w, h, sq):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.sq = sq

    def get_origin(self, img: ImageFile):
        img_w, img_h = img.size

        return round(self.x * img_w, 0), round(self.y * img_h, 0)

    def get_bbox(self, img: ImageFile):
        img_w, img_h = img.size

        _w = self.w * img_w
        _h = self.h * img_h
        if self.sq:
            if _h == 0:
                _h = _w
            if _w == 0:
                _w = _h
            _w = _h = min([_w, _h])

        tl_x = (self.x * img_w) - (_w / 2)
        tl_y = (self.y * img_h) - (_h / 2)

        br_x = (self.x * img_w) + (_w / 2)
        br_y = (self.y * img_h) + (_h / 2)

        # Return top-left, bottom-right coordinates
        return (int(round(tl_x, 0)), int(round(tl_y, 0))), (int(round(br_x, 0)), int(round(br_y,0)))


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


def draw_field_locations(img: ImageFile, template: dict):
    for key, field in template.items():
        if type(field) != list:
            field = [field]

        for fld in field:
            p1, p2 = fld.get_bbox(img)

            draw = ImageDraw.Draw(img)
            draw.rectangle([p1, p2], outline=(255, 0, 0))

    return img

def _get_text_offset(text, draw, font):
    anchor_bbox = draw.textbbox((0, 0), text, font=font, anchor='lt')
    anchor_center = (anchor_bbox[0] + anchor_bbox[2]) // 2, (anchor_bbox[1] + anchor_bbox[3]) // 2
    mask_bbox = font.getmask(text).getbbox()
    mask_center = (mask_bbox[0] + mask_bbox[2]) // 2, (mask_bbox[1] + mask_bbox[3]) // 2
    return anchor_center[0] - mask_center[0], anchor_center[1] - mask_center[1]

def draw_text_to_field(img: ImageFile, field: Field, text: str, font_file: str, color=(0, 0, 0), font_size=None, align='center'):
    # Convert image to PIL
    draw = ImageDraw.Draw(img)

    # Resize font until it fits the field
    font_size = font_size
    if font_size is None:
        tl, br = field.get_bbox(img)
        field_w = br[0] - tl[0]
        field_h = br[1] - tl[1]

        font_size = 100
        while True:
            font = ImageFont.truetype('fonts/' + font_file, font_size)
            text_bbox = font.getmask(text).getbbox()
            text_w = text_bbox[2] - text_bbox[0]
            text_h = text_bbox[3] - text_bbox[1]

            if text_w > field_w:
                ratio = field_w / text_w
                font_size = int(ratio * font_size)
            elif text_h > field_h:
                ratio = field_h / text_h
                font_size = int(ratio * font_size)
            else:
                break

    font = ImageFont.truetype('fonts/' + font_file, font_size)


    if align == 'center':
        text_anchor = 'mm'
        field_origin = field.get_origin(img)
        offset = (0, 0)

        if '\n' not in list(text):
            offset = _get_text_offset(text, draw, font)
            text_origin = (field_origin[0] + offset[0], field_origin[1] + offset[1])
        else:
            field_bb = field.get_bbox(img)
            text_origin = field_bb[0]
    else:
        field_bb = field.get_bbox(img)
        x_pos = field_bb[0][0]
        y_pos = (field_bb[0][1] + field_bb[1][1]) // 2
        text_origin = (x_pos, y_pos)
        text_anchor = 'lm'

    draw.text(text_origin, text, font=font, fill=color, anchor=text_anchor)

    return img

def draw_text_to_modfield(img: ImageFile, field: Field, text: str, font_file: str, color=(0, 0, 0)):
    # Convert image to PIL
    draw = ImageDraw.Draw(img)

    # Resize font until it fits the field
    tl, br = field.get_bbox(img)
    field_w = br[0] - tl[0]
    field_h = br[1] - tl[1]

    font_size = int(round(field_h / 2 * 0.91))
    spacing = int(round(0.5 * font_size))
    font = ImageFont.truetype('fonts/' + font_file, font_size)

    field_origin = field.get_origin(img)
    offset = (0, 0)
    if '\n' not in list(text):
        offset = _get_text_offset(text, draw, font)
        text_origin = (field_origin[0] + offset[0], field_origin[1] + offset[1])
    else:
        field_bb = field.get_bbox(img)
        text_origin = field_bb[0]

    draw.text(text_origin, text, font=font, fill=color, align='left', spacing=spacing)

    return img

def draw_image_to_field(base_img: ImageFile, insert_img: ImageFile, field: Field):
    p1, p2 = field.get_bbox(base_img)
    field_w = p2[0] - p1[0]
    field_h = p2[1] - p1[1]

    insert_img = ImageOps.contain(insert_img, (field_w, field_h), method=Image.Resampling.LANCZOS)
    img_w, img_h = insert_img.size

    # Calculate Top-Left corner position of the newly resized image
    origin_x, origin_y = field.get_origin(base_img)
    p1 = (int(origin_x - round((img_w / 2), 0)), int(origin_y - round((img_h / 2), 0)))

    base_img.paste(insert_img, box=p1, mask=insert_img.split()[3])

    return base_img

def recolor_image(src_image, new_color):
    alpha = src_image.getchannel('A')
    img_out = Image.new('RGBA', src_image.size, new_color + (0,))
    img_out.putalpha(alpha)

    return img_out

def wrap_text(img, text_str, font, field):
    tl, br = field.get_bbox(img)
    max_width = br[0] - tl[0]
    draw = ImageDraw.Draw(img)

    lines = []
    for paragraph in text_str.split('\n'):
        line = []
        for word in paragraph.split():
            tmp_line = ' '.join(line + [word])
            if draw.textlength(tmp_line, font=font) <=  max_width:
                line.append(word)
            else:
                lines.append(' '.join(line))
                line = [word]

        # End of Line
        if line:
            lines.append(' '.join(line))

    return lines

def get_max_font_size(img, text_list, field, font_file):
    fnt_size_min = 5
    fnt_size_max = 25

    tl, br = field.get_bbox(img)
    max_height = br[1] - tl[1]

    for fnt_size in range(fnt_size_max, fnt_size_min - 1, -1):
        # Load font with new font size
        font = ImageFont.truetype(f"fonts/{font_file}", fnt_size)

        text_height = 0
        for line in text_list:
            wrapped = wrap_text(img, line, font, field)
            # Bounding Box Height * 1.1 for a little bit of space between rows
            tst_bbox = font.getbbox("Ay")
            row_h = ((tst_bbox[3] - tst_bbox[1]) * 1.2) * max(1, len(wrapped))
            text_height += row_h

        if text_height <= max_height:
            return fnt_size

    return fnt_size_min




