from entities.entity import Entity
from models.cards import Deck

class Dealer(Entity): 

    def __init__(self, hand_limit: int = None):
        super().__init__(hand_limit)
        self.up_card = None
        self.hole_card = None
    
    def __str__(self):
        return (f"The Dealer has {self.hand.hand_size}")
    

    #must hit if score below 16, dealer hits on soft 17, stop at hard 17
    def hard17(self, deck: Deck):
        self.hand.update_score(self.hand.hand_score())
        if self.get_hard_score() == 21:
            return
        if self.get_hard_score() >= 17:
            return
        while self.get_hard_score() < 17 or (self.get_soft_score() < 17 and self.get_soft_score() != 0):
            self.hand.add_card(deck.deal_card(True))
            self.hand.update_score(self.hand.hand_score())
    def get_up_card(self):
        if len(self.hand.cards) != 0:
            return self.hand.cards[0]
        else:
            print("Dealer has no cards")