import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entities.player import Poker_Player

SLEEP_TIME = 0.000075
SPACE = " "
BORDER = {"symbol": "X", "amount": 4}
EMPTY_SPACE = {"symbol": " ", "amount": None}
PLAYER_NAME = 9 
PRINT_PLAYER = 10
ADJUST_POT = 11
PRINT_POT = 12
# This allows us to find which EMPTY_SPACE amount we need to edit depending on the length or the names
PRINT_PLAYER_INDEX = [
    {"index": 5}, # player 0
    {"index": 5}, # player 9
    {"index": 5}, # player 1
    {"index": 7}, # player 8
]

PRINT_POT_INDEX = [
    {"left": 3, "right": 5}, # player 0 pot
    {"left": 5, "right": 7}, # player 9 pot
    {"left": 3, "right": 5}, # player 1 pot
    {"left": 7, "right": 9} # player 8 pot
]

PRINTED_NAMES = {
    0: {"length": None, "name": None},
    1: {"length": None, "name": None},
    2: {"length": None, "name": None},
    3: {"length": None, "name": None},
    4: {"length": None, "name": None},
    5: {"length": None, "name": None},
    6: {"length": None, "name": None},
    7: {"length": None, "name": None},
    8: {"length": None, "name": None},
    9: {"length": None, "name": None}
}

PRINTED_POT_NAME = [
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
]

SPACES_AMOUNT = {
    "big_bend_1": [
        {"index": 1, "amount": 50},
        {"index": 3, "amount": 50},
    ],
    "big_bend_2": [
        {"index": 3, "amount": 5},
        {"index": 5, "amount": 81},
        {"index": 7, "amount": 5},
    ],
    "big_bend_3": [
        {"index": 3, "amount": 8},
        {"index": 5, "amount": 85},
        {"index": 7, "amount": 8}
    ],
    "big_bend_4": [
        {"index": 1, "amount": 118}
    ],
    "big_bend_5": [
        {"index": 1, "amount": 122}
    ],
    "big_bend_6": [
        {"index": 1, "amount": 126}
    ],
    "big_bend_7": [
        {"index": 1, "amount": 61},
        {"index": 3, "amount": 60}
    ],
    "small_bend_1": [
        {"index": 1, "amount": 35},
        {"index": 3, "amount": 35}
    ],
    "small_bend_2": [
        {"index": 3, "amount": 6},
        {"index": 5, "amount": 20},
        {"index": 7, "amount": 20},
        {"index": 9, "amount": 6}
    ],
    "small_bend_3": [
        {"index": 3, "amount": 8},
        {"index": 5, "amount": 20},
        {"index": 7, "amount": 20},
        {"index": 9, "amount": 8},
    ],
    "small_bend_4": [
        {"index": 1, "amount": 35},
        {"index": 3, "amount": 35}
    ]
}

STRAIGHT = [
    {"symbol": "X", "amount": 110}
]

BIG_BEND_1 = [
    BORDER,
    EMPTY_SPACE,
    {"symbol": "DEALER", "amount": 1},
    EMPTY_SPACE,
    BORDER
]

BIG_BEND_2 = [
    PLAYER_NAME,
    PLAYER_NAME,
    BORDER,
    EMPTY_SPACE,
    PRINT_PLAYER,
    EMPTY_SPACE,
    PRINT_PLAYER,
    EMPTY_SPACE,
    BORDER
]

BIG_BEND_3 = [
    ADJUST_POT,
    ADJUST_POT,
    BORDER,
    EMPTY_SPACE,
    PRINT_POT,
    EMPTY_SPACE,
    PRINT_POT,
    EMPTY_SPACE,
    BORDER
]

BIG_BEND_4 = [
    BORDER,
    EMPTY_SPACE,
    BORDER
]

BIG_BEND_5 = [
    BORDER,
    EMPTY_SPACE,
    BORDER
]

BIG_BEND_6 = [
    BORDER,
    EMPTY_SPACE,
    BORDER
]

BIG_BEND_7 = [
    BORDER,
    EMPTY_SPACE,
    {"symbol": "THE BOARD", "amount": 1},
    EMPTY_SPACE,
    BORDER
]

SMALL_BEND_1 = [
    BORDER,
    EMPTY_SPACE,
    {"symbol": "x", "amount": 65},
    EMPTY_SPACE,
    BORDER
]

SMALL_BEND_2 = [
    PLAYER_NAME,
    PLAYER_NAME,
    BORDER,
    EMPTY_SPACE,
    PRINT_PLAYER,
    EMPTY_SPACE,
    {"symbol": "x   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   x ", "amount": 1},
    EMPTY_SPACE,
    PRINT_PLAYER,
    EMPTY_SPACE,
    BORDER
]

SMALL_BEND_3 = [
    ADJUST_POT,
    ADJUST_POT,
    BORDER,
    EMPTY_SPACE,
    PRINT_POT,
    EMPTY_SPACE,
    {"symbol": "x    │  C      │ │  C      │ │  C      │ │  C      │ │  C      │    x", "amount": 1},
    EMPTY_SPACE,
    PRINT_POT,
    EMPTY_SPACE,
    BORDER
]

SMALL_BEND_4 = [
    BORDER,
    EMPTY_SPACE,
    {"symbol": "x     │   A     │ │   A     │ │   A     │ │   A     │ │   A     │     x", "amount": 1},
    EMPTY_SPACE,
    BORDER
]

NO_BEND_1 = [
    BORDER,
    {"symbol": "                                    x     │    R    │ │    R    │ │    R    │ │    R    │ │    R    │     x                                  ", "amount": 1},
    BORDER
]

