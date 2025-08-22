import random

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



POKER_NAMES = [
    "All-In Annie",
    "Bluffing Bob",
    "Card Shark Charlie",
    "Diamond Dave",
    "Easy Money Eddie",
    "Folding Fred",
    "Going Broke Gary",
    "High Roller Harry",
    "Impatient Irene",
    "Jackpot Jimmy",
    "King Kong Kenny",
    "Lucky Lucy",
    "Money Bags Mike",
    "No Luck Nick",
    "One-Eyed Pete",
    "Poker Face Paul",
    "Queen Bee Quinn",
    "River Rat Randy",
    "Straight Face Steve",
    "Texas Hold'em Tom",
    "Unlucky Ursula",
    "Vegas Vic",
    "Wild Card Willy",
    "X-Factor Xavier",
    "Yolo Yolanda"
]



class Poker_Player(Entity):

    def __init__(self, hand_limits: int = None, bot: bool = True):
        super().__init__(hand_limits)
        self.bot = bot
        self.money = 250
        self.round_bet = 0
        self.best_hand = None
        self.name = self.get_name()
    


    def get_name(self) -> str:
        if self.bot:
            name = random.choice(POKER_NAMES)
            POKER_NAMES.remove(name)
            return name
        return "YOU THE PERSON"
