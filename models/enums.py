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

class Ascii_Rank(Enum):
    ACE = "A"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"

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
    DEAL = "DEAL" #1
    PLAYER = "PLAYER" #2
    #player stands
    ROUNDOVER = "ROUNDOVER" #3
    #Ace + 10 value on the deal
    BLACKJACK = "glizzymaxx!!!" #4
    # 9 + 10
    DEALER_PEAK = "DEALER_PEAK" #5
    WIN = "ONE MORE ROUND CANT HURT" #6
    LOSE = "TRY AGAIN, NERD!" #7
    BUST = "GREEDY OR UNLUCKY..?" #8
    TIE = "It's always been rigged.." #9
    CHOOSE = "CHOOSE"
    GAMEOVER = "GAMEOVER"