from dataclasses import dataclass
from .dice import Dice


@dataclass
class DiceRequest:
    dice: str
    prompt: str

class GenerationSession:
    def __init__(self, generator_obj, manual=False):
        self.generator = generator_obj
        self.manual = manual

    def start(self):
        return self.submit(None)

    def submit(self, dice_result):
        while True:
            try:
                request = self.generator.send(dice_result)
            except StopIteration as e:
                return e.value

            if self.manual is False:
                dice = Dice.from_string(request.dice)
                dice_result = dice.roll()
                print(f"{request.prompt}: {dice_result}")
            else:
                return request
