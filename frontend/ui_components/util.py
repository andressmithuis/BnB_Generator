import numpy as np
from kivy.graphics.texture import Texture

def img_to_texture(pil_image):
    pil_image = pil_image.convert('RGBA')
    w, h = pil_image.size
    data = np.frombuffer(pil_image.tobytes(), dtype=np.uint8)

    texture = Texture.create(size=(w, h), colorfmt='rgba')
    texture.blit_buffer(data.tobytes(), colorfmt='rgba', bufferfmt='ubyte')
    texture.flip_vertical()

    return texture