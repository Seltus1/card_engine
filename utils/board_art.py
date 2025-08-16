from art import text2art, tprint
from models.enums import States
from rich.console import Console
from rich.text import Text
from entities.dealer import Dealer
from entities.player import Player
import os

console = Console()
ascii_win = """
 .----------------.  .----------------.  .-----------------. .-----------------. .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| | _____  _____ | || |     _____    | || | ____  _____  | || | ____  _____  | || |  _________   | || |  _______     | |
| ||_   _||_   _|| || |    |_   _|   | || ||_   \|_   _| | || ||_   \|_   _| | || | |_   ___  |  | || | |_   __ \    | |
| |  | | /\ | |  | || |      | |     | || |  |   \ | |   | || |  |   \ | |   | || |   | |_  \_|  | || |   | |__) |   | |
| |  | |/  \| |  | || |      | |     | || |  | |\ \| |   | || |  | |\ \| |   | || |   |  _|  _   | || |   |  __ /    | |
| |  |   /\   |  | || |     _| |_    | || | _| |_\   |_  | || | _| |_\   |_  | || |  _| |___/ |  | || |  _| |  \ \_  | |
| |  |__/  \__|  | || |    |_____|   | || ||_____|\____| | || ||_____|\____| | || | |_________|  | || | |____| |___| | |
| |              | || |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 
"""

ascii_lose = """
 .----------------.                      .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. |                    | .--------------. || .--------------. || .--------------. || .--------------. |
| |   _____      | |                    | |   ______     | || |     ____     | || |   ________   | || |     ____     | |
| |  |_   _|     | |                    | |  |_   _ \    | || |   .'    `.   | || |  |  __   _|  | || |   .'    `.   | |
| |    | |       | |                    | |    | |_) |   | || |  /  .--.  \  | || |  |_/  / /    | || |  /  .--.  \  | |
| |    | |   _   | |                    | |    |  __'.   | || |  | |    | |  | || |     .'.' _   | || |  | |    | |  | |
| |   _| |__/ |  | |                    | |   _| |__) |  | || |  \  `--'  /  | || |   _/ /__/ |  | || |  \  `--'  /  | |
| |  |________|  | |                    | |  |_______/   | || |   `.____.'   | || |  |________|  | || |   `.____.'   | |
| |              | |                    | |              | || |              | || |              | || |              | |
| '--------------' |                    | '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'                      '----------------'  '----------------'  '----------------'  '----------------' 
"""

def print_board(player: Player, dealer: Dealer, end_game: bool):
    tprint("Dealer's Hand", font="small")
    if end_game:
        print(dealer.hand)
    else:
        print(dealer.get_up_card())
    print("####################################################")
    tprint("Player's Hand", font="small")
    print(player.hand)


def print_choose_state(player: Player, dealer: Dealer):
    print(text2art(f"Dealer: {dealer.get_max_valid_score()}", "small"))
    print(text2art(f"Player: {player.get_max_valid_score()}", "small"))
    print()
    print()
    print(text2art("Are you tired of winning?", "small"))
    print()
    print(text2art("Q: quit", "small"))
    print(text2art("Enter: gamble more", "small"))

def print_blackjack_instructions():
    os.system("clear")
    print(text2art("Blackjack Instructions", "tarty2"))
    print(text2art("H to hit", "tarty2"))
    print(text2art("S to stand", "tarty2"))
    print(text2art("D to double down", "tarty2"))
    print(text2art("Press F to play", "tarty2"))

def text2asci(text: str, font: str):
    return text2art(text, font)

def final_print(state: States, player: Player, dealer: Dealer):
        os.system('clear')
        print_board(player, dealer, True)
        match state:
            case States.LOSE | States.BUST:
                console.print(Text(ascii_lose, style="red"))
                console.print(Text(text2art(state.value, "xhelvi"), justify="center"))
            case States.WIN | States.BLACKJACK:
                console.print(Text(ascii_win, style="green"))
                console.print(Text(text2art(state.value, "xhelvi"), justify="center"))
            case States.TIE:
                console.print(Text(text2art(state.value, "xhelvi"), style="blue"))
