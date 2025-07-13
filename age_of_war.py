import itertools

def solve_battle(my_platoons, opponent_platoons):
    """
    This function finds a winning arrangement of platoons.
    """
    advantages = {
        "Militia": ["Spearmen", "LightCavalry"],
        "Spearmen": ["LightCavalry", "HeavyCavalry"],
        "LightCavalry": ["FootArcher", "CavalryArcher"],
        "HeavyCavalry": ["Militia", "FootArcher", "LightCavalry"],
        "CavalryArcher": ["Spearmen", "HeavyCavalry"],
        "FootArcher": ["Militia", "CavalryArcher"]
    }

    my_platoons_list = []
    for platoon in my_platoons.split(';'):
        name, count = platoon.split('#')
        my_platoons_list.append({"name": name, "count": int(count)})

    opponent_platoons_list = []
    for platoon in opponent_platoons.split(';'):
        name, count = platoon.split('#')
        opponent_platoons_list.append({"name": name, "count": int(count)})

    for arrangement in itertools.permutations(my_platoons_list):
        wins = 0
        for i in range(5):
            my_platoon = arrangement[i]
            opponent_platoon = opponent_platoons_list[i]

            # Check for advantage
            if opponent_platoon["name"] in advantages.get(my_platoon["name"], []):
                if my_platoon["count"] * 2 > opponent_platoon["count"]:
                    wins += 1
            elif my_platoon["count"] > opponent_platoon["count"]:
                wins += 1
        
        if wins >= 3:
            return ";".join([f"{p['name']}#{p['count']}" for p in arrangement])

    return "There is no chance of winning"

if __name__ == "__main__":
    my_platoons_input = "Spearmen#10;Militia#30;FootArcher#20;LightCavalry#1000;HeavyCavalry#120"
    opponent_platoons_input = "Militia#10;Spearmen#10;FootArcher#1000;LightCavalry#120;CavalryArcher#100"
    
    result = solve_battle(my_platoons_input, opponent_platoons_input)
    print(result)
