from dataclasses import dataclass
from enums import *
@dataclass(frozen=True)
class Card:
    suit: str
    rank: int

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
    def print_card(self, rank, suit):
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
            rank_right = self.rank
            rank_left = self.rank
        else:
            rank_right = self.rank + " "
            rank_left = " " + self.rank

        suit_line = f"│    {self.suit}    │"
        rank_line_left = f"│{rank_left}       │"
        rank_line_right = f"│       {rank_right}│"

        print(top)
        print(rank_line_left)
        print(side)
        print(suit_line)
        print(side)
        print(rank_line_right)
        print(bottom)

