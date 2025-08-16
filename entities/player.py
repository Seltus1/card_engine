import random

from entities.entity import Entity
from models.cards import Card, Hand

class Player(Entity): 
    def __init__(self, hand_limit: int = None):
        super().__init__(hand_limit)
        self.has_natural_blackjack = False
        self.total_money: int = 0
        self.curr_bet: int = 0
        self.seen_cards: list[Card] = []
        self.split_hand: Hand
        self.split_choice = False 

    def __str__(self):
        return (f"The player has {self.hand.hand_size}")
    
    def decide_action(self, prompt: str = ""):
        return input(prompt).lower()
    
    def increase_bet(self, bet: int):
        self.curr_bet += bet


    def add_card(self, card: Card):
        self.hand.add_card(card)
        self.seen_cards.append(card)
        

    def check_for_split(self):
        #thanks ethan v2
        return self.hand.cards[0].rank == self.hand.cards[1].rank
    
    def make_split_hand(self):
        self.split_hand = Hand.create_hand(10)
        self.split_hand.cards.append(self.hand.cards.pop())
    
    
    def reset(self):
        super().reset()
        self.has_natural_blackjack = False



class Poker_Player(Entity):

    def __init__(self, hand_limits: int = None, bot: bool = True):
        super().__init__(hand_limits)
        self.bot = bot
        self.chips = 250
        self.round_bet = 0
        self.name = self.get_name()
    


    def get_name(self) -> str:
        funny_names = [
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
        if self.bot:
            return random.choice(funny_names)
        return "YOU THE PERSON"
