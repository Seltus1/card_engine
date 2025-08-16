import time
import random

from utils.poker_hands import BestHand
from entities.player import Poker_Player
from models.enums import Poker_Game_State
from models.cards import Deck, Card, print_cards

class PokerGame:

    def __init__(self, players: int):
        if players > 10:
            raise ValueError("Too many players, 10 is the max")
        
        self.river = []
        self.river_count = 0
        self.single_river = False # If false, we will deal 3 cards to the river, if true we will deal 1 card to the river
        self.deck = Deck.create_deck()

        self.big_blind_index = 2
        self.small_blind_index = 1
        self.dealer_button_index = 0

        self.pot = 0
        self.big_blind = 20
        self.call_amount = 20
        self.small_blind = 10

        self.did_raise = False
        self.seen_players = []
        
        self.players = []
        for i in range(players):
            self.players.append(Poker_Player(bot=i != 0))
        
        random.shuffle(self.players) # give the players a random order to sit at the table

        self.ranked_hands = []
    


    def call_bet(self, player: Poker_Player) -> None:
        if player.chips < self.call_amount:
            raise ValueError("Player does not have enough chips to call")
        if player.bot:
            time.sleep(0.5)

        print()
        bet_amount = self.call_amount - player.round_bet
        print(f"{player.name} called ${bet_amount}")
        self.pot += bet_amount
        player.chips -= bet_amount
        player.round_bet += bet_amount
    


    def raise_bet(self, player: Poker_Player) -> None:
        print(f"You currently have ${player.chips} dollars\n")
        raise_amount = int(input(f"Please enter the amount you want to raise: $"))
        if raise_amount < self.call_amount:
            raise ValueError("Raise amount must be greater than the call amount")
        
        self.pot += raise_amount
        player.chips -= raise_amount

        self.call_amount = raise_amount
        self.did_raise = True
        self.seen_players = [] # reset the seen players since everyone has to call the raise
    


    def fold(self, player: Poker_Player) -> None:
        player_index = self.players.index(player)
        self.players.pop(player_index)
                
    


    def play_bet(self, player: Poker_Player) -> None:
        bet = input(f"Please enter r to raise, c to call, or f to fold\n")

        if bet.lower() == "r":
            self.raise_bet(player)
        elif bet.lower() == "c":
            self.call_bet(player)
        elif bet.lower() == "f":
            self.fold()



    def deal_cards(self):
        did_small_blind = False
        did_big_blind = False
        did_all = False
        for _ in range(2):
            # The first card is dealt to the left of the dealer button (small blind)
            end_index = self.dealer_button_index
            player_pos = end_index + 1
            while True:
                player = self.players[player_pos]
                player.hand.add_card(self.deck.deal_card(True))

                if player_pos == end_index:
                    break # We have dealt the cards in a circle

                # Resetting the players betting amount for the next round
                
                if not did_small_blind and player_pos == self.small_blind_index:
                    player.round_bet = self.small_blind
                    self.pot += self.small_blind
                    did_small_blind = True
                elif not did_big_blind and player_pos == self.big_blind_index:
                    player.round_bet = self.big_blind
                    self.pot += self.big_blind
                    self.seen_players.append(player_pos)
                    did_big_blind = True
                elif not did_all:
                    player.round_bet = 0
                
                player_pos = (player_pos + 1) % len(self.players)
            
            did_all = True

    

    def bets(self):
        index = self.big_blind_index + 1
        if not self.players[self.big_blind_index].bot:
            print("You were the big blind, and called")
            print_cards(list(self.players[self.big_blind_index].hand.cards))

        while len(self.seen_players) < len(self.players):
            player = self.players[index]
            if player.bot:
                self.call_bet(player)
            else:
                print(f"\nPlayer Hand is:")
                print_cards(list(player.hand.cards))
                self.play_bet(player)
            
            self.seen_players.append(index)
            index = (index + 1) % len(self.players)
        
        self.seen_players = []
    


    def showdown(self) -> None:
        if not self.single_river:
            for _ in range(3):
                self.river.append(self.deck.deal_card(True))
            
            self.single_river = True
        else:
            self.river.append(self.deck.deal_card(True))
        
        self.river_count += 1
    


    def reveal(self) -> None:
        for player in self.players:
            cards = list(player.hand.cards)
            print(f"\n{player.name} Hand is:")
            print_cards(cards)
            hand = BestHand(cards, self.river)
            best_hand = hand.get_best_hand()
            self.ranked_hands.append((best_hand, player))
        
        self.ranked_hands.sort(key=lambda x: x[0].value, reverse=True)
    


    def winner(self) -> None:
        winner = self.ranked_hands[0][1]
        print(f"The winner is {winner.name} with a {self.ranked_hands[0][0].name}")
        
        winner.chips += self.pot
        if not winner.bot:
            print(f"Your new pot is ${winner.chips}")
        
        print("Starting the next round...")
        time.sleep(1)
        self.reset_game()
    


    def reset_game(self) -> None:
        self.river = []
        self.river_count = 0
        self.single_river = False # If false, we will deal 3 cards to the river, if true we will deal 1 card to the river
        self.deck = Deck.create_deck()

        self.big_blind_index = 2
        self.small_blind_index = 1
        self.dealer_button_index = 0

        self.pot = 0
        self.big_blind = 20
        self.call_amount = 20
        self.small_blind = 10

        self.did_raise = False
        self.seen_players = []

        self.ranked_hands = []

    
    
    def play_poker(self):
        print("Welcome to Poker!")
        print(f"The small blind is ${self.small_blind}")
        print(f"The big blind is ${self.big_blind}")
        curr_state = Poker_Game_State.DEAL
        while curr_state != Poker_Game_State.GAMEOVER:

            match curr_state:

                case Poker_Game_State.DEAL:
                    self.deal_cards()
                    curr_state = Poker_Game_State.BETS
                case Poker_Game_State.BETS:
                    self.bets()
                    print(f"\nThe Pot is: ${self.pot}")
                    curr_state = Poker_Game_State.SHOWDOWN
                    self.call_amount = self.big_blind
                case Poker_Game_State.SHOWDOWN:
                    self.showdown()
                    print(f"\nThe River is:")
                    print_cards(self.river)
                    curr_state = Poker_Game_State.REVEAL if self.river_count == 3 else Poker_Game_State.BETS
                    if curr_state == Poker_Game_State.BETS:
                        for player in self.players:
                            player.round_bet = 0
                case Poker_Game_State.REVEAL:
                    self.reveal()
                    curr_state = Poker_Game_State.WINNER
                case Poker_Game_State.WINNER:
                    self.winner()
                    curr_state = Poker_Game_State.DEAL # TODO: Make this a loop so we can play again state.DEAL, game over is when 1 player left



if __name__ == "__main__":
    player = random.randint(4, 10)
    game = PokerGame(player)
    game.play_poker()








# TODO:
# If someone goes all in and one other person accepts, then the cards of both players are shown.
