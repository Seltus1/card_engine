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
    
    def hand_score(self) -> int:
        total = 0
        if self.hand.hand_size == 0:
            return total
        has_ace = self.hand.contains_rank("ACE")
        
        if has_ace:
            low_total = 0
            for card in self.hand.cards:
                if card.rank == "ACE":
                    ace_values = Value[card.rank].value
                    low_total += ace_values[0]
                    total += ace_values[1]
                    continue
                low_total += Value[card.rank].value
                total += Value[card.rank].value
            self.update_score((low_total,total))
            return (low_total,total)
        
        else:
            total += sum(Value[card.rank].value for card in self.hand.cards)
            self.update_score(total)
            return total
    
    def update_score(self, score):
        
        if isinstance(score, tuple):
            self.soft_score = score[0]
            self.hard_score = score[1]
        else:
            self.hard_score = score

    def get_max_valid_score(self):
        if self.hard_score == 21 or self.soft_score == 21:
            return 21
        elif self.hard_score > 21:
            if self.soft_score != 0 and self.soft_score < 22:
                return self.soft_score
            else:
                return 21 - self.hard_score
        else:
            return max(self.hard_score, self.soft_score)

    def get_soft_score(self) -> int:
        return self.soft_score
    
    def get_hard_score(self) -> int:
        return self.hard_score
    
    def reset(self):
        self.hand: Hand = Hand.create_hand(self.hand_limit)
        self.hard_score = 0
        self.soft_score = 0