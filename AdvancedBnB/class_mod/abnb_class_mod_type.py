from copy import deepcopy

from util import Dice, lookup_in_table, Rarity


class ClassModtype:
    name: ''
    prefixes = {
        (1, 6): {'prefix': 'Class Mod Name Prefix', 'skill': 'Class Mod Skill Name'},
    }
    manufacturer = None

    passive = None

    legendary_effect = None
    legendary_skills = []

    def pick_skills(self, roll):
        skills = []

        # Pick main skill
        pfx = lookup_in_table(self.prefixes, roll)
        skills.append(pfx)

        # Pick secondary skill
        tmp_roll = roll - 2
        if roll % 2 == 0:
            tmp_roll = roll + 2

        if tmp_roll < 1:
            tmp_roll += 6
        if tmp_roll > 6:
            tmp_roll -= 6

        pfx = lookup_in_table(self.prefixes, tmp_roll)
        skills.append(pfx)

        # Pick remaining skill
        for k, v in self.prefixes.items():
            if v not in skills:
                skills.append(v)

        return skills

    def create(self, item):
        item.name = self.name
        item.manufacturer = self.manufacturer
        item.passive_effect = self.passive

        if item.rarity == Rarity.LEGENDARY:
            bonus = skill_bonus[min([item.tier, 5])][item.rarity]

            item.name_prefix = 'Legendary'
            item.legendary_effect = self.legendary_effect

            for i in range(len(self.legendary_skills)):
                item.add_skill(self.legendary_skills[i], bonus[i])

        elif item.rarity != Rarity.COMMON:
            bonus = skill_bonus[min(item.tier, 5)][item.rarity]

            pfx = self.pick_skills(Dice.from_string('1d6').roll())

            for i in range(len(bonus)):
                if i == 0:  # First Skill/Prefix
                    item.name_prefix = pfx[0]['prefix']

                item.add_skill(pfx[i]['skill'], bonus[i])


skill_bonus = {
    1: { Rarity.UNCOMMON: [1], Rarity.RARE: [1, 1], Rarity.EPIC: [1, 1, 1], Rarity.LEGENDARY: [] },
    2: { Rarity.UNCOMMON: [2], Rarity.RARE: [2, 1], Rarity.EPIC: [2, 1, 1], Rarity.LEGENDARY: [] },
    3: { Rarity.UNCOMMON: [2], Rarity.RARE: [2, 1], Rarity.EPIC: [2, 2, 2], Rarity.LEGENDARY: [1, 1, 1, 1, 1] },
    4: { Rarity.UNCOMMON: [3], Rarity.RARE: [3, 2], Rarity.EPIC: [3, 2, 2], Rarity.LEGENDARY: [2, 2, 2, 2, 2] },
    5: { Rarity.UNCOMMON: [3], Rarity.RARE: [3, 3], Rarity.EPIC: [3, 3, 3], Rarity.LEGENDARY: [3, 3, 3, 3, 3] },
}








