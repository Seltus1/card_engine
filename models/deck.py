from dataclasses import dataclass, field
from card import Card
from enums import Suit, Rank
from random import shuffle

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