from dataclasses import dataclass
from enum import Enum
from cards import *

ace_of_spaces = Card("SPADE", "ACE") 
king_of_heart = Card("HEART", "KING")


class Value(Enum):
    ACE = (1,11)
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 10
    QUEEN = 10
    KING = 10



class States(Enum):
    DEAL = 1
    PLAYER = 2
    #player stands
    ROUNDOVER = 3
    #Ace + 10 on the deal
    NATURAL_CHECK = 4
    #hitting black jack with hitting
    BLACKJACK = 5
    WIN = 6
    LOSE = 7
    BUST = 8



class Entity:
    def __init__(self, hand_limit: int):
        self.hand: Hand = Hand.create_hand(hand_limit)
    
    def hand_score(self) -> int:
        total = 0
        if self.hand.hand_size == 0:
            return total
        has_ace = self.hand.contains_rank("ACE")
        
        if has_ace:
            low_total = 0
            for card in self.hand.cards:
                if card.rank == "ACE":
                    ace_values = Value[card.rank].value
                    low_total += ace_values[0]
                    total += ace_values[1]
                    continue
                low_total += Value[card.rank].value
                total += Value[card.rank].value
            return (low_total,total)
        
        else:
            total += sum(Value[card.rank].value for card in self.hand.cards)
            return total



class Player(Entity): 
    def __init__(self, hand_limit: int):
        super().__init__(hand_limit)
    def __str__(self):
        return (f"The player has {self.hand.hand_size}")
    
    

class Dealer(Entity): 
    def __init__(self, hand_limit: int):
        super().__init__(hand_limit)
    def __str__(self):
        return (f"The Dealer has {self.hand.hand_size}")
    

class BlackJack:


    def __init__(self):
        pass
    def run_game():
        curr_state = States(1).name
        deck = Deck.create_deck()
        
        game_over = False
        player = Player(4)
        dealer = Dealer(4)
        # BlackJack.deal_state(deck, curr_state, player, dealer)
        while not game_over:
            match curr_state:
                case "DEAL":
                    curr_state = BlackJack.deal_state(deck, curr_state, player, dealer)
                case "NATURAL_CHECK":
                    print("glizzymaxx")
                    game_over = True

                case "PLAYER":
                    curr_state = BlackJack.player_state(deck, curr_state, player)
                
                case "LOSE":
                    print("A winner never quits...")
                    game_over = True

                case "BUST":
                    print("Womp womp, there goes the kid's college fund..")
                    game_over = True



    def deal_state(deck: Deck, curr_state: States, player: Player, dealer: Dealer):
        player_card1 = deck.deal_card(True)
        player_card2 = deck.deal_card(True)
        natural_ranks = ("ACE", "QUEEN", "JACK", "KING", "TEN")
        #ncheck for natural hit
        if player_card1.rank == "ACE" or player_card2.rank == "ACE":
            if player_card1.rank in natural_ranks and player_card2.rank in natural_ranks:
                curr_state = States(4).name
                return curr_state
        
        player.hand.add_card(player_card1)
        player.hand.add_card(player_card2)
        dealer.hand.add_card(deck.deal_card(True))
        dealer.hand.add_card(deck.deal_card(True))

        curr_state = States(2).name
        return curr_state

    
    #player can hit, stand, double down(later), 
    def player_state(deck: Deck, curr_state: str, player: Player):
        print("Enter the following:")
        print("H to hit, D for double down, S for stand")
        end_turn = False

        while not end_turn:
            
            user_input = input()
            match user_input.upper():
                case "H":
                    print("yep")
                    player.hand.add_card(deck.deal_card(True))
                    print(player.hand)
                    if player.hand_score == 21:
                        return States(5).name
                    if player.hand_score() > 21:
                        return States(8).name
                    
                case "S":
                    print("Done hitting it from the bacc")
                    return States(3).name
                
                case "D":
                    print("Not yet implemented")
                    


    


# player = Player(4)
# player.hand.add_card(ace_of_spaces)
# player.hand.add_card(king_of_heart)
# print(player.hand_score())
# card = Card(2, 2)
# player.hand.add_card(card)
# print(player.hand.hand_size)
# print(player)


BlackJack.run_game()
