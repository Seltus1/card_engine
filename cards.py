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



@dataclass(frozen=True)
class Card:
    suit: str
    rank: int

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    def print_card(rank, suit):
        """
        Prints an ASCII representation of a single playing card.

        Args:
            rank (str): The rank of the card ('2'-'10', 'J', 'Q', 'K', 'A').
            suit (str): The suit of the card ('♠', '♥', '♦', '♣').
        """
        top = "┌─────────┐"
        bottom = "└─────────┘"
        side = "│         │"

        if rank == "10":  # Ten is the only rank with two digits
            rank_right = rank
            rank_left = rank
        else:
            rank_right = rank + " "
            rank_left = " " + rank

        suit_line = f"│    {suit}    │"
        rank_line_left = f"│{rank_left}       │"
        rank_line_right = f"│       {rank_right}│"

        print(top)
        print(rank_line_left)
        print(side)
        print(suit_line)
        print(side)
        print(rank_line_right)
        print(bottom)



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
    

    def deal_card(self, can_add: bool) -> Card:
        if not self.is_empty and can_add:
            return self.cards.pop()
        


@dataclass
class Hand:
    hand_limit: int
    cards: list[Card] = field(default_factory=list)


    @property
    def hand_size(self) -> int:
        return len(self.cards)
    
    @property
    def can_add_hand(self) -> bool:

        return self.hand_size < self.hand_limit
    #Always remember to change any function sigs when you change the way things aer organized or sorted
    def create_hand(hand_limit: int = None) -> 'Hand':
        if hand_limit:
            return Hand(hand_limit=hand_limit)
        else:
            return Hand(hand_limit=100)
    
    def add_card(self, card: Card) -> bool:
        if self.hand_size < self.hand_limit:
            self.cards.append(card)
            return True
        else:
            return False
        
    
    def contains_rank(self, target: str):
        return any(card.rank == target for card in self.cards)
    
    def __str__(self):
        return "Hand contains: " + ", ".join(f"{card} " for card in self.cards)

# x = Deck.create_deck()

# p = x.deal_card()
# print(f"{p.rank} and {p.suit}")