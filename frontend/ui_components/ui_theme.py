from file_handling import resource_path

class UITheme:
    class Button:
        PRIMARY = (0.267, 0.369, 0.435, 1)
        DANGER = (0.439, 0.227, 0.239, 1)
        DISABLED = (0.122, 0.145, 0.165, 1)
        DISABLED_TEXT = (0.4, 0.4, 0.4, 1)

    class Panel:
        BG_LIGHT = (0.757, 0.702, 0.553, 1)
        BG_LIGHT_2 = (0.949, 0.929, 0.898, 1)
        BG_GRAY = (0.729, 0.745, 0.776, 1)
        BG_DARK = (0.122, 0.145, 0.165, 1)
        BG_BORDER = (0.725, 0.737, 0.757, 1)

    class colors:
        HIT_BLUE = (0.267, 0.369, 0.435, 1)
        CRIT_RED = (0.439, 0.227, 0.239, 1)
        TINY_TINA_PINK = (0.902, 0.451, 0.969, 1)
        TINY_TINA_PURPLE = (0.396, 0.204, 0.545, 1)
        LIME_GREEN = (0.631372549019608,0.980392156862745,0.309803921568627,1)

    class fonts:
        CARD_TITLE = resource_path('fonts/rexlia rg.otf')
