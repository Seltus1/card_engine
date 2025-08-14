from models.enums import States
from models.cards import *
from entities.dealer import Dealer
from entities.player import Player

ace_of_spaces = Card("SPADE", "ACE") 
king_of_heart = Card("HEART", "KING")

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
                    print("glizzymaxx!!!")
                    game_over = True

                case "PLAYER":
                    curr_state = BlackJack.player_state(deck, player)
                
                case "BUST":
                    print("Womp womp, there goes the kid's college fund..")
                    print(player.hand)
                    game_over = True

                case "DEALER_PEAK":
                    curr_state = BlackJack.dealer_peak(deck, player, dealer)

                case "ROUNDOVER":
                    curr_state = BlackJack.roundover_state(deck, player, dealer)
                    
                case "WIN":
                    print("ONE MORE ROUND CANT HURT")
                    game_over = True

                case "LOSE":
                    print("TRY AGAIN, NERD!")
                    game_over = True
                
                case "TIE":
                    print("It's always been rigged..")
                    game_over = True



    def deal_state(deck: Deck, player: Player, dealer: Dealer):
        player.hand.add_card(deck.deal_card(True))
        dealer.hand.add_card(deck.deal_card(True))
        player.hand.add_card(deck.deal_card(True))
        dealer.hand.add_card(deck.deal_card(True))
        natural_ranks = ("QUEEN", "JACK", "KING", "TEN", "ACE")
        up_card = dealer.get_up_card()
        print(dealer.get_up_card())
        player.update_score(player.hand_score())
        if player.soft_score == 21 or player.hard_score == 21:
            print(player.hand)
            #change this to dealer peak
            player.has_natural_blackjack = True
            return States(5).name
        
        
        if up_card.rank in natural_ranks:
            return States(5).name
        dealer.update_score(dealer.hand_score())
        return States(2).name

    
    #player can hit, stand, double down(later), 
    def player_state(deck: Deck, player: Player):
        print("Enter the following:")
        print("H to hit, D for double down, S for stand")
        end_turn = False

        while not end_turn:
            print(player.hand)
            user_input = player.decide_action()
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


                    
    def roundover_state(deck: Deck, player: Player, dealer: Dealer):
        print(f"Dealer: {dealer.hand}")
        dealer.hard17(deck)
        player_final_score = player.get_max_valid_score()
        dealer_final_score = dealer.get_max_valid_score()
        print(f"The scores are for player {player_final_score} and dealer {dealer_final_score}")
        print()
        if player_final_score > dealer_final_score:
            curr_state = States(6).name
        elif player_final_score < dealer_final_score:
            curr_state = States(7).name
        else:
            curr_state = States(9).name
        print(f"Dealer: {dealer.hand} and final score {dealer_final_score}")
        print(f"Final score: {player_final_score} Player {player.hand}")
        return curr_state


   
    def dealer_peak(deck: Deck, player: Player, dealer: Dealer) -> str:
        dealer.update_score(dealer.hand_score())
        dealer_score = dealer.get_max_valid_score()
        if dealer_score == 21:
            if player.has_natural_blackjack:
                #tie
                print(f"Unlucky...{dealer.hand}")
                return States(9).name
            else:
                print(f"shit on dealer: {dealer.hand}")
                print()
                print(f"Player hand: {player.hand}")
                return States(6).name
        elif player.has_natural_blackjack:
            return States(4).name
            
        return States(2).name
            

BlackJack.run_game()
