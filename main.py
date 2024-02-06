# Importerar bibliotek, numpy för numeriska operationer, pandas för datahantering och random för slumpmässiga val.
import numpy as np
import pandas as pd
import random


# Funktion för att skriva ut en seperator för att få det visuellt snyggare.
def print_separator(title=None):
    # Skriver ut separatorn med titeln centrerad, placerad mellan 10 st = på var sida.
    print(f"\n{'=' * 10} {title} {'=' * 10}\n")


# Funktion för att slå om tärningarna.
def roll_dices(dice_values, reroll_indices):
    # Uppdaterar värdena för de tärningarna som ska slås om
    dice_values[reroll_indices] = np.random.randint(1, 7, size=len(reroll_indices))
    # Returnerar den nya listan med tärningsvärden.
    return dice_values


# Funktion för att räkna ut rundans poäng.
def calculate_round_score(dice_values, target_number):
    # Kontrollerar om spelaren har fått yatzy, och i sådana fall returnerar 50 poäng.
    if target_number == 'Yatzy' and np.all(dice_values == dice_values[0]):
        return 50
    # Beräknar och returnerar poängen baserat på målnumret och att det inte änr yatzy.
    elif target_number != 'Yatzy':
        return np.sum(dice_values == target_number) * target_number
    # Returnerar noll poäng om inget av de ovanstående stämmer.
    return 0


# Funktion för en spelares runda.
def player_round(player_name, used_categories):
    # Skriver ut spelarens tur med namn.
    print_separator(f"{player_name}'s Turn")
    # Slår fem tärningar med värde 1-6.
    dice_values = np.random.randint(1, 7, size=5)
    # Visar värdet för de fem tärningarna.
    print(f"Initial roll: {dice_values}")

    # Låter spelaren slå om tärningar upp till två gånger.
    for attempt in range(2):
        # Spelaren få ange index på de tärningarna de vill slå om.
        reroll_input = input("Enter the indices of dice to reroll (0-4), separate by spaces, or press enter to keep: ")

        # Om spelaren trycker på enter så går spelet vidare.
        if reroll_input.strip() == '':
            break

        # Skapar en lista med index för de tärningarna som ska slås om.
        reroll_indices = [int(index) for index in reroll_input.split() if index.isdigit() and 0 <= int(index) < 5]

        # Kontrollerar om alla angivna index är giltiga.
        if len(reroll_indices) != len(reroll_input.split()):
            # Felmeddelande om det angetts något annat än de index (0-4) som går att välja på.
            print("Invalid choice detected. Please enter indices between 0 and 4 only.")
            continue

        # Slår om de valda tärningarna.
        dice_values = roll_dices(dice_values, np.array(reroll_indices))
        # Visar det nya resultatet.
        print(f"New roll: {dice_values}")

    # Kontrollerar om spelaren fått yatzy.
    if np.all(dice_values == dice_values[0]):
        # Skriver ut att spelaren fått yatzy.
        print("🎲 Yatzy Explosion! Pure Dice Domination!")
        # Returnerar 50 poäng till yatzy-kategorin.
        return 50, 'Yatzy'

    # Kontrollerar om antalet använda kategorier än mindre än 6.
    if len(used_categories) < 6:
        # Om det finns kategorier kvar att välja, så fortsätter den.
        while True:
            try:
                # Ber spelaren att välja en kategori mellan 1 och 6.
                target_number = int(input("Choose your scoring category (1-6): "))
                # Kontrollerar om den valda kategorin redan har valts.
                if target_number in used_categories:
                    # Meddelar spelaren att kategorin redan använts, och ber den att välja en annan.
                    print("You already used that category. Please choose a different category.")
                # Kontrollerar om den angivna valet är tillåtet (mellan 1 och 6).
                elif 1 <= target_number <= 6:
                    # Bryter loopen om det är ett giltigt val.
                    break
                else:
                    # Meddelar spelaren om att välja ett nummer inom det giltiga intervallet om valet ligger utanför.
                    print("Please choose a valid category between 1 and 6.")
            # Hanterar fall där inmatningen inte är ett heltal.
            except ValueError:
                # Meddelar spelaren om att den måste ange ett nummer.
                print("Invalid input. Please enter a number.")
    else:
        # Om alla kategorier redan använts, så vals yatzy som sista kategorin.
        target_number = 'Yatzy'

    # Beräknar och returnerar poängen för rundan baserat på vald kategori.
    round_score = calculate_round_score(dice_values, target_number)
    return round_score, target_number


