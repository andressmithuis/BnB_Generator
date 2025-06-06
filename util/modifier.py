class Modifier:
    name = '<Item Modifier>'
    effect = '<Changes the Stats of an Item.>'
    situational = False

    def apply(self, item):
        return

    def finalize(self, item):
        return

    def to_text(self, item):
        return f"{self}"

    def __str__(self):
        return f"{self.__class__.effect}"
