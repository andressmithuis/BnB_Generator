from dataclasses import dataclass
from .dice import Dice

from file_handling import resource_path

class GenerationEvent:
    def __init__(
            self,
            leading_img='',
            trailing_img=''
    ):
        self.anchor = 'right'
        self.prompt = ''
        self.leading_img_src = leading_img
        self.trailing_img_src = trailing_img


class InfoEvent(GenerationEvent):
    def __init__(self, prompt, **kwargs):
        super().__init__(**kwargs)
        self.prompt = prompt


class WarningEvent(GenerationEvent):
    def __init__(self, prompt, **kwargs):
        super().__init__(**kwargs)
        self.prompt = prompt


class AddPropertyEvent(InfoEvent):
    def __init__(self, property_type, property, **kwargs):
        prompt = f"Adding {property_type}"
        prompt += f"{' ' if property_type != '' else ''}"
        prompt += f"<[b][i]{property.name}[/i][/b]>\n-\n<[i]{property.effect}[/i]>"
        super().__init__(prompt, **kwargs)

class DiceRequest(GenerationEvent):
    def __init__(self, dice, prompt):
        super().__init__()
        self.type = 'dice_request'
        self.anchor = 'left'
        self.prompt = prompt
        self.dice = dice
        if dice == '1d100':
            dice = '1d10'
        elif dice not in ['1d4', '1d6', '1d8', '1d10', '1d12', '1d20']:
            dice = '1d20'
        self.leading_img_src = resource_path(f"img/dice_symbol/{dice}.png")


class GenerationSession:
    def __init__(self, generator_obj, manual=False):
        self.generator = generator_obj
        self.manual = manual

    def start(self):
        return self.submit(None)

    def submit(self, dice_result):
        try:
            event = self.generator.send(dice_result)
        except StopIteration as e:
            return e.value

        return event

class GeneratorSession:
    def __init__(self, generator_func):
        self.generator = generator_func

    def start(self):
        return self.submit(None)

    def submit(self, input_value):
        try:
            event = self.generator.send(input_value)
        except StopIteration as e:
            return e.value

        return event
