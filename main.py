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
    player1_name = input("Enter Player 1's name: ")
    player2_name = input("Enter Player 2's name: ")
    scores = pd.DataFrame(columns=[player1_name, player2_name], index=range(1, 7))
    scores.index.name = "Round"

    for round_num in range(1, 7):
        scores.loc[round_num, player1_name] = player_round(player1_name, round_num)
        scores.loc[round_num, player2_name] = player_round(player2_name, round_num)

    print("\nFinal Scoreboard:")
    print(scores)
    print("\nTotal Scores:")
    print(scores.sum().to_string())


game()
