import time
import random
import os
from dataclasses import dataclass, field
from models.enums import *
from random import shuffle


@dataclass(frozen=True)
class Card:
    suit: str
    rank: int

    def __str__(self):
        print_cards([self])
        return ""
    
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
        for suit_index in range(1,5):
            for rank_index in range (1,14):
                play_deck.cards.append(Card(Suit(suit_index).name, Rank(rank_index).name))
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
        print_cards(self.cards)
        return ""


def get_ranks(card: Card):
    value = Ascii_Rank[card.rank].value
    right_rank = value + " " if value != "10" else "10"
    left_rank = " " + value if value != "10" else "10"
    return left_rank, right_rank

def get_ranks(card: Card) -> tuple[str, str]:
    right_rank = card.rank.value + " " if card.rank.value != "10" else "10"
    left_rank = " " + card.rank.value if card.rank.value != "10" else "10"
    return right_rank, left_rank
def determineCardColor(suit):
    match suit:
        case Symbols.HEART:
            return "\033[91m"
        case Symbols.DIAMOND:
            return "\033[38;5;214m"
        case Symbols.SPADE:
            return "\033[92m"
        case Symbols.CLUB:
            return "\033[94m"


def print_cards(cards: list[Card]):
    os.system('color')
    card_builder = {
        "top":             ["┌", "─", "─", "─", "─", "─", "─", "─", "─", "─┐"],
        "bottom":          ["└", "─", "─", "─", "─", "─", "─", "─", "─", "─┘"],
        "side":            ["│", " ", " ", " ", " ", " ", " ", " ", " ", " ", "│"],
        "suit_line":       ["│", " ", " ", " ", " ", "{symbol}", " ", " ", " ", " ", "│"],
        "rank_line_left":  ["│", "{rank_left}", " ", " ", " ", " ", " ", " ", " ", "│"],
        "rank_line_right": ["│", " ", " ", " ", " ", " ", " ", " ", "{rank_right}", "│"],
    }
    build_order = ["top", "rank_line_left", "side", "suit_line", "side", "rank_line_right", "bottom"]

    card_print
    skipables = ["bottom", "side", "suit_line", "rank_line_left", "rank_line_right"]
    skip_7 = ["rank_line_left"]
    skip_8 = ["side", "bottom", "suit_line", "rank_line_right"]

    count = 0
    card_location = {}
    for card in cards:
        card_location[card] = count
        count -= 1

    padding = ""
    card_print
    sleepTime = .03
    decay = .00025
    minSleepTime = .008
    while len(card_location) > 0:
        cards_to_print = len(card_location)
        for card in card_location:
            if card_location[card] < 0:
                cards_to_print -= 1
                continue
            
        for card_index, (card, build_index) in enumerate(card_location.items()):
            if build_index < 0:
                card_location[card] += 1
                continue

            order = build_order[build_index]
            left_rank, right_rank = get_ranks(card)
            can_skip = card_index < cards_to_print - 1
            for index, build_string in enumerate(card_builder[order]):

                # Checking when to stop printing for this card
                if can_skip and order in skip_7 and index == 7:
                    break

                if can_skip and order in skip_8 and index == 8:
                    break
                card_print

                if order == "suit_line" and index == 5:
                    build_string = build_string.format(symbol=Symbols[card.suit].value)
                elif order == "rank_line_left" and index == 1:
                    build_string = build_string.format(rank_left=left_rank)
                elif order == "rank_line_right" and index == 8:
                    build_string = build_string.format(rank_right=right_rank)

                first_print = card_index == 0 and index == 0
                
                if padding != "" and first_print:
                    build_string = padding + build_string
                 card_print
                cardColor = determineCardColor(card.suit)
                print(f"{cardColor}{build_string}\x1b[0m", end="", flush=True)
                time.sleep(sleepTime)
                sleepTime -= decay
                if(sleepTime < minSleepTime):
                    sleepTime = minSleepTime

                print(build_string, end="", flush=True)
                time.sleep(0.005)
            
            card_location[card] += 1
        
        delete_cards = None
        for card in card_location:
            if card_location[card] >= 7:
                delete_cards = card
                break
        
        if delete_cards is not None:
            del card_location[delete_cards]
            padding += " " * 8
         card_print

        print()

        print()

if __name__ == "__main__":
    card_print
    cards = []
    for i in range(10):
        random_suit = random.choice(list(Symbols))
        random_rank = random.choice(list(Ascii_Rank))
        random_card = Card(random_suit, random_rank)
        cards.append(random_card)

        print_cards(cards)

    print_cards([Card(Suit.SPADE, Rank.TEN), Card(Suit.DIAMOND, Rank.TEN), Card(Suit.CLUB, Rank.JACK), Card(Suit.SPADE, Rank.QUEEN)])
