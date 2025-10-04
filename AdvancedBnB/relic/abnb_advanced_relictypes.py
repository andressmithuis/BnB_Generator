from copy import deepcopy

from util import Rarity, Dice
from .abnb_basic_relictypes import Relic, BasicRelictypes, basic_relics_table


sub_rarity = {
    Rarity.RARE: Rarity.COMMON,
    Rarity.EPIC: Rarity.UNCOMMON,
    Rarity.LEGENDARY: Rarity.RARE,
    Rarity.PEARLESCENT: Rarity.EPIC
}

class AdvancedRelic(Relic):
    sub_relic_types = []

    def create_part_pool(self, tier):
        pool = []
        for sub_relic in self.sub_relic_types:
            pool += sub_relic.create_part_pool(tier)

        return pool

# --- ADVANCED RELICS ---
class RelicBloodOTA(AdvancedRelic):
    name = 'Blood of the Ancients'
    sub_relic_types = [BasicRelictypes.STOCKPILE, BasicRelictypes.VITALITY]


class RelicBoneOTA(AdvancedRelic):
    name = 'Bone of the Ancients'
    sub_relic_types = [BasicRelictypes.ELEMENTAL, BasicRelictypes.PROFICIENCY]


class RelicHeartOTA(AdvancedRelic):
    name = 'Heart of the Ancients'
    sub_relic_types = [BasicRelictypes.AGGRESSION, BasicRelictypes.TENACITY]


class RelicSkinOTA(AdvancedRelic):
    name = 'Skin of the Ancients'
    sub_relic_types = [BasicRelictypes.PROTECTION, BasicRelictypes.RESISTANCE]


class RelicBrainOTA(AdvancedRelic):
    name = 'Brain of the Ancients'
    sub_relic_types = []

    def create_part_pool(self, tier):
        # Pick 2 (different!) random basic relics
        self.sub_relic_types = []
        while len(self.sub_relic_types) < 2:
            new_relic = basic_relics_table[Dice.from_string('1d10').roll()]
            if new_relic not in self.sub_relic_types:
                print(f"Brain of the Ancients: Selected Basic Relic: {new_relic.name}")
                self.sub_relic_types.append(new_relic)

        # Create part pool like normal
        return super().create_part_pool(tier)


class AdvancedRelictypes:
    BLOOD = RelicBloodOTA()
    BONE = RelicBoneOTA()
    HEART = RelicHeartOTA()
    SKIN = RelicSkinOTA()
    BRAIN = RelicBrainOTA()


advanced_relics_table = {
    (1, 2): AdvancedRelictypes.BLOOD,
    (3, 4): AdvancedRelictypes.BONE,
    (5, 6): AdvancedRelictypes.HEART,
    (7, 8): AdvancedRelictypes.SKIN,
    (9, 10): AdvancedRelictypes.BRAIN,
}
