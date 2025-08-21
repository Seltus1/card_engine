import os
import sys
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.cards import Card
from entities.player import Poker_Player
from models.enums import Rank, Hands, Poker_Value

TWO_OF_A_KIND = 2
THREE_OF_A_KIND = 3
FOUR_OF_A_KIND = 4



class BestHand:

    def __init__(self, hand: list[Card], river: list[Card]):
        self.hand = hand
        self.river = river
        self.best_hand = None
        self.total_cards = hand + river

        # Will be used as a cache so we don't need to have duplicate checks for different hand types
        self.counts, self.suits = self.count_cards(self.total_cards)
        self.high_card_count = 0
        self.contains_straight = False
        self.high_cards = []



    def _best_hand_contains_hand_held(self, best_hand: list[Card]) -> bool:
        return any(card in self.hand for card in best_hand)



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
    


    def is_flush(self, cards: list[Card]) -> None | list[Card]:
        # This check is for regular flushes, since we will be checking all 7 cards
        if len(cards) != 5:
            suit_to_check = None
            for suit in self.suits:
                if self.suits[suit] == 5:
                    suit_to_check = suit
                    break
            
            if suit_to_check is None:
                return None
            
            return [card for card in cards if card.suit == suit_to_check]

        # This check is for royal flushes, since we will be checking the cards from the straight
        suits = set([card.suit for card in cards])
        return cards if len(suits) == 1 else None
    


    def count_individual_card_amount(self, amount: int):
        kind_check = None
        for rank, count in self.counts.items():
            if count == amount:
                kind_check = rank
                break
        
        if kind_check is None:
            return None
        
        return [card for card in self.total_cards if card.rank == kind_check]
    


    def something_of_a_kind(self, amount: int) -> bool:
        best_hand = self.count_individual_card_amount(amount)
        if best_hand is None:
            return False
        
        if not self._best_hand_contains_hand_held(best_hand):
            return False
        
        self.best_hand = best_hand
        return True



    def is_royal_flush(self) -> bool:
        if self.total_high_cards() != 5:
            return False
        
        straight_results = self.is_straight(self.total_cards)
        if straight_results is None:
            return False
        
        flush_results = self.is_flush(straight_results)
        if flush_results is None:
            return False
        
        if not self._best_hand_contains_hand_held(flush_results):
            return False
        
        self.best_hand = flush_results
        return True
    


    def is_straight_flush(self) -> bool:
        straight_result = self.is_straight(self.total_cards)
        if straight_result is None:
            return False
        
        flush_results = self.is_flush(straight_result)
        if flush_results is None:
            return False
        
        if not self._best_hand_contains_hand_held(flush_results):
            return False
        
        self.best_hand = flush_results
        return True

    
    
    def is_four_of_a_kind(self) -> bool:
        return self.something_of_a_kind(FOUR_OF_A_KIND)
    


    def is_full_house(self) -> bool:
        three_of_a_kind = self.count_individual_card_amount(THREE_OF_A_KIND)
        if three_of_a_kind is None:
            return False
    
        two_of_a_kind = self.count_individual_card_amount(TWO_OF_A_KIND)
        if two_of_a_kind is None:
            return False
        
        if not self._best_hand_contains_hand_held(three_of_a_kind) or not self._best_hand_contains_hand_held(two_of_a_kind):
            return False

        self.best_hand = three_of_a_kind + two_of_a_kind
        return True
    


    def is_three_of_a_kind(self) -> bool:
        return self.something_of_a_kind(THREE_OF_A_KIND)
    


    def is_two_pair(self) -> bool:
        two_pair_1 = self.count_individual_card_amount(TWO_OF_A_KIND)
        if two_pair_1 is None:
            return False
        
        rank = two_pair_1[0].rank
        del self.counts[rank]

        two_pair_2 = self.count_individual_card_amount(TWO_OF_A_KIND)
        if two_pair_2 is None:
            self.counts[rank] = 2 # Need to put back this since it will be used for the one_pair check
            return False
        
        best_hand = two_pair_1 + two_pair_2
        if not self._best_hand_contains_hand_held(best_hand):
            return False
        
        self.best_hand = best_hand
        return True
    


    def is_pair(self) -> bool:
        return self.something_of_a_kind(TWO_OF_A_KIND)



    def get_best_hand(self) -> int:
        if self.is_royal_flush():
            return Hands.ROYAL_FLUSH
        
        if self.is_straight_flush():
            return Hands.STRAIGHT_FLUSH
        
        if self.is_four_of_a_kind():
            return Hands.FOUR_OF_A_KIND
        
        if self.is_full_house():
            return Hands.FULL_HOUSE
        
        if self.is_flush(self.total_cards) is not None:
            return Hands.FLUSH
        
        if self.is_straight(self.total_cards) is not None:
            return Hands.STRAIGHT
        
        if self.is_three_of_a_kind():
            return Hands.THREE_OF_A_KIND
        
        if self.is_two_pair():
            return Hands.TWO_PAIR
        
        if self.is_pair():
            return Hands.ONE_PAIR
        
        self.best_hand = self.hand
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
            hand = rank[1].hand.cards
            ordered_hand = sorted(hand, key=lambda x: Poker_Value[x.rank].value, reverse=True)
            
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
                value = Poker_Value[cards[index].rank].value
                if value > max_card:
                    max_card = value
                    player_name = player
                    count = 0
                elif value == max_card:
                    count += 1
            
            if count == 0:
                break
            index += 1
        
        return self.players[player_name]



