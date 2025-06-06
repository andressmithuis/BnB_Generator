import cv2
import numpy as np
import pypdfium2 as pdfium

def convert_pdf(pdf_filename):
    """
    Splits a PDF document into separate pages and saves them as an image.
    """
    pdf = pdfium.PdfDocument(pdf_filename)

    for i in range(len(pdf)):
        page = pdf[i]
        img = page.render(scale=5).to_pil()
        img.save(f"page_{i}.bmp", 'BMP')


def cutout_weapon_cards():
    """
    Loads on of the PDF image files and tries to extract the weapon cards.
    Saves them each as a separate image file
    """
    # Offset Top-Left
    # Offset between images (line width)

    page = cv2.imread('page_0.bmp')
    page = cv2.cvtColor(page, cv2.COLOR_BGR2HSV)

    # HSV range
    lo_hsv = np.array([140, 200, 200])
    hi_hsv = np.array([180, 200, 200])

    lo_hsv = np.array([140, 194, 189])
    hi_hsv = np.array([180, 214, 209])

    mask = cv2.inRange(page, lo_hsv, hi_hsv)

    cv2.floodFill(mask, None, (0, 0), 255)
    mask = (255 - mask)

    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]

    margin = 2
    x, y, w, h = (0, 0, 0, 0)
    for c in contours:
        (_x, _y, _w, _h) = cv2.boundingRect(c)
        w += _w
        h += _h

    w = int(w / len(contours))
    h = int(h / len(contours))
    w = w - margin * 2
    h = h - margin * 2

    out = []
    for c in contours:
        (x, y, _w, _h) = cv2.boundingRect(c)
        x = x + margin
        y = y + margin

        card_img = page[y:y+h, x:x+w]
        card_img = cv2.cvtColor(card_img, cv2.COLOR_HSV2BGR)
        out.append(card_img)
        cv2.imwrite(f"Card_{len(out)}.webp", card_img)


    for i in range(len(out)):
        print(out[i].shape)
    #cv2.waitKey(0)


def extract_rarity_border():
    """
    Tries to extract the Rarity Border of one of the Gun Cards.
    It takes a difference of 2 Gun Cards (with different rarities), and applies a threshold in order to create a mask.
    It then uses that mask to extract an image with ONLY the Rarity Border of the original image.
    """
    img_1 = cv2.imread('Card_3.webp')
    img_2 = cv2.imread('Card_8.webp')
    #mask = cv2.imread('mask_scale5.bmp')
    #mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    if True:
        res = cv2.subtract(img_2, img_1)
        (b, g, r) = cv2.split(res)

        cv2.imshow('b', b)
        cv2.imshow('g', g)
        cv2.imshow('r', r)

        g = cv2.subtract(g, b)
        g = cv2.subtract(g, r)

        _, mask = cv2.threshold(g, 10, 250, cv2.THRESH_OTSU)

    border = cv2.bitwise_and(img_1, img_1, mask=mask)
    inv_mask = (255 - mask)
    new_card = cv2.bitwise_and(img_2, img_2, mask=inv_mask)
    new_card = cv2.bitwise_or(border, new_card)

    #mask = cv2.inRange(res, lo_hsv, hi_hsv)
    cv2.imshow('original', img_2)
    cv2.imshow('mask', mask)
    cv2.imshow('border', border)
    cv2.imshow('new_card', new_card)
    #cv2.imwrite('border_rare.bmp', border)
    cv2.waitKey(0)


def apply_rarity_border():
    """
    Takes the Rarity Border, its mask and another Gun card and combines them into a Gun Card with that Rarity Border
    :return:
    """
    card = cv2.imread('shield_card_blank_common.png')
    mask = cv2.imread('mask_scale5.bmp')
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    border = cv2.imread('border_rare.bmp')

    print(card.shape, mask.shape)

    new_card = cv2.bitwise_or(card, card, mask=(255-mask))
    new_card = cv2.bitwise_or(new_card, border)

    cv2.imshow('new card', new_card)
    cv2.imwrite('shield_card_blank_rare.webp', new_card)
    cv2.waitKey(0)