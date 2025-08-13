from dataclasses import dataclass, field
from models.enums import *
from random import shuffle


@dataclass(frozen=True)
class Card:
    suit: str
    rank: int

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
    def  ascii_card(self):
        """
        Prints an ASCII representation of a single playing card.

        Args:
            rank (str): The rank of the card ('2'-'10', 'J', 'Q', 'K', 'A').
            suit (str): The suit of the card ('♠', '♥', '♦', '♣').
        """
        top = "┌─────────┐"
        bottom = "└─────────┘"
        side = "│         │"

        if self.rank == "10":  # Ten is the only rank with two digits
            rank_right = Ascii_Rank[self.rank].value
            rank_left = Ascii_Rank[self.rank].value
        else:
            rank_right = Ascii_Rank[self.rank].value + " "
            rank_left = " " + Ascii_Rank[self.rank].value

        suit_line = f"│    {Symbols[self.suit].value}    │"
        rank_line_left = f"│{rank_left}       │"
        rank_line_right = f"│       {rank_right}│"
        lines_of_cards = [top, rank_line_left, side, suit_line, side, rank_line_right, bottom]
        return lines_of_cards


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
    # i and j, i is changing fastsr than j, therefore i should be in the most inner loop
    def __str__(self):
        word = ""
        for i in range(0, 7):
            # if i % 4 == 0:
            #         print() 
            for card in self.cards:
                card_str = card.ascii_card()
                word += card_str[i] + "\t"
            print(word)
            if i == 6:
                print()
            word = ""

                
        return "Hand contains: " + ", ".join(f"{card} " for card in self.cards)