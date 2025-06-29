from .abnb_tables import level_to_tiers


def get_item_tier(level:int):
    """
    Returns Item Tier based on Item Level

    1-30:   normal
    31-35:  TVH1
    36-40:  TVH2
    41-45:  UVH1
    46-50:  UVH2
    51+:    OP
    """

    assert level > 0, f"level argument given ({level}) is not at least 1"

    for (lo, hi), tier in level_to_tiers.items():
        if lo <= level <= hi:
            return tier