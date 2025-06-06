import cv2

def generate_blank_cards(file, outfile_prefix):
    card = cv2.imread(file)
    mask = cv2.imread('img/blank_cards/mask_rarity_border.bmp')
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    for type in ['common', 'uncommon', 'rare', 'epic', 'legendary']:
        border = cv2.imread(f"border_{type}.bmp")

        print(card.shape, mask.shape)

        new_card = cv2.bitwise_or(card, card, mask=(255 - mask))
        new_card = cv2.bitwise_or(new_card, border)

        cv2.imshow('new card', new_card)
        cv2.imwrite(f"img/blank_cards/{outfile_prefix}_{type}.webp", new_card)
        cv2.waitKey(0)
