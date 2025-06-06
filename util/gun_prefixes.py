from .modifier import Modifier

class Prefix(Modifier):
    name = '<Prefix>'
    effect = '<Prefix Effect>'
    print_to_card = True

    def apply(self, gun):
        return


class prefix_crappy(Prefix):
    name = 'Crappy'
    effect = '-2 DMG MOD'

    def apply(self, gun):
        gun.mod_stats.setdefault('mods', {}).setdefault('dmg_mod', 0)
        gun.mod_stats['mods']['dmg_mod'] -= 2
