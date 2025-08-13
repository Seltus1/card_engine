from enum import Enum

class Suit(Enum):
    SPADE = 1
    CLUB = 2
    HEART = 3
    DIAMOND = 4

class Rank(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

class Symbols(Enum):
    SPADE = '♣'
    CLUB = '♠'
    HEART = '♥'
    DIAMOND = '♦'

class Value(Enum):
    ACE = (1,11)
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 10
    QUEEN = 10
    KING = 10

class States(Enum):
    DEAL = 1
    PLAYER = 2
    #player stands
    ROUNDOVER = 3
    #Ace + 10 value on the deal
    BLACKJACK = 4
    # 9 + 10
    DEALER_PEAK = 5
    WIN = 6
    LOSE = 7
    BUST = 8
    TIE = 9