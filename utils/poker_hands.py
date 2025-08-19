import os
import sys
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.cards import Card
from entities.player import Poker_Player
from models.enums import Suit, Rank, Hands, Poker_Value



class BestHand:

    def __init__(self, hand: list[Card], river: list[Card]):
        self.hand = hand
        self.river = river
        self.total_cards = hand + river

        # Will be used as a cache so we don't need to have duplicate checks for different hand types
        self.counts, self.suits = self.count_cards(self.total_cards)
        self.high_card_count = 0
        self.contains_straight = False
        self.high_cards = []



    def is_high_card(self, card: Card) -> bool:
        value = Poker_Value[card.rank].value
        return value >= 10
    


    def count_cards(self, cards: list[Card]) -> dict[Rank, int]:
        self.counts = {}
        self.suits = {}
        for card in cards:
            if card.rank not in self.counts:
                self.counts[card.rank] = 1
            else:
                self.counts[card.rank] += 1
            
            if card.suit not in self.suits:
                self.suits[card.suit] = 1
            else:
                self.suits[card.suit] += 1
        
        return self.counts, self.suits



    def total_high_cards(self) -> int:
        count = 0
        for card in self.total_cards:
            if self.is_high_card(card):
                self.high_cards.append(card)
                count += 1
        
        self.high_card_count = count
        return count
    


    def is_straight(self, cards: list[Card]) -> None | list[Card]:
        values = [(Poker_Value[card.rank].value, card) for card in cards]
        values.sort(key=lambda x: x[0])

        longest_straight_cards = []

        current_straight_cards = [values[0][1]]
        for i in range(1, len(values)):
            if values[i][0] - values[i - 1][0] == 1:
                current_straight_cards.append(values[i][1])
            else:
                if len(longest_straight_cards) < len(current_straight_cards):
                    longest_straight_cards = current_straight_cards
                current_straight_cards = [values[i][1]]
        
        if len(longest_straight_cards) < len(current_straight_cards):
            longest_straight_cards = current_straight_cards

        return None if len(longest_straight_cards) < 5 else longest_straight_cards
    


    def is_flush(self, cards: list[Card]) -> bool:
        if len(cards) != 5:
            for suit in self.suits:
                if self.suits[suit] == 5:
                    return True

        suits = set([card.suit for card in cards])
        return len(suits) == 1



    def is_royal_flush(self) -> bool:
        if self.total_high_cards() != 5:
            return False
        
        straight_results = self.is_straight(self.total_cards)
        if straight_results is None:
            return False
        
        if not self.is_flush(straight_results):
            return False
        
        return True
    


    def is_straight_flush(self) -> bool:
        straight_result = self.is_straight(self.total_cards)
        if straight_result is None:
            return False
        
        if not self.is_flush(straight_result):
            return False
        
        return True

    
    
    def is_four_of_a_kind(self) -> bool:
        return 4 in self.counts.values()
    


    def is_full_house(self) -> bool:
        return self.is_three_of_a_kind() and self.is_pair()
    


    def is_three_of_a_kind(self) -> bool:
        return 3 in self.counts.values()
    


    def is_two_pair(self) -> bool:
        return sum(1 for count in self.counts.values() if count == 2) == 2
    


    def is_pair(self) -> bool:
        return 2 in self.counts.values()



    def get_best_hand(self) -> int:
        if self.is_royal_flush():
            return Hands.ROYAL_FLUSH
        
        if self.is_straight_flush():
            return Hands.STRAIGHT_FLUSH
        
        if self.is_four_of_a_kind():
            return Hands.FOUR_OF_A_KIND
        
        if self.is_full_house():
            return Hands.FULL_HOUSE
        
        if self.is_flush(self.total_cards):
            return Hands.FLUSH
        
        if self.is_straight(self.total_cards) is not None:
            return Hands.STRAIGHT
        
        if self.is_three_of_a_kind():
            return Hands.THREE_OF_A_KIND
        
        if self.is_two_pair():
            return Hands.TWO_PAIR
        
        if self.is_pair():
            return Hands.ONE_PAIR
        
        return Hands.HIGH_CARD



class TieBreaker:

    def __init__(self, ranks: list[tuple[BestHand, Poker_Player]]):
        self.ranks = ranks
        self.hands, self.players = self._fill_hands()
    


    def _fill_hands(self) -> None:
        hands = {}
        players = {}
        for rank in self.ranks:
            key = rank[1].name
            hand = rank[1].hand
            ordered_hand = sorted(hand, key=lambda x: Poker_Value[x.rank.name].value, reverse=True)
            
            players[key] = rank[1]
            hands[key] = ordered_hand
        
        return hands, players
    


    def high_card(self) -> Poker_Player:
        index = 0
        while index < 2:
            count = 0
            max_card = 0
            player_name = None
            for player, cards in self.hands.items():
                value = Poker_Value[cards[index].rank.name].value
                if value > max_card:
                    max_card = value
                    player_name = player
                elif value == max_card:
                    count += 1
            
            if count == 0:
                break
            index += 1
        
        return self.players[player_name]



    def one_pair(self) -> Poker_Player:
        pass




if __name__ == "__main__":
    player1 = Poker_Player("Player 1")
    player2 = Poker_Player("Player 2")
    player3 = Poker_Player("Player 3")

    player1.hand = [Card(Suit.HEART, Rank.ACE), Card(Suit.HEART, Rank.KING)]
    player2.hand = [Card(Suit.HEART, Rank.ACE), Card(Suit.HEART, Rank.QUEEN)]
    player3.hand = [Card(Suit.SPADE, Rank.ACE), Card(Suit.SPADE, Rank.TWO)]
    

    ranks = [(Hands.HIGH_CARD, player1), (Hands.HIGH_CARD, player2), (Hands.HIGH_CARD, player3)]
    random.shuffle(ranks)
    tie_breaker = TieBreaker(ranks)
    print(tie_breaker.high_card().name)