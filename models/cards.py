import time

from dataclasses import dataclass, field
from enums import *
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

        if self.rank == 10:  # Ten is the only rank with two digits
            rank_right = f"{Ascii_Rank[self.rank].value:2}" 
            rank_left =  f"{Ascii_Rank[self.rank].value:2}"
        else:
            rank_right = f"{Ascii_Rank[self.rank].value:<2}"
            rank_left =  f"{Ascii_Rank[self.rank].value:>2}"

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
    # fix this shit later (or not)
    def __str__(self):
        for i in range(0, 7):
            word = ""
            for card in self.cards:
                card_str = card.ascii_card()
                word += card_str[i] + "\t"
            print(word)


        return "Hand contains: " + ", ".join(f"{card} " for card in self.cards)




def print_cards(cards: list[Card]):
    card_builder = {
        "top":             ["┌", "─", "─", "─", "─", "─", "─", "─", "─", "─┐"],
        "bottom":          ["└", "─", "─", "─", "─", "─", "─", "─", "─", "─┘"],
        "side":            ["│", " ", " ", " ", " ", " ", " ", " ", " ", " ", "│"],
        "suit_line":       ["│", " ", " ", " ", " ", "{symbol}", " ", " ", " ", " ", "│"],
        "rank_line_left":  ["│", "{rank_left}", " ", " ", " ", " ", " ", " ", " ", "│"],
        "rank_line_right": ["│", " ", " ", " ", " ", " ", " ", " ", "{rank_right}", "│"],
    }

    build_order = ["top", "rank_line_left", "side", "suit_line", "side", "rank_line_right", "bottom"]

    for order in build_order:
        for card in cards:
            for index, build_string in enumerate(card_builder[order]):
                right_rank = card.rank.value + " " if card.rank.value != "10" else "10"
                left_rank = " " + card.rank.value if card.rank.value != "10" else "10"
                if order == "suit_line" and index == 5:
                    build_string = build_string.format(symbol=card.suit.value)
                elif order == "rank_line_left" and index == 1:
                    build_string = build_string.format(rank_left=left_rank)
                elif order == "rank_line_right" and index == 8:
                    build_string = build_string.format(rank_right=right_rank)
                print(build_string, end="", flush=True)
                time.sleep(0.005)
            print("\t", end="", flush=True)
        
        print()


if __name__ == "__main__":
    print_cards([Card(Symbols.HEART, Ascii_Rank.ACE), Card(Symbols.DIAMOND, Ascii_Rank.TEN), Card(Symbols.CLUB, Ascii_Rank.JACK), Card(Symbols.SPADE, Ascii_Rank.QUEEN)])