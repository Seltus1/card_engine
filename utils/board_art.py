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
    print("##########################")
    tprint("Player's Hand", font="small")
    print(player.hand)

def print_final_board(player: Player, dealer: Dealer):
    tprint("Dealer's Hand", font="small")
    print(dealer.get_up_card())
    print("##########################")
    tprint("Player's Hand", font="small")
    print(player.hand)

def text2asci(text: str, font: str):
    return text2art(text, font)

def final_print(state: States):
        os.system('clear')
        console.print(Text(text2art(state.value, "xhelvi"), justify="center"))
        match state:
            case States.LOSE | States.BUST:
                console.print(Text(ascii_lose, style="red"))
            case States.WIN | States.BLACKJACK:
                console.print(Text(ascii_win, style="green"))
            case States.TIE:
                console.print(Text(text2art(States.TIE.value, font="block"), style="blue"))     
