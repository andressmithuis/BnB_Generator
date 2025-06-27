class Shieldtype:
    name = ''

    def __repr__(self):
        return f"{self.__class__.name}"


class Balanced(Shieldtype):
    name = 'Balanced'

    @staticmethod
    def get_basestats(tier):
        table = {
            1: {'capacity': 30, 'charge_rate': 10},
            2: {'capacity': 45, 'charge_rate': 15},
            3: {'capacity': 60, 'charge_rate': 20},
            4: {'capacity': 75, 'charge_rate': 25},
            5: {'capacity': 90, 'charge_rate': 30},
            6: {'capacity': 105, 'charge_rate': 35},
            7: {'capacity': 120, 'charge_rate': 40},
            8: {'capacity': 135, 'charge_rate': 45},
            9: {'capacity': 150, 'charge_rate': 50},
            10: {'capacity': 165, 'charge_rate': 55},
        }

        return table[tier]


class HighCapacity(Shieldtype):
    name = 'High Capacity'

    @staticmethod
    def get_basestats(tier):
        table = {
            1: {'capacity': 40, 'charge_rate': 5},
            2: {'capacity': 60, 'charge_rate': 10},
            3: {'capacity': 80, 'charge_rate': 10},
            4: {'capacity': 100, 'charge_rate': 15},
            5: {'capacity': 120, 'charge_rate': 15},
            6: {'capacity': 140, 'charge_rate': 20},
            7: {'capacity': 160, 'charge_rate': 20},
            8: {'capacity': 180, 'charge_rate': 25},
            9: {'capacity': 200, 'charge_rate': 25},
            10: {'capacity': 220, 'charge_rate': 30},
        }

        return table[tier]


class Fast(Shieldtype):
    name = 'Fast'

    @staticmethod
    def get_basestats(tier):
        table = {
            1: {'capacity': 20, 'charge_rate': 10},
            2: {'capacity': 30, 'charge_rate': 20},
            3: {'capacity': 40, 'charge_rate': 25},
            4: {'capacity': 50, 'charge_rate': 35},
            5: {'capacity': 60, 'charge_rate': 40},
            6: {'capacity': 70, 'charge_rate': 50},
            7: {'capacity': 80, 'charge_rate': 55},
            8: {'capacity': 90, 'charge_rate': 65},
            9: {'capacity': 100, 'charge_rate': 70},
            10: {'capacity': 110, 'charge_rate': 80},
        }

        return table[tier]


class Shieldtypes:
    BALANCED = Balanced(),
    HIGHCAPACITY = HighCapacity(),
    FAST = Fast()
