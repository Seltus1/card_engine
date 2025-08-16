from models.enums import States
from models.cards import *
from entities.dealer import Dealer
from entities.player import Player
from utils.board_art import *
import os
ace_of_spaces = Card("SPADE", "ACE") 
king_of_heart = Card("HEART", "KING")

class BlackJack:



    def run_game():
        curr_state = States.DEAL
        deck = Deck.create_deck()
        
        game_over = False
        player = Player()
        dealer = Dealer()
        # BlackJack.deal_state(deck, curr_state, player, dealer)
        while not game_over:

            match curr_state:
                case States.DEAL:
                    deck = deck.reset()
                    curr_state = BlackJack.deal_state(deck, player, dealer)
                case States.BLACKJACK:
                    final_print(States.BLACKJACK, player, dealer)
                    curr_state = BlackJack.choose_state(player, dealer)

                case States.PLAYER:
                    curr_state = BlackJack.player_state(deck, player, dealer)
                
                case States.BUST:
                    final_print(States.BUST, player, dealer)
                    curr_state = BlackJack.choose_state(player, dealer)


                case States.DEALER_PEAK:
                    curr_state = BlackJack.dealer_peak(deck, player, dealer)

                case States.ROUNDOVER:
                    curr_state = BlackJack.roundover_state(deck, player, dealer)
                    
                case States.WIN:
                    final_print(States.WIN, player, dealer)
                    curr_state = BlackJack.choose_state(player, dealer)

                case States.LOSE:
                    final_print(States.LOSE, player, dealer)
                    curr_state = BlackJack.choose_state(player, dealer)
                
                case States.TIE:
                    print("It's always been rigged..")
                    curr_state = BlackJack.choose_state(player, dealer)
                
                case States.GAMEOVER:
                    game_over = True



    def deal_state(deck: Deck, player: Player, dealer: Dealer):
        print(deck.remaining_cards)
        player.hand.add_card(deck.deal_card(True))
        dealer.hand.add_card(deck.deal_card(True))
        player.hand.add_card(deck.deal_card(True))
        dealer.hand.add_card(deck.deal_card(True))
        natural_ranks = ("QUEEN", "JACK", "KING", "TEN", "ACE")
        up_card = dealer.get_up_card()
        player.update_score(player.hand_score())
        if player.soft_score == 21 or player.hard_score == 21:
            print(player.hand)
            #change this to dealer peak
            player.has_natural_blackjack = True
            return States.DEALER_PEAK
        
        
        if up_card.rank in natural_ranks:
            return States.DEALER_PEAK
        dealer.update_score(dealer.hand_score())
        return States.PLAYER

    
    #player can hit, stand, double down(later), 
    def player_state(deck: Deck, player: Player, dealer: Dealer):
        end_turn = False

        while not end_turn:
            os.system("clear")
            print_board(player, dealer, False)
            print("Enter the following:")
            print("H to hit, D for double down, S for stand")
            print(deck.remaining_cards)
            user_input = player.decide_action()
            match user_input.upper():
                case "H":
                    player.hand.add_card(deck.deal_card(True))
                    player.update_score(player.hand_score())

                    if player.hard_score == 21 or player.soft_score == 21:
                        return States.ROUNDOVER
                    if player.hard_score > 21 and player.soft_score > 21:
                        return States.BUST
                    elif player.hard_score > 21 and player.soft_score == 0:
                        return States.BUST
                    
                case "S":
                    player.update_score(player.hand_score())
                    dealer.update_score(dealer.hand_score())
                    return States.ROUNDOVER
                
                case "D":
                    print("Not yet implemented")
                case _:
                    print("hey")
                    continue


                    
    def roundover_state(deck: Deck, player: Player, dealer: Dealer):
        dealer.hard17(deck)
        player_final_score = player.get_max_valid_score()
        dealer_final_score = dealer.get_max_valid_score()
        print(f"The scores are for player {player_final_score} and dealer {dealer_final_score}")
        print()
        if player_final_score > dealer_final_score:
            curr_state = States.WIN
        elif player_final_score < dealer_final_score:
            curr_state = States.LOSE
        else:
            curr_state = States.TIE
        return curr_state


   
    def dealer_peak(deck: Deck, player: Player, dealer: Dealer) -> str:
        dealer.update_score(dealer.hand_score())
        dealer_score = dealer.get_max_valid_score()
        if dealer_score == 21:
            if player.has_natural_blackjack:
                #tie
                print(f"Unlucky...{dealer.hand}")
                return States.TIE
            else:
                print(f"shit on dealer: {dealer.hand}")
                print()
                print(f"Player hand: {player.hand}")
                return States.LOSE
        elif player.has_natural_blackjack:
            return States.BLACKJACK
            
        return States.PLAYER
    
    def choose_state(player: Player, dealer: Dealer):
        print(text2asci(f"FINAL SCORE! Dealer: {dealer.get_max_valid_score()} and Player: {player.get_max_valid_score()}", "medium"))
        print("Are you tired of winning?")
        print("Type q to quit or press Enter to gamble more")
        while True:
            action = player.decide_action()
            match action:
                case "q":
                    return States.GAMEOVER
                case "":
                    player.reset()
                    dealer.reset()
                    os.system('clear')
                    return States.DEAL
                case _:
                    print("Valid input, nerd!")
        


           
if __name__ == "__main__":
    BlackJack.run_game()