from models.enums import States
from models.cards import *
from entities.dealer import Dealer
from entities.player import Player
from utils.board_art import *
from utils.stats import *

ace_of_spaces = Card("SPADE", "ACE") 
king_of_heart = Card("HEART", "KING")

class BlackJack:

    def run_game():
        curr_state = States.BET
        deck = Deck.create_deck()
        game_over = False
        player = Player()
        dealer = Dealer()
        stat_tracking = Stats()
        while not game_over:
            match curr_state:
                case States.BET:
                    curr_state = BlackJack.bet_state(player)
                    stat_tracking.update_specific_stat("total_bets")
                case States.DEAL:
                    deck = deck.reset()
                    curr_state = BlackJack.deal_state(deck, player, dealer)

                case States.BLACKJACK:
                    final_print(States.BLACKJACK, player, dealer)
                    stat_tracking.update_stat(player, curr_state)
                    curr_state = BlackJack.choose_state(player, dealer)

                case States.PLAYER:
                    curr_state = BlackJack.player_state(deck, player, dealer)
                
                case States.BUST:
                    final_print(States.BUST, player, dealer)
                    stat_tracking.update_stat(player, curr_state)
                    curr_state = BlackJack.choose_state(player, dealer)

                case States.DEALER_PEAK:
                    curr_state = BlackJack.dealer_peak(deck, player, dealer, stat_tracking)

                case States.ROUNDOVER:
                    curr_state = BlackJack.roundover_state(deck, player, dealer)
                    
                case States.WIN:
                    final_print(States.WIN, player, dealer)
                    stat_tracking.update_stat(player, curr_state)
                    curr_state = BlackJack.choose_state(player, dealer)

                case States.LOSE:
                    final_print(States.LOSE, player, dealer)
                    stat_tracking.update_stat(player, curr_state)
                    curr_state = BlackJack.choose_state(player, dealer)
                
                case States.TIE:
                    final_print(States.TIE, player, dealer)
                    stat_tracking.update_stat(player, curr_state)
                    curr_state = BlackJack.choose_state(player, dealer)
                
                case States.GAMEOVER:
                    game_over = True



    def deal_state(deck: Deck, player: Player, dealer: Dealer):
        player.hand.add_card(deck.deal_card(True))
        dealer.hand.add_card(deck.deal_card(True))
        player.hand.add_card(deck.deal_card(True))
        dealer.hand.add_card(deck.deal_card(True))
        natural_ranks = ("QUEEN", "JACK", "KING", "TEN", "ACE")
        up_card = dealer.get_up_card()
        player.update_score(player.hand_score())
        if player.soft_score == 21 or player.hard_score == 21:
            print(player.hand)
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
            clear_screen()
            print_board(player, dealer, False)
            tprint(f"Remaining cards: {deck.remaining_cards}", "small")
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


   
    def dealer_peak(deck: Deck, player: Player, dealer: Dealer, stat_tracker: Stats) -> str:
        dealer.update_score(dealer.hand_score())
        dealer_score = dealer.get_max_valid_score()
        if dealer_score == 21:
            if player.has_natural_blackjack:
                return States.TIE
            else:
                stat_tracker.update_specific_stat("blackjacks_against")
                return States.LOSE
        elif player.has_natural_blackjack:
            return States.BLACKJACK
            
        return States.PLAYER
    
    def choose_state(player: Player, dealer: Dealer):
        print_choose_state(player, dealer)
        while True:
            action = player.decide_action()
            match action:
                case "q":
                    return States.GAMEOVER
                case "":
                    player.reset()
                    dealer.reset()
                    clear_screen()
                    return States.BET
                case _:
                    print("Valid input, nerd!")

    def bet_state(player: Player):
        print_bet_state()
        while True:
            try:
                bet = int(player.decide_action())
                if bet > player.total_money:
                    #dummy for now, will call for input later
                    player.total_money == 10000
                player.curr_bet = bet
                return States.DEAL
            except:
                print("Invalid entry, whole numbers only")
                
    # def bet_state_helper(player: Player, answer: int):
    #     while True:
    #         try:
    #             bet = int(answer)
    #             if bet > player.total_money:
    #                 #dummy for now, will call for input later
    #                 player.total_money == 10000
    #             player.curr_bet = bet
    #             return bet
    #         except:
    #             print("Invalid entry, whole numbers only")
    
    def handle_player_bets(player: Player, bet: int):
        x=5



if __name__ == "__main__":
    BlackJack.run_game()