import numpy as np
import pandas as pd
import random


def print_separator(title=None):
    print(f"\n{'=' * 10} {title} {'=' * 10}\n")


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
    print_separator(f"{player_name}'s Turn")
    dice_values = np.random.randint(1, 7, size=5)
    print(f"Initial roll: {dice_values}")

    for attempt in range(2):
        reroll_input = input("Enter the indices of dice to reroll (0-4), separate by spaces, or press enter to keep: ")

        if reroll_input.strip() == '':
            break

        reroll_indices = [int(index) for index in reroll_input.split() if index.isdigit() and 0 <= int(index) < 5]

        if len(reroll_indices) != len(reroll_input.split()):
            print("Invalid choice detected. Please enter indices between 0 and 4 only.")
            continue

        dice_values = roll_dices(dice_values, np.array(reroll_indices))
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
    print_separator("Welcome to a different kind of Yatzy!")
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

    rounds = list(range(1, 7)) + ['Yatzy']
    for i, round_num in enumerate(rounds):
        if round_num == 'Yatzy':
            round_display = "Final Round!"
        else:
            round_display = f"Round {round_num}"
        print_separator(round_display)
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
        "\n🌟 The stars aligned for you, {winner}! With {score} points, you've danced through the dice storm and emerged as the undisputed Yatzy Emperor. Long may you roll! 🌟",
        "\n🚀 {winner}, you've rocketed past the competition and landed squarely in the winner's circle with {score} points! Your dice-rolling skills are truly out of this world. 🚀",
        "\n🎩 Hats off to you, {winner}! With a magical score of {score} points, you've proven that luck is just skill in disguise. The wizardry of dice bends to your will! 🎩",
        "\n🏰 Against all odds, {winner} has stormed the castle and seized the throne with {score} points! All hail the new ruler of Yatzy Kingdom, where dice rule the land! 🏰",
        "\n🍀 {winner}, it's not just luck—it's legend. With {score} points, you've rolled your way into the annals of Yatzy history. Let's carve your name on the high score tablet! 🍀",
        "\n🎉 Confetti and cheers for {winner}, the Yatzy Maestro with {score} points! Your symphony of dice has played the sweetest victory tune. Encore! 🎉",
        "\n🔥 {winner}, you've set the game ablaze with your fiery score of {score} points! Like a phoenix, you've risen from the ashes of chance to claim your victory. 🔥",
        "\n🌈 {winner}, you've captured the pot of gold at the end of the rainbow with {score} points! In the realm of Yatzy, you're the leprechaun that outsmarted luck itself. 🌈",
        "\n⚔️ In the epic saga of dice, {winner} has emerged as the hero of legend with {score} points! Your tale will be told across the lands, inspiring future generations of rollers. ⚔️",
        "\n🕵️‍♂️ Mystery solved, {winner}! With {score} points, you've uncovered the secret to ultimate Yatzy mastery. The game's afoot, and you're the detective who cracked the code! 🕵️‍♂️"
    ]

    if len(winners) > 1:
        winners_text = ", ".join(winners[:-1]) + " and " + winners[-1]
        tie_message = f"\nIt's a tie! Congratulations to {winners_text} for scoring {max_score} points!"
        print(tie_message)
    else:
        selected_message = random.choice(congratulations_messages).format(winner=winners[0], score=max_score)
        print(selected_message)


game()
