import random
from dataclasses import dataclass

class Dice:
    input_rolls = False

    def __init__(self, count, sides):
        self.count = count
        self.sides = sides

    def __repr__(self):
        return f"{self.count}d{self.sides}"

    def rolls(self):
        return [random.randint(1, self.sides) for _ in range(self.count)]

    def roll(self):
        rolls = self.rolls()
        total = sum(rolls)

        return total

    @staticmethod
    def from_string(dice_str: str):
        str_parts = dice_str.split('d')
        if len(str_parts) != 2:
            raise ValueError(f"Invalid dice format: {dice_str}")

        count = int(str_parts[0])
        sides = int(str_parts[1])

        return Dice(count, sides)

    @staticmethod
    def best_dice_for_table(table):
        dice_table = {
            (1, 4): '1d4',
            (5, 6): '1d6',
            (7, 8): '1d8',
            (9, 10): '1d10',
            (11, 12): '1d12',
        }

        best_dice = lookup_in_table(dice_table, len(table))
        if best_dice is None:
            best_dice = '1d20'

        return Dice.from_string(best_dice)

    @property
    def value_range(self):
        return self.count, self.count * self.sides






def lookup_in_table(table: dict, dice_roll: int):
    for index, row in table.items():
        # Handle if table rows have value ranges
        if isinstance(index, tuple):
            (lo, hi) = index
            if lo <= dice_roll <= hi:
                return row

        # Assume table has single value items
        else:
            if index == dice_roll:
                return row

    print(f"Roll {dice_roll} not present in given table!")
    return None
