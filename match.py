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
    #Ace + 10 value on the deal
    BLACKJACK = 4
    # 9 + 10
    DEALER_PEAK = 5
    WIN = 6
    LOSE = 7
    BUST = 8
    TIE = 9



class Entity:
    def __init__(self, hand_limit: int = None):
        if hand_limit:
            self.hand: Hand = Hand.create_hand(hand_limit)
        else:
            self.hand: Hand = Hand.create_hand(hand_limit)
        self.soft_score = 0
        self.hard_score = 0
    
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
            self.update_score((low_total,total))
            return (low_total,total)
        
        else:
            total += sum(Value[card.rank].value for card in self.hand.cards)
            self.update_score(total)
            return total
    
    def update_score(self, score):
        
        if isinstance(score, tuple):
            self.soft_score = score[0]
            self.hard_score = score[1]
        else:
            self.hard_score = score

    def get_max_valid_score(self):
        if self.hard_score == 21 or self.soft_score == 21:
            return 21
        elif self.hard_score > 21:
            return self.soft_score
        else:
            return max(self.hard_score, self.soft_score)

    def get_soft_score(self) -> int:
        return self.soft_score
    
    def get_hard_score(self) -> int:
        return self.hard_score



class Player(Entity): 
    def __init__(self, hand_limit: int = None):
        super().__init__(hand_limit)
    def __str__(self):
        return (f"The player has {self.hand.hand_size}")
    
    

class Dealer(Entity): 
    def __init__(self, hand_limit: int = None):
        super().__init__(hand_limit)
        self.up_card = None
        self.hole_card = None
    def __str__(self):
        return (f"The Dealer has {self.hand.hand_size}")
    #must hit if score below 16, dealer hits on soft 17, stop at hard 17
    def hard17(self, deck: Deck):
        self.update_score(self.hand_score())
        if self.get_hard_score() == 21:
            return
        while self.hard_score < 17 or (self.soft_score < 17 and self.soft_score != 0):
            self.hand.add_card(deck.deal_card(True))
            self.update_score(self.hand_score())
    def get_up_card(self):
        if len(self.hand.cards != 0):
            return self.hand.cards[0]



class BlackJack:

    def __init__(self):
        pass
    def run_game():
        curr_state = States(1).name
        deck = Deck.create_deck()
        
        game_over = False
        player = Player()
        dealer = Dealer()
        # BlackJack.deal_state(deck, curr_state, player, dealer)
        while not game_over:

            match curr_state:
                case "DEAL":
                    curr_state = BlackJack.deal_state(deck, player, dealer)
                case "BLACKJACK":
                    print("glizzymaxx")
                    game_over = True

                case "PLAYER":
                    curr_state = BlackJack.player_state(deck, player)
                
                case "BUST":
                    print("Womp womp, there goes the kid's college fund..")
                    print(player.hand)
                    game_over = True

                case "DEALER_PEAK":
                    print("ONE MORE ROUND CANT HURT")
                    game_over = True

                case "ROUNDOVER":
                    curr_state = BlackJack.roundover_state(player, dealer, deck)
                    
                case "WIN":
                    print("TIME TO GET SOME BEER")
                    game_over = True

                case "LOSE":
                    print("TRY AGAIN, NERD!")
                    game_over = True
                
                case "Tie":
                    print("It's always been rigged..")



    def deal_state(deck: Deck, player: Player, dealer: Dealer):
        player.hand.add_card(deck.deal_card(True))
        dealer.hand.add_card(deck.deal_card(True))
        player.hand.add_card(deck.deal_card(True))
        dealer.hand.add_card(deck.deal_card(True))

        player.update_score(player.hand_score())
        if player.soft_score == 21 or player.hard_score == 21:
            print(player.hand)
            return States(4).name
        natural_ranks = ("QUEEN", "JACK", "KING", "TEN")
        
        dealer.update_score(dealer.hand_score())
        #ncheck for natural hit
        # if player_card1.rank == "ACE" or player_card2.rank == "ACE":
        #     if player_card1.rank in natural_ranks and player_card2.rank in natural_ranks:
        #         player.hand.add_card(player_card1)
        #         player.hand.add_card(player_card2)
        #         print(player.hand)
        #         return States(4).name
        
        # player.hand.add_card(player_card1)
        # player.hand.add_card(player_card2)
        return States(2).name

    
    #player can hit, stand, double down(later), 
    def player_state(deck: Deck, player: Player):
        print("Enter the following:")
        print("H to hit, D for double down, S for stand")
        end_turn = False

        while not end_turn:
            print(player.hand)
            user_input = input()
            match user_input.upper():
                case "H":
                    player.hand.add_card(deck.deal_card(True))
                    player.update_score(player.hand_score())

                    if player.hard_score == 21 or player.soft_score == 21:
                        print(player.hand)
                        return States(3).name
                    if player.hard_score > 21 and player.soft_score > 21:
                        return States(8).name
                    elif player.hard_score > 21 and player.soft_score == 0:
                        return States(8).name
                    
                case "S":
                    player.update_score(player.hand_score())
                    return States(3).name
                
                case "D":
                    print("Not yet implemented")


                    
    def roundover_state(player: Player, dealer: Dealer, deck: Deck):
        print(f"Dealer: {dealer.hand}")
        dealer.hard17(deck)
        player_final_score = player.get_max_valid_score()
        dealer_final_score = dealer.get_max_valid_score()
        if player_final_score > dealer_final_score:
            curr_state = States(6).name
        elif player_final_score < dealer_final_score:
            curr_state = States(7).name
        else:
            curr_state = States(9).name
        print(f"Dealer: {dealer.hand} and final score {dealer_final_score}")
        print(f"Final score: {player_final_score} Player {player.hand}")
        return curr_state


    #player hits a blackjack, now we calculate it
    def blackjack_state(self, deck: Deck, player: Player, dealer: Dealer) -> str:
        x=5


    


# player = Player(4)
# player.hand.add_card(ace_of_spaces)
# player.hand.add_card(king_of_heart)
# print(player.hand_score())
# card = Card(2, 2)
# player.hand.add_card(card)
# print(player.hand.hand_size)
# print(player)


BlackJack.run_game()
