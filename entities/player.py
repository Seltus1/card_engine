from entities.entity import Entity
class Player(Entity): 
    def __init__(self, hand_limit: int = None):
        super().__init__(hand_limit)
        self.has_natural_blackjack = False
        self.total_money: int = 0
        self.curr_bet: int = 0

    def __str__(self):
        return (f"The player has {self.hand.hand_size}")
    
    def decide_action(self, prompt: str = ""):
        return input(prompt)
    
    def increase_bet(self, bet: int):
        self.curr_bet += bet
    
    def reset(self):
        super().reset()
        self.has_natural_blackjack = False
        self.curr_bet = 0
        