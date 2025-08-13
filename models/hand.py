from dataclasses import dataclass, field
from card import Card

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