import itertools

class Platoon:
    """Represents a single platoon with a specific class and number of units."""
    PLATOON_CLASSES = {
        'Militia': lambda: PlatoonMilitia(),
        'Spearmen': lambda: PlatoonSpearmen(),
        'LightCavalry': lambda: PlatoonLightCavalry(),
        'HeavyCavalry': lambda: PlatoonHeavyCavalry(),
        'CavalryArcher': lambda: PlatoonCavalryArcher(),
        'FootArcher': lambda: PlatoonFootArcher(),
    }

    def __init__(self, unit_class, units):
        self.unit_class = unit_class
        self.units = int(units)
        self.platoon_class = self.get_platoon_class()

    def __str__(self):
        return f"{self.unit_class}#{self.units}"

    def get_platoon_class(self):
        """
        Factory method to create platoon instances based on their class names.
        """
        return self.PLATOON_CLASSES.get(self.unit_class, BasePlatoon)()

class Army:
    """Represents an army consisting of multiple platoons."""
    def __init__(self, platoons_str):
        self.platoons = self._parse_platoons(platoons_str)

    def _parse_platoons(self, platoons_str):
        """Parses the platoon string into a list of Platoon objects."""
        platoons = []
        for part in platoons_str.strip().split(';'):
            try:
                name, count = part.split('#')
                platoons.append(Platoon(name, count))
            except Exception as e:
                print(f"Warning: Skipping malformed platoon string: {part}, {e}")
                continue
        return platoons

class BasePlatoon:
    def __init__(self):
         self.advantage_over_list = []

class PlatoonMilitia(BasePlatoon):
     def __init__(self):
         self.advantage_over_list = ['Spearmen', 'LightCavalry']

class PlatoonSpearmen(BasePlatoon):
     def __init__(self):
         self.advantage_over_list = ['LightCavalry', 'HeavyCavalry']

class PlatoonLightCavalry(BasePlatoon):
     def __init__(self):
         self.advantage_over_list = ['FootArcher', 'CavalryArcher']

class PlatoonHeavyCavalry(BasePlatoon):
     def __init__(self):
         self.advantage_over_list = ['Militia', 'FootArcher', 'LightCavalry']

class PlatoonCavalryArcher(BasePlatoon):
     def __init__(self):
         self.advantage_over_list =  ['Spearmen', 'HeavyCavalry']

class PlatoonFootArcher(BasePlatoon):
     def __init__(self):
         self.advantage_over_list = ['Militia', 'CavalryArcher']

class Terrain:
    TERRAIN_CLASSES = {
        'Default': lambda: Terrain(),
        'Hill': lambda: Hill(),
        'Plains': lambda: Plains(),
        'Muddy': lambda: Muddy(),
    }

    def get_effective_count(self, platoon):
        return platoon.units

    @classmethod
    def get_terrains_class(cls, terrain_name):
        """
        Factory method to create terrain instances based on their names.
        """
        if terrain_name in cls.TERRAIN_CLASSES:
            return cls.TERRAIN_CLASSES[terrain_name]()
        else:
            raise ValueError(f"Invalid terrain type: {terrain_name}")

    @classmethod
    def parse_terrains(cls, terrains_str):
        terrains = []
        for part in terrains_str.strip().split(';'):
            try:
                terrains.append(cls.get_terrains_class(part))
            except ValueError as e:
                print(e)
                continue
        return terrains

class Hill(Terrain):
    def get_effective_count(self, platoon):
        if platoon.unit_class in ['CavalryArcher', 'FootArcher']:
            return platoon.units* 2 
        elif platoon.unit_class in ['Militia', 'HeavyCavalry', 'LightCavalry', 'Spearmen']:
            return platoon.units* 0.5
        return platoon.units

class Plains(Terrain):
    def get_effective_count(self, platoon):
        if platoon.unit_class in ['CavalryArcher', 'HeavyCavalry', 'LightCavalry']:
            return platoon.units* 2
        return platoon.units

class Muddy(Terrain):
    def get_effective_count(self, platoon):
        if platoon.unit_class in ['FootArcher', 'Militia', 'Spearmen']:
            return platoon.units* 2
        return platoon.units

class Battle:
    def __init__(self, my_army, opponent_army, terrains):
        self.my_army = my_army
        self.opponent_army = opponent_army
        self.terrains = terrains

    def _can_win_engagement(self, my_platoon, opponent_platoon, terrain):
        my_effective_units = terrain.get_effective_count(my_platoon)
        opponent_effective_units = terrain.get_effective_count(opponent_platoon)
        print(f"{terrain} {my_platoon} {opponent_platoon} {my_effective_units} {opponent_effective_units}")

        if opponent_platoon.unit_class in my_platoon.platoon_class.advantage_over_list:
            return my_effective_units * 2 > opponent_effective_units
        elif my_platoon.unit_class in opponent_platoon.platoon_class.advantage_over_list:
            return my_effective_units > opponent_effective_units * 2
        else:
            return my_effective_units > opponent_effective_units

    def find_winning_arrangement(self):
        if len(self.my_army.platoons) != len(self.opponent_army.platoons):
            return "Armies must have the same number of platoons."

        for arrangement in itertools.permutations(self.my_army.platoons):
            wins = 0
            for i in range(len(arrangement)):
                if self._can_win_engagement(arrangement[i], self.opponent_army.platoons[i], self.terrains[i]):
                    wins += 1
            if wins >= 3:
                return ";".join(map(str, arrangement))

        return "No winning arrangement found."

def main():
    my_platoons_str = input("Enter your platoons")
    opponent_platoons_str = input("Enter opponent's platoons")
    terrains_str = input("Enter terrains")
    if not my_platoons_str:
        my_platoons_str = "Militia#100;Spearmen#100;LightCavalry#100;HeavyCavalry#100;FootArcher#100"
    if not opponent_platoons_str:
        opponent_platoons_str = "Militia#99;Spearmen#100;LightCavalry#100;HeavyCavalry#100;FootArcher#100"
    if not terrains_str:
        terrains_str = 'Muddy;Default;Default;Default;Default'

    my_army = Army(my_platoons_str)
    opponent_army = Army(opponent_platoons_str)
    terrains = Terrain.parse_terrains(terrains_str)

    battle = Battle(my_army, opponent_army, terrains)
    result = battle.find_winning_arrangement()
    print(result)

if __name__ == "__main__":
    main()
