import itertools

class Platoon:
    """Represents a single platoon with a specific class and number of units."""
    def __init__(self, unit_class, units):
        self.unit_class = unit_class
        self.units = int(units)

    def __str__(self):
        return f"{self.unit_class}#{self.units}"

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
            except ValueError:
                print(f"Warning: Skipping malformed platoon string: {part}")
                continue
        return platoons

class Battle:
    """Manages a battle between two armies and determines the outcome."""
    _advantages = {
        'Militia': ['Spearmen', 'LightCavalry'],
        'Spearmen': ['LightCavalry', 'HeavyCavalry'],
        'LightCavalry': ['FootArcher', 'CavalryArcher'],
        'HeavyCavalry': ['Militia', 'FootArcher', 'LightCavalry'],
        'CavalryArcher': ['Spearmen', 'HeavyCavalry'],
        'FootArcher': ['Militia', 'CavalryArcher']
    }

    def __init__(self, my_army, opponent_army):
        self.my_army = my_army
        self.opponent_army = opponent_army

    def _can_win_engagement(self, my_platoon, opponent_platoon):
        """
        Determines if my_platoon wins against opponent_platoon based on advantages.
        A platoon with an advantage can handle twice the number of opponents.
        """
        # Check if my platoon has an advantage
        if opponent_platoon.unit_class in self._advantages.get(my_platoon.unit_class, []):
            return my_platoon.units * 2 > opponent_platoon.units
        # Check if opponent has an advantage
        elif my_platoon.unit_class in self._advantages.get(opponent_platoon.unit_class, []):
            return my_platoon.units > opponent_platoon.units * 2
        # No advantage on either side
        else:
            return my_platoon.units > opponent_platoon.units

    def find_winning_arrangement(self):
        """
        Finds a permutation of my army's platoons that wins at least 3 out of 5 battles.
        """
        # Iterate through all possible arrangements of my platoons
        for arrangement in itertools.permutations(self.my_army.platoons):
            wins = 0
            # Match each of my platoons against the opponent's platoons
            for i in range(len(arrangement)):
                if self._can_win_engagement(arrangement[i], self.opponent_army.platoons[i]):
                    wins += 1

            # If we have 3 or more wins, we've found a solution
            if wins >= 3:
                return ";".join(map(str, arrangement))

        # No winning arrangement was found
        return "There is no chance of winning"

def main():
    """
    Main function to run the Age of War solver.
    It reads platoon data from stdin, uses the OOP model to find a solution,
    and prints the result.
    """
    try:
        # Read the platoon data for both sides from standard input
        my_platoons_str = input()
        opponent_platoons_str = input()

        if not my_platoons_str:
            my_platoons_str = "Militia#100;Spearmen#100;LightCavalry#100;HeavyCavalry#100;FootArcher#100"
        if not opponent_platoons_str:
            opponent_platoons_str = "Militia#100;Spearmen#100;LightCavalry#100;HeavyCavalry#100;FootArcher#100"

        my_army = Army(my_platoons_str)
        opponent_army = Army(opponent_platoons_str)

        battle = Battle(my_army, opponent_army)
        solution = battle.find_winning_arrangement()
        print(solution)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
