from dataclasses import dataclass
from enum import Enum
from cards import *
class States(Enum):
    DEAL = 1
    PLAYER = 2
    GAMEOVER = 3
    WIN = 4

class Player: 
    def __init__(self, hand_limit: int):
        self.hand = Hand.create_hand(hand_limit)
    
    def __str__(self):
        return (f"The player has {self.hand.hand_size}")
        

class Dealer: 
    def __init__(self, hand_limit: int):
        self.hand = Hand.create_hand(hand_limit)
    def __str__(self):
        return (f"The Dealer has {self.hand.hand_size}")
    
@dataclass
class BlackJack:
    def run_game():
        curr_state = States(1).name
        deck = Deck.create_deck()
        
        game_over = False
        player = Player(4)
        dealer = Dealer(4)
        BlackJack.deal_state(deck, curr_state, player, dealer)
        # while not game_over:
        #     match States:
        #         case "DEAL":
        #             x=5


    def deal_state(deck: Deck, curr_state: States, player: Player, dealer: Dealer):
        player.hand.add_card(deck.deal_card())
        player.hand.add_card(deck.deal_card())
        dealer.hand.add_card(deck.deal_card())
        dealer.hand.add_card(deck.deal_card())
        print(player.hand.hand_size)
        print(dealer.hand.hand_size)

# player = Player(4)
# card = Card(2, 2)
# player.hand.add_card(card)
# print(player.hand.hand_size)
# print(player)


BlackJack.run_game()
