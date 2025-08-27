from models.cards import Hand
from models.enums import *
class Entity:


    def __init__(self, hand_limit: int = None):
        if hand_limit:
            self.hand_limit = hand_limit
            self.hand: Hand = Hand.create_hand(hand_limit)
        else:
            self.hand_limit = 100
            self.hand: Hand = Hand.create_hand(hand_limit)
        self.soft_score = 0
        self.hard_score = 0
    
    def get_soft_score(self) -> int:
        return self.hand.get_soft_score()
    


    def get_hard_score(self) -> int:
        return self.hand.get_hard_score()
    

    
    def reset(self):
        self.hand: Hand = Hand.create_hand(self.hand_limit)
        