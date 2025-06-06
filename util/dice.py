import random

class Dice:
    def __init__(self, count, sides):
        self.count = count
        self.sides = sides

    def __repr__(self):
        return f"{self.count}d{self.sides}"

    def roll_dice(self, user=False):
        rolls = [random.randint(1, self.sides) for _ in range(self.count)]
        if user:
            rolls = self.ask_for_roll()

        return rolls

    def roll(self, user=False):
        roll = sum(self.roll_dice())
        if user:
            roll = self.ask_for_roll()

        return roll

    def ask_for_roll(self, text=None):
        roll = None
        if text is None:
            text = f"Please roll {self}"

        valid_roll = False
        while not valid_roll:
            roll = int(input(f"{text}:"))
            if self.count <= roll <= self.count * self.sides:
                valid_roll = True

        return roll


    @staticmethod
    def from_string(dice_str: str):
        str_parts = dice_str.split('d')
        if len(str_parts) != 2:
            raise ValueError(f"Invalid dice format: {dice_str}")

        count = int(str_parts[0])
        sides = int(str_parts[1])

        return Dice(count, sides)


def roll_on_table(table, dice_roll):
    for (lo, hi), row in table.items():
        if lo <= dice_roll <= hi:
            return row

    raise ValueError(f"Roll {dice_roll} not present in given table!")
