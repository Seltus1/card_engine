from dataclasses import dataclass
from enum import Enum
from cards import Deck
class States(Enum):
    DEAL = 1
    PLAYER = 2
    GAMEOVER = 3
    WIN = 4


@dataclass
class BlackJack:
    @classmethod
    def run_game():
        curr_state = States(1).name
        deck = Deck.create_deck()

        game_over = False
        while not game_over:
            match States:
                case "DEAL":
                    x=5


    def deal_state(deck: Deck, curr_state: States):
        

print(type(States(1).name))