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
        self.curr_bet = 0
        