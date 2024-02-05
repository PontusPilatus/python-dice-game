import numpy as np
import pandas as pd
import random


def roll_dices(dice_values, reroll_indices):
    dice_values[reroll_indices] = np.random.randint(1, 7, size=len(reroll_indices))
    return dice_values


def calculate_round_score(dice_values, target_number):
    if target_number == 'Yatzy' and np.all(dice_values == dice_values[0]):
        return 50
    elif target_number != 'Yatzy':
        return np.sum(dice_values == target_number) * target_number
    return 0


def player_round(player_name, used_categories):
    dice_values = np.random.randint(1, 7, size=5)
    print(f"{player_name}'s turn. Initial roll: {dice_values}")

    for attempt in range(2):
        reroll_input = input("Enter the indices of dice to reroll (0-4), separate by spaces, or press enter to keep: ")
        if reroll_input.strip() == '':
            break
        reroll_indices = np.array([int(index) for index in reroll_input.split() if index.isdigit() and 0 <= int(index) < 5])
        dice_values = roll_dices(dice_values, reroll_indices)
        print(f"New roll: {dice_values}")

    if np.all(dice_values == dice_values[0]):
        print("Yatzy! 50 points!")
        return 50, 'Yatzy'

    if len(used_categories) < 6:
        while True:
            try:
                target_number = int(input("Choose your scoring category (1-6): "))
                if target_number in used_categories:
                    print("You already used that category! Please choose a different category.")
                elif 1 <= target_number <= 6:
                    break
                else:
                    print("Please choose a valid category between 1 and 6.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    else:
        target_number = 'Yatzy'

    round_score = calculate_round_score(dice_values, target_number)
    return round_score, target_number


def game():
    while True:
        try:
            num_players = int(input("Enter the number of players (1-10): "))
            if 1 <= num_players <= 10:
                break
            else:
                print("Please enter a number between 1 and 10.")
        except ValueError:
            print("Please enter a valid number.")

    player_names = [input(f"Enter Player {i + 1}'s name: ") for i in range(num_players)]
    scores = pd.DataFrame(columns=player_names, index=list(range(1, 7)) + ['Yatzy'])
    scores.index.name = "Round"
    used_categories = {player: [] for player in player_names}

    for round_num in list(range(1, 7)) + ['Yatzy']:
        for player_name in player_names:
            round_score, target_number = player_round(player_name, used_categories[player_name])
            if target_number == 'Yatzy' and round_score == 50:
                scores.loc['Yatzy', player_name] = 50
            else:
                if target_number != 'Yatzy':
                    used_categories[player_name].append(target_number)
                scores.loc[target_number, player_name] = round_score

    print("\nFinal Scoreboard:")
    print(scores)
    total_scores = scores.sum()
    print("\nTotal Scores:")
    print(total_scores.to_string())

    max_score = total_scores.max()
    winners = total_scores[total_scores == max_score].index.tolist()

    congratulations_messages = [
        "Victory is yours, {winner}! With an impressive {score} points, you've triumphed over the odds. Well played!",
        "Bravo, {winner}! Your strategic prowess and luck have led you to victory with {score} points. The crown is well-deserved!",
        "Outstanding performance, {winner}! You've swept the board with {score} points. Your name will be remembered in the halls of fame!",
        "Is it skill? Is it luck? Who cares - {winner}, you're the champion with {score} points! Drinks are on you, right?",
        "In the grand arena of fate, {winner} emerged victorious with {score} points! Remember, in the game of dice, as in life, fortune favors the bold."
    ]

    if len(winners) > 1:
        winners_text = ", ".join(winners[:-1]) + " and " + winners[-1]
        tie_message = f"\nIt's a tie! Congratulations to {winners_text} for scoring {max_score} points!"
        print(tie_message)
    else:
        selected_message = random.choice(congratulations_messages).format(winner=winners[0], score=max_score)
        print(selected_message)


game()
