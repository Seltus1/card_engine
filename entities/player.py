from entities.entity import Entity
class Player(Entity): 
    def __init__(self, hand_limit: int = None):
        super().__init__(hand_limit)
        self.has_natural_blackjack = False
    def __str__(self):
        return (f"The player has {self.hand.hand_size}")
    
    def decide_action(self):
        return input()
    
    def reset(self):
        super().reset()
        self.has_natural_blackjack = False
        