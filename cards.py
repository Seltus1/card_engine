from dataclasses import dataclass, field
from enum import Enum
from random import shuffle


class Suit(Enum):
    SPADE = 1
    CLUB = 2
    HEART = 3
    DIAMOND = 4


class Rank(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13



@dataclass
class Card:
    suit: str
    rank: int



@dataclass
class Deck:
    is_empty: bool
    total_cards: int
    cards: list[Card] = field(default_factory=list)

    @classmethod
    def create_deck(cls) -> 'Deck':
        play_deck = Deck(False, 52)
        for i in range(1,5):
            for j in range (1,14):
                play_deck.cards.append(Card(Suit(i).name, Rank(j).name))
        shuffle(play_deck.cards)
        return play_deck
    

    @property
    def remaining_cards(self):
        return len(self.cards)
    
    
    def deal_card(self) -> Card:
        if not self.is_empty:
            return self.cards.pop()


@dataclass
class Hand:
    hand_limit: int
    cards: list[Card] = field(default_factory=list)


    @property
    def hand_size(self) -> int:
        return len(self.cards)
    
    #Always remember to change any function sigs when you change the way things aer organized or sorted
    def create_hand(hand_limit: int) -> 'Hand':
        return Hand(hand_limit=hand_limit)
    
    def add_card(self, card: Card) -> bool:
        if self.hand_size < self.hand_limit:
            self.cards.append(card)
            return True
        else:
            return False

# x = Deck.create_deck()

# p = x.deal_card()
# print(f"{p.rank} and {p.suit}")