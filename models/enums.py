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

class Poker_Value(Enum):
    ACE = 14
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

class Hands(Enum):
    ROYAL_FLUSH = 10
    STRAIGHT_FLUSH = 9
    FOUR_OF_A_KIND = 8
    FULL_HOUSE = 7
    FLUSH = 6
    STRAIGHT = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


class Poker_Bets(Enum):
    SMALL_BLIND = 1
    BIG_BLIND = 2
    ANTE = 3
    CALL = 4
    RAISE = 5
    FOLD = 6

class Poker_Game_State(Enum):
    DEAL = 1
    BETS = 2
    SHOWDOWN = 3
    REVEAL = 4
    WINNER = 5
    GAMEOVER = 6