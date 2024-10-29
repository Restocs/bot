import os
import importlib.util
from tkinter import Tk, filedialog

# Constants
ROCK = 1
PAPER = 2
SCISSORS = 3
MAX_SETS = 40
WINS_PER_SET = 31
MAX_ROUNDS_PER_SET = (WINS_PER_SET - 1) * 2
MAX_CONSECUTIVE_DRAWS = 10

BOT1_FILE = "KNBmodUP.py"
BOT2_FILE = "bot.py"

# Determine the winner of a round
def determine_winner(choice1, choice2):
    if choice1 == choice2:
        return 'Draw'
    
    if (choice1 == ROCK and choice2 == SCISSORS) or (choice1 == SCISSORS and choice2 == PAPER) or (choice1 == PAPER and choice2 == ROCK):
        return 'Bot1'
    
    return 'Bot2'

# Print the final results
def print_results(bot1_set_wins, bot2_set_wins):
    print('--- Game Results ---')
    print('Bot1 Set Wins:', bot1_set_wins)
    print('Bot2 Set Wins:', bot2_set_wins)
    if bot1_set_wins > bot2_set_wins:
        print('Bot1 is the overall winner!')
    elif bot2_set_wins > bot1_set_wins:
        print('Bot2 is the overall winner!')
    else:
        print("It's a tie overall!")

# Main game loop
def play_game(bot1, bot2):
    bot1_set_wins = 0
    bot2_set_wins = 0

    bot1.on_game_start()
    bot2.on_game_start()

    prev_bot1_choice = 0
    prev_bot2_choice = 0

    for set_number in range(1, MAX_SETS + 1):
        # print(f'--- Set {set_number} ---')
        bot1_points = 0
        bot2_points = 0
        bot1_wins = 0
        bot2_wins = 0
        consecutive_draws = 0
        round_number = 0

        while bot1_wins < WINS_PER_SET and bot2_wins < WINS_PER_SET and round_number < MAX_ROUNDS_PER_SET:
            round_number += 1
            # print(f'--- Round {round_number} ---')

            bot1_choice = bot1.choose(prev_bot2_choice)
            bot2_choice = bot2.choose(prev_bot1_choice)

            prev_bot1_choice = bot1_choice
            prev_bot2_choice = bot2_choice

            # Check for valid moves
            if bot1_choice not in [ROCK, PAPER, SCISSORS]:
                print(f'Error: Bot1 made an invalid choice: {bot1_choice}')
                break
            if bot2_choice not in [ROCK, PAPER, SCISSORS]:
                print(f'Error: Bot2 made an invalid choice: {bot2_choice}')
                break

            # print('Bot1 chose:', bot1_choice)
            # print('Bot2 chose:', bot2_choice)

            # Determine the winner of the round
            result = determine_winner(bot1_choice, bot2_choice)

            if result == 'Bot1':
                # print('Bot1 wins the round!')
                bot1_points += 3
                bot1_wins += 1
                consecutive_draws = 0
            elif result == 'Bot2':
                # print('Bot2 wins the round!')
                bot2_points += 3
                bot2_wins += 1
                consecutive_draws = 0
            else:
                # print("It's a draw!")
                bot1_points += 1
                bot2_points += 1
                consecutive_draws += 1

                if consecutive_draws == MAX_CONSECUTIVE_DRAWS:
                    # print('10 draws in a row! The set is a draw!')
                    break

            # print(f'Current Score: Bot1 Points - {bot1_points}, Bot2 Points - {bot2_points}')

            # Determine the winner of the set
            if consecutive_draws == MAX_CONSECUTIVE_DRAWS or (round_number == MAX_ROUNDS_PER_SET and bot1_wins == bot2_wins):
                # print(f'Set {set_number} ends in a draw!')
                bot1_set_wins += 1
                bot2_set_wins += 1
            elif bot1_wins >= WINS_PER_SET:
                # print(f'Bot1 wins Set {set_number} by rounds!')
                bot1_set_wins += 1
            elif bot2_wins >= WINS_PER_SET:
                # print(f'Bot2 wins Set {set_number} by rounds!')
                bot2_set_wins += 1
            elif round_number == MAX_ROUNDS_PER_SET:
                if bot1_points > bot2_points:
                    # print(f'Bot1 wins Set {set_number} by points!')
                    bot1_set_wins += 1
                elif bot2_points > bot1_points:
                    # print(f'Bot2 wins Set {set_number} by points!')
                    bot2_set_wins += 1
                else:
                    # print(f'Set {set_number} ends in a draw by points!')
                    bot1_set_wins += 1
                    bot2_set_wins += 1


    print_results(bot1_set_wins, bot2_set_wins)

    bot1.on_game_end()
    bot2.on_game_end()

# Function to load the bot from a .py file
def load_bot(file_path):
    spec = importlib.util.spec_from_file_location("Bot", file_path)
    bot_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bot_module)
    return bot_module.Bot()

# GUI for file selection
def select_files():
    root = Tk()
    root.withdraw()  # Hide the main window

    bot1_file = BOT1_FILE
    if not bot1_file:
        print("Bot 1 file not selected. Exiting.")
        return

    bot2_file = BOT2_FILE
    if not bot2_file:
        print("Bot 2 file not selected. Exiting.")
        return

    return bot1_file, bot2_file

# Start the game
if __name__ == "__main__":
    bot_files = select_files()
    if bot_files:
        bot1_path, bot2_path = bot_files
        bot1 = load_bot(bot1_path)
        bot2 = load_bot(bot2_path)
        play_game(bot1, bot2)
