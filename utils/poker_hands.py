import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.cards import Card
from models.enums import Hands, Rank, Suit, Poker_Value



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


    def find_card(self, rank: Rank, suit: Suit, cards: list[Card]) -> Card | None:
        for card in cards:
            pass



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





if __name__ == "__main__":
    def test_hand_type(name: str, hand: list[Card], river: list[Card], expected_hand_type: Hands) -> bool:
        """Test a specific hand type and return whether it matches the expected result."""
        best_hand = BestHand(hand, river)
        result = best_hand.get_best_hand()
        success = result == expected_hand_type
        print(f"{name}: {'PASS' if success else 'FAIL'} (Expected: {expected_hand_type}, Got: {result})")
        return success
    
    print("Testing all 10 poker hand types:")
    print("=" * 50)
    
    # Test cases for all 10 hand types
    test_results = []
    
    # 1. Royal Flush (A, K, Q, J, 10 all same suit)
    hand1 = [Card(Suit.SPADE, Rank.ACE), Card(Suit.SPADE, Rank.KING)]
    river1 = [Card(Suit.SPADE, Rank.QUEEN), Card(Suit.SPADE, Rank.JACK), Card(Suit.SPADE, Rank.TEN), Card(Suit.HEART, Rank.TWO), Card(Suit.CLUB, Rank.THREE)]
    test_results.append(test_hand_type("Royal Flush", hand1, river1, Hands.ROYAL_FLUSH))
    
    # 2. Straight Flush (5 consecutive cards, same suit)
    hand2 = [Card(Suit.HEART, Rank.FIVE), Card(Suit.HEART, Rank.SIX)]
    river2 = [Card(Suit.HEART, Rank.SEVEN), Card(Suit.HEART, Rank.EIGHT), Card(Suit.HEART, Rank.NINE), Card(Suit.CLUB, Rank.TWO), Card(Suit.SPADE, Rank.THREE)]
    test_results.append(test_hand_type("Straight Flush", hand2, river2, Hands.STRAIGHT_FLUSH))
    
    # 3. Four of a Kind (4 cards of same rank)
    hand3 = [Card(Suit.SPADE, Rank.KING), Card(Suit.HEART, Rank.KING)]
    river3 = [Card(Suit.CLUB, Rank.KING), Card(Suit.DIAMOND, Rank.KING), Card(Suit.SPADE, Rank.ACE), Card(Suit.HEART, Rank.TWO), Card(Suit.CLUB, Rank.THREE)]
    test_results.append(test_hand_type("Four of a Kind", hand3, river3, Hands.FOUR_OF_A_KIND))
    
    # 4. Full House (3 of one rank + 2 of another rank)
    hand4 = [Card(Suit.SPADE, Rank.QUEEN), Card(Suit.HEART, Rank.QUEEN)]
    river4 = [Card(Suit.CLUB, Rank.QUEEN), Card(Suit.DIAMOND, Rank.JACK), Card(Suit.SPADE, Rank.JACK), Card(Suit.HEART, Rank.TWO), Card(Suit.CLUB, Rank.THREE)]
    test_results.append(test_hand_type("Full House", hand4, river4, Hands.FULL_HOUSE))
    
    # 5. Flush (5 cards same suit, not consecutive)
    hand5 = [Card(Suit.DIAMOND, Rank.TWO), Card(Suit.DIAMOND, Rank.FIVE)]
    river5 = [Card(Suit.DIAMOND, Rank.SEVEN), Card(Suit.DIAMOND, Rank.JACK), Card(Suit.DIAMOND, Rank.KING), Card(Suit.HEART, Rank.ACE), Card(Suit.CLUB, Rank.THREE)]
    test_results.append(test_hand_type("Flush", hand5, river5, Hands.FLUSH))
    
    # 6. Straight (5 consecutive cards, different suits)
    hand6 = [Card(Suit.SPADE, Rank.FOUR), Card(Suit.HEART, Rank.FIVE)]
    river6 = [Card(Suit.CLUB, Rank.SIX), Card(Suit.DIAMOND, Rank.SEVEN), Card(Suit.SPADE, Rank.EIGHT), Card(Suit.HEART, Rank.JACK), Card(Suit.CLUB, Rank.KING)]
    test_results.append(test_hand_type("Straight", hand6, river6, Hands.STRAIGHT))
    
    # 7. Three of a Kind (3 cards of same rank)
    hand7 = [Card(Suit.SPADE, Rank.TEN), Card(Suit.HEART, Rank.TEN)]
    river7 = [Card(Suit.CLUB, Rank.TEN), Card(Suit.DIAMOND, Rank.ACE), Card(Suit.SPADE, Rank.KING), Card(Suit.HEART, Rank.TWO), Card(Suit.CLUB, Rank.FOUR)]
    test_results.append(test_hand_type("Three of a Kind", hand7, river7, Hands.THREE_OF_A_KIND))
    
    # 8. Two Pair (2 cards of one rank + 2 cards of another rank)
    hand8 = [Card(Suit.SPADE, Rank.NINE), Card(Suit.HEART, Rank.NINE)]
    river8 = [Card(Suit.CLUB, Rank.SEVEN), Card(Suit.DIAMOND, Rank.SEVEN), Card(Suit.SPADE, Rank.ACE), Card(Suit.HEART, Rank.TWO), Card(Suit.CLUB, Rank.FOUR)]
    test_results.append(test_hand_type("Two Pair", hand8, river8, Hands.TWO_PAIR))
    
    # 9. One Pair (2 cards of same rank)
    hand9 = [Card(Suit.SPADE, Rank.EIGHT), Card(Suit.HEART, Rank.EIGHT)]
    river9 = [Card(Suit.CLUB, Rank.THREE), Card(Suit.DIAMOND, Rank.FIVE), Card(Suit.SPADE, Rank.SEVEN), Card(Suit.HEART, Rank.JACK), Card(Suit.CLUB, Rank.KING)]
    test_results.append(test_hand_type("One Pair", hand9, river9, Hands.ONE_PAIR))
    
    # 10. High Card (no other combination)
    hand10 = [Card(Suit.SPADE, Rank.TWO), Card(Suit.HEART, Rank.FOUR)]
    river10 = [Card(Suit.CLUB, Rank.SIX), Card(Suit.DIAMOND, Rank.EIGHT), Card(Suit.SPADE, Rank.TEN), Card(Suit.HEART, Rank.QUEEN), Card(Suit.CLUB, Rank.ACE)]
    test_results.append(test_hand_type("High Card", hand10, river10, Hands.HIGH_CARD))
    
    print("=" * 50)
    passed_tests = sum(test_results)
    total_tests = len(test_results)
    print(f"Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! The poker hand detection is working correctly.")
    else:
        print("❌ Some tests failed. Please check the implementation.")