if __name__ == "__main__":
    # Create test players
    players = {}
    for i in range(10):
        players[f"player{i+1}"] = Poker_Player(f"Player {i+1}")
    
    # Community cards (river) for testing
    river = [
        Card("HEART", "NINE"),
        Card("CLUB", "TEN"), 
        Card("DIAMOND", "JACK"),
        Card("SPADE", "QUEEN"),
        Card("HEART", "KING")
    ]
    
    # Test hands for each poker hand type
    
    # 1. ROYAL FLUSH - A, K, Q, J, 10 all same suit
    players["player1"].hand.cards = [Card("HEART", "ACE"), Card("HEART", "TEN")]
    royal_flush_river = [
        Card("HEART", "KING"),
        Card("HEART", "QUEEN"), 
        Card("HEART", "JACK"),
        Card("CLUB", "TWO"),
        Card("SPADE", "THREE")
    ]
    royal_flush_hand = BestHand(players["player1"].hand.cards, royal_flush_river)
    print(f"Royal Flush: {royal_flush_hand.get_best_hand()}")
    
    # 2. STRAIGHT FLUSH - 5 consecutive cards same suit
    players["player2"].hand.cards = [Card("SPADE", "FIVE"), Card("SPADE", "SIX")]
    straight_flush_river = [
        Card("SPADE", "SEVEN"),
        Card("SPADE", "EIGHT"),
        Card("SPADE", "NINE"),
        Card("HEART", "TWO"),
        Card("CLUB", "THREE")
    ]
    straight_flush_hand = BestHand(players["player2"].hand.cards, straight_flush_river)
    print(f"Straight Flush: {straight_flush_hand.get_best_hand()}")
    
    # 3. FOUR OF A KIND - 4 cards of same rank
    players["player3"].hand.cards = [Card("HEART", "EIGHT"), Card("SPADE", "EIGHT")]
    four_kind_river = [
        Card("CLUB", "EIGHT"),
        Card("DIAMOND", "EIGHT"),
        Card("HEART", "ACE"),
        Card("SPADE", "TWO"),
        Card("CLUB", "THREE")
    ]
    four_kind_hand = BestHand(players["player3"].hand.cards, four_kind_river)
    print(f"Four of a Kind: {four_kind_hand.get_best_hand()}")
    
    # 4. FULL HOUSE - 3 of a kind + pair
    players["player4"].hand.cards = [Card("HEART", "KING"), Card("SPADE", "KING")]
    full_house_river = [
        Card("CLUB", "KING"),
        Card("DIAMOND", "ACE"),
        Card("HEART", "ACE"),
        Card("SPADE", "TWO"),
        Card("CLUB", "THREE")
    ]
    full_house_hand = BestHand(players["player4"].hand.cards, full_house_river)
    print(f"Full House: {full_house_hand.get_best_hand()}")
    
    # 5. FLUSH - 5 cards same suit
    players["player5"].hand.cards = [Card("DIAMOND", "TWO"), Card("DIAMOND", "FOUR")]
    flush_river = [
        Card("DIAMOND", "SIX"),
        Card("DIAMOND", "EIGHT"),
        Card("DIAMOND", "TEN"),
        Card("HEART", "ACE"),
        Card("SPADE", "KING")
    ]
    flush_hand = BestHand(players["player5"].hand.cards, flush_river)
    print(f"Flush: {flush_hand.get_best_hand()}")
    
    # 6. STRAIGHT - 5 consecutive cards
    players["player6"].hand.cards = [Card("HEART", "FOUR"), Card("SPADE", "FIVE")]
    straight_river = [
        Card("CLUB", "SIX"),
        Card("DIAMOND", "SEVEN"),
        Card("HEART", "EIGHT"),
        Card("SPADE", "ACE"),
        Card("CLUB", "KING")
    ]
    straight_hand = BestHand(players["player6"].hand.cards, straight_river)
    print(f"Straight: {straight_hand.get_best_hand()}")
    
    # 7. THREE OF A KIND - 3 cards same rank
    players["player7"].hand.cards = [Card("HEART", "SEVEN"), Card("SPADE", "SEVEN")]
    three_kind_river = [
        Card("CLUB", "SEVEN"),
        Card("DIAMOND", "ACE"),
        Card("HEART", "KING"),
        Card("SPADE", "TWO"),
        Card("CLUB", "THREE")
    ]
    three_kind_hand = BestHand(players["player7"].hand.cards, three_kind_river)
    print(f"Three of a Kind: {three_kind_hand.get_best_hand()}")
    
    # 8. TWO PAIR - 2 pairs
    players["player8"].hand.cards = [Card("HEART", "JACK"), Card("SPADE", "JACK")]
    two_pair_river = [
        Card("CLUB", "NINE"),
        Card("DIAMOND", "NINE"),
        Card("HEART", "ACE"),
        Card("SPADE", "TWO"),
        Card("CLUB", "THREE")
    ]
    two_pair_hand = BestHand(players["player8"].hand.cards, two_pair_river)
    print(f"Two Pair: {two_pair_hand.get_best_hand()}")
    
    # 9. ONE PAIR - 1 pair
    players["player9"].hand.cards = [Card("HEART", "QUEEN"), Card("SPADE", "QUEEN")]
    one_pair_river = [
        Card("CLUB", "FOUR"),
        Card("DIAMOND", "SEVEN"),
        Card("HEART", "NINE"),
        Card("SPADE", "TWO"),
        Card("CLUB", "ACE")
    ]
    one_pair_hand = BestHand(players["player9"].hand.cards, one_pair_river)
    print(f"One Pair: {one_pair_hand.get_best_hand()}")
    
    # 10. HIGH CARD - no pairs, straights, or flushes
    players["player10"].hand.cards = [Card("HEART", "ACE"), Card("SPADE", "KING")]
    high_card_river = [
        Card("CLUB", "QUEEN"),
        Card("DIAMOND", "JACK"),
        Card("HEART", "NINE"),
        Card("SPADE", "SEVEN"),
        Card("CLUB", "FIVE")
    ]
    high_card_hand = BestHand(players["player10"].hand.cards, high_card_river)
    print(f"High Card: {high_card_hand.get_best_hand()}")
    
    print("\n" + "="*50)
    print("All test hands created successfully!")
    print("="*50)