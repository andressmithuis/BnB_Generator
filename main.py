import os.path
import argparse

# Put PIL ImageLoader first to support .webp files
from kivy.core.image import ImageLoader
from kivy.core.image.img_pil import ImageLoaderPIL
ImageLoader.loaders.remove(ImageLoaderPIL)
ImageLoader.loaders.insert(0, ImageLoaderPIL)
from kivy.config import Config
from kivy.core.window import Window

from util import GenerationEvent, DiceRequest, Dice, Rarity, GenerationSession
from frontend.card_editor import CardEditorApp

if __name__ == '__main__':
    Config.set('input', 'mouse', 'mouse,disable_multitouch')  # Disable debug touch markers on desktop
    Window.size = (1200, 800)

    # Start the application
    if True:
        CardEditorApp().run()


    if True:
        # CLI generation bypass for custom cards not supported by UI yet
        from AdvancedBnB import Gun, Guntypes

        equipment_obj = Gun()

        equipment_obj.overrides.set('name', 'Standard Issue')
        equipment_obj.overrides.set('rarity', Rarity.COMMON)
        equipment_obj.overrides.set('type', Guntypes.PISTOL)

        gen_session = GenerationSession(equipment_obj.generator_func)

        dice_roll = None
        while True:
            event = gen_session.submit(dice_roll)
            if isinstance(event, GenerationEvent):
                if isinstance(event, DiceRequest):
                    dice = Dice.from_string(event.dice)
                    dice_roll = dice.roll()
                else:
                    dice_roll = None
            else:
                break

        equipment_obj.render_card()
        equipment_obj.export_generated_card(dialog=False)


