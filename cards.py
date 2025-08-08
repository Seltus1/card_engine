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
    remaining_cards: int
    cards: list[Card] = field(default_factory=list)

    @classmethod
    def create_deck(cls) -> 'Deck':
        play_deck = Deck(False, 52, 52)
        for i in range(1,5):
            for j in range (1,14):
                x = Card(Suit(i).name, Rank(j).name)
                play_deck.cards.append(x)
        shuffle(play_deck.cards)
        return play_deck

x = Deck.create_deck()

for card in x.cards:
    print(f"The rank is: {card.rank} and the suit is {card.suit} {f}")