# Huvudfunktionen för spelet.
def game():
    # Välkomstmeddelande, använder sig av separatorn för att det ska se snyggare ut.
    print_separator("Welcome to a different kind of Yatzy!")
    while True:
        try:
            # Frågar efter antalet spelare, mellan 1 och 10.
            num_players = int(input("Enter the number of players (1-10): "))
            if 1 <= num_players <= 10:
                # Bryter loopen om det angivna talet är mellan 1 och 10.
                break
            else:
                # Ber en skriva ett tal mellan 1 och 10 om det angivna är utanför det giltiga intervallet.
                print("Please enter a number between 1 and 10.")
        # Hanterar fall där inmatningen inte är ett heltal.
        except ValueError:
            # Meddelar spelaren om att den måste ange ett nummer.
            print("Please enter a valid number.")

    # Skapar en lista med spelarnamn baserat på antal spelare.
    player_names = [input(f"Enter Player {i + 1}'s name: ") for i in range(num_players)]
    # Gör en dataframe för att hålla reda på poängen, spelarnamn som kolumner och rundorna som rader.
    scores = pd.DataFrame(columns=player_names, index=list(range(1, 7)) + ['Yatzy'])
    scores.index.name = "Round"
    # Skapar en dictionary för att hålla reda på vilka kategorier varje spelare redan har använt.
    used_categories = {player: [] for player in player_names}

    # Skapar en lista med rundor, inklusive den sista rundan "yatzy".
    rounds = list(range(1, 7)) + ['Yatzy']
    for i, round_num in enumerate(rounds):
        # Om det är rundan för yatzy --
        if round_num == 'Yatzy':
            # -- så skrivs det ut som "Final Round". (Fick döpa om det från yatzy round med tanke på att man redan kan ha fått yatzy och då ska ha något annat)
            round_display = "Final Round!"
        else:
            # anger vilken runda det spelas.
            round_display = f"Round {round_num}"
        # Skriver ut vilken runda det är med hjälp av separatorn för att göra det lite snyggare.
        print_separator(round_display)
        # Går igenom samtliga spelare.
        for player_name in player_names:
            # Kallar på funktionen player_round för att spela rundan och returnerar poäng samt vald kategori.
            round_score, target_number = player_round(player_name, used_categories[player_name])
            # Kontrollerar om spelaren fick Yatzy och 50 poäng.
            if target_number == 'Yatzy' and round_score == 50:
                scores.loc['Yatzy', player_name] = 50
            else:
                # Om en annan kategori än Yatzy valdes, läggs den till i listan över använda kategorier.
                if target_number != 'Yatzy':
                    used_categories[player_name].append(target_number)
                scores.loc[target_number, player_name] = round_score

    # Skriver ut den slutgiltiga poängtavlan --
    print("\n\nFinal Scoreboard:")
    # -- med resultaten för varje runda.
    print(scores)
    # Beräknar totalpoängen för varje spelare.
    total_scores = scores.sum()
    # Skriver ut totalpoängen för varje spelare.
    print("\nTotal Scores:")
    # Konverterar poängen till en sträng, så det blir enklare att läsa, samt snyggare presenterat.
    print(total_scores.to_string())

    # Räknar ut vem som vunnit, baserat på högsta poängen.
    max_score = total_scores.max()
    # Skapar en lista av spelarnamn som har uppnått det högsta poängvärdet, vilket kan inkludera flera spelare vid oavgjort.
    winners = total_scores[total_scores == max_score].index.tolist()

    # Olika gratulationsmeddelanden.
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

    # Hanterar oavgjort resultat.
    if len(winners) > 1:
        # Text där alla som vunnit är inkluderade med namn och resultat.
        winners_text = ", ".join(winners[:-1]) + " and " + winners[-1]
        tie_message = f"\nIt's a tie! Congratulations to {winners_text} for scoring {max_score} points!"
        # Skriver ut gratulationsmeddelande för en oavgjord runda.
        print(tie_message)
    else:
        # Väljer slumpmässigt ett gratulationsmeddelande från en lista och formaterar det med namnet och poängen för den ensamma vinnaren.
        selected_message = random.choice(congratulations_messages).format(winner=winners[0], score=max_score)
        # Skriver ut det valda gratulationsmeddelandet till konsolen.
        print(selected_message)


game()