NO_BEND_2 = [
    BORDER,
    {"symbol": "                                    x     │     D   │ │     D   │ │     D   │ │     D   │ │     D   │     x                                  ", "amount": 1},
    BORDER
]


def get_amount(build_step: str, index: int) -> int:
    amount = 0
    for space in SPACES_AMOUNT[build_step]:
        if space["index"] == index:
            amount = space["amount"]
            break
    
    return amount



def update_amount(build_step: str, index: int, amount: int) -> None:
    for space in SPACES_AMOUNT[build_step]:
        if space["index"] == index:
            space["amount"] = amount
            break



def update_pot(player_pot_index: int, left_change: int, right_change: int, build_step: str) -> None:
    left, right = list(PRINT_POT_INDEX[player_pot_index].values())
    left_amount = get_amount(build_step, left)
    left_update = left_amount + left_change
    update_amount(build_step, left, left_update)

    right_amount = get_amount(build_step, right)
    right_update = right_amount + right_change
    update_amount(build_step, right, right_update)



def print_char(char: str) -> None:
    print(char, end="", flush=True)
    time.sleep(SLEEP_TIME)



def split_string(string: str) -> None:
    chars = list(string)
    for char in chars:
        print_char(char)



def adjust_name_spacing(player_index: int, build_step: str, players: list[Poker_Player]):
    player = players[player_index]
    player_name = player.name
    length = len(player_name)
    PRINTED_NAMES[player_index]["length"] = length
    PRINTED_NAMES[player_index]["name"] = player_name

    check = 9 # The 9 is the length of {PLAYER0} that we are replacing
    spacing_diff = check - length

    check_index = PRINT_PLAYER_INDEX[player_index]["index"]
    amount = get_amount(build_step, check_index)
    new_amount = amount + spacing_diff
    update_amount(build_step, check_index, new_amount)



def adjust_pot_spacing(player_pot_index: int, build_step: str, players: list[Poker_Player], left: bool):
    player_name_length = len(PRINTED_NAMES[player_pot_index]["name"])
    player = players[player_pot_index]
    money = player.money
    money_str = f"${money}"
    PRINTED_POT_NAME[player_pot_index] = money_str
    money_length = len(money_str)

    check = 7 # The length of {P0POT} that we are replacing
    player_name_mid_point = player_name_length // 2
    # we use 8 since for the name we always just add extra to the right, and {P0POT} is always 1 to the left of the starting point
    placeholder_past_mid_point = (check + 1) - player_name_mid_point
    placeholder_before_mid_point = check - placeholder_past_mid_point

    money_mid_point = money_length // 2 # this is all the values (INCLUDING) to the left of the mid
    money_past_mid = money_length - money_mid_point

    if left:
        left_add = placeholder_before_mid_point - money_mid_point
        right_add = placeholder_past_mid_point - money_past_mid
    else:
        left_add = placeholder_past_mid_point - money_past_mid
        right_add = placeholder_before_mid_point - money_mid_point
    update_pot(player_pot_index, left_add, right_add, build_step)



def print_table(players: list[Poker_Player]):
    steps = {
        "top": STRAIGHT,
        "big_bend_1": BIG_BEND_1,
        "big_bend_2": BIG_BEND_2,
        "big_bend_3": BIG_BEND_3,
        "big_bend_4": BIG_BEND_4,
        "big_bend_5": BIG_BEND_5,
        "big_bend_6": BIG_BEND_6,
        "big_bend_7": BIG_BEND_7,
        "small_bend_1": SMALL_BEND_1,
        "small_bend_2": SMALL_BEND_2,
        "small_bend_3": SMALL_BEND_3,
        "small_bend_4": SMALL_BEND_4,
        "no_bend_1": NO_BEND_1,
        "no_bend_2": NO_BEND_2
    }
    padding = 20
    player_index = 0
    player_pot_index = 0
    player_print_index = 0
    player_pot_print_index = 0
    for i, (build_step, build_item) in enumerate(steps.items()):
        # Include the padding at the start
        for _ in range(padding):
            print_char(SPACE)

        for index, step in enumerate(build_item):

            if step == EMPTY_SPACE:
                step["amount"] = get_amount(build_step, index)
            
            if step == PLAYER_NAME:
                adjust_name_spacing(player_index, build_step, players)
                player_index += 1
                continue
            
            if step == PRINT_PLAYER: # This is when we print the players name
                string = PRINTED_NAMES[player_print_index]["name"]
                split_string(string)
                player_print_index += 1
                continue

            if step == ADJUST_POT:
                adjust_pot_spacing(player_pot_index, build_step, players, player_pot_index % 2 == 0)
                player_pot_index += 1
                continue

            if step == PRINT_POT:
                string = PRINTED_POT_NAME[player_pot_print_index]
                split_string(string)
                player_pot_print_index += 1
                continue

            for _ in range(step["amount"]):
                string = step["symbol"]
                if len(string) > 1:
                    split_string(string)
                else:
                    print_char(string)
            
        print() # Printing the new line
        if i < 7:
            padding -= 2
        elif i < 12:
            padding -= 1
        
        

        


if __name__ == "__main__":


    players = {
        0: Poker_Player(2, True),
        1: Poker_Player(2, True),
        2: Poker_Player(2, True),
        3: Poker_Player(2, True),
        4: Poker_Player(2, True),
        5: Poker_Player(2, True),
        6: Poker_Player(2, True),
        7: Poker_Player(2, True),
        8: Poker_Player(2, True),
        9: Poker_Player(2, True)
    }

    players[1].name = "Wild Card Willy"
    print_table(players)