from games.blackjack import BlackJack
from utils.board_art import print_blackjack_instructions

if __name__ == "__main__":
    while True:
        print_blackjack_instructions()
        usr_input= input()
        if usr_input.lower() == "f":
            break
    BlackJack.run_game()
