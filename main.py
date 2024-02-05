import numpy as np
import pandas as pd


def roll_dices(dice_values, reroll_indices):
    dice_values[reroll_indices] = np.random.randint(1, 7, size=len(reroll_indices))
    return dice_values


def calculate_round_score(dice_values, target_number):
    if np.all(dice_values == dice_values[0]):
        return 50
    else:
        return np.sum(dice_values == target_number) * target_number


def player_round(player_name, round_number):
    dice_values = np.random.randint(1, 7, size=5)
    print(f"{player_name}'s turn, Round {round_number}, focusing on {round_number}'s. Initial roll: {dice_values}")

    if np.all(dice_values == dice_values[0]):
        print("Yatzy! 50 points!")
        return 50

    for attempt in range(2):
        reroll_input = input("Enter the indices of dice to reroll (0-4), seperate by spaces, or press enter to keep: ")
        if reroll_input.strip() == '':
            break
        reroll_indices = np.array([int(index) for index in reroll_input.split() if index.isdigit() and 0 <= int(index) < 5])
        dice_values = roll_dices(dice_values, reroll_indices)
        print(f"New roll: {dice_values}")

        if np.all(dice_values == dice_values[0]):
            print("Yatzy! 50 points!")
            return 50

    round_score = calculate_round_score(dice_values, round_number)
    return round_score


def game():
    num_players = int(input("Enter the number of players: "))
    player_names = [input(f"Enter Player {i + 1}'s name: ") for i in range(num_players)]
    scores = pd.DataFrame(columns=player_names, index=range(1, 7))
    scores.index.name = "Round"

    for round_num in range(1, 7):
        for player_name in player_names:
            scores.loc[round_num, player_name] = player_round(player_name, round_num)

    print("\nFinal Scoreboard:")
    print(scores)
    print("\nTotal Scores:")
    print(scores.sum().to_string())


game()
