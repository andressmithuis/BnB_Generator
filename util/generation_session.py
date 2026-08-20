from collections.abc import Callable, Generator

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
        print(f"INFO EVENT: {self.prompt.replace('\n', '')}")


class WarningEvent(GenerationEvent):
    def __init__(self, prompt, **kwargs):
        super().__init__(**kwargs)
        self.prompt = prompt
        print(f"WARNING EVENT: {self.prompt.replace('\n', '')}")


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
        print(f"DICEREQUEST EVENT: {self.prompt.replace('\n', '')}")


class GenerationSession:
    def __init__(self, generator_func):
        self.generator_func = generator_func
        self.generator = self.generator_func()

    def start(self):
        return self.submit(None)

    def submit(self, dice_result):
        try:
            event = self.generator.send(dice_result)
        except StopIteration as e:
            return e.value

        return event

    def reset(self):
        self.generator = self.generator_func()

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


class GenerationOverrides:
    def __init__(self):
        self.overrides: dict[str, object] = {}

    def set(self, name: str, value: any) -> None:
        self.overrides.update({name: value})

    def apply(self, var_name: str, var_value: any) -> any:
        ret = self.overrides.get(var_name, var_value)
        if ret != var_value:
            print(f"Property '{var_name}' replaced <{var_value}> with <{ret}>")
            yield InfoEvent(f"Property '{var_name}' replaced <{var_value}> with <{ret}>")

        return ret

