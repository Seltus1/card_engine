import os
import sys
import time

from enum import IntEnum

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entities.player import Poker_Player


class Player(IntEnum):
    PLAYER0 = 0
    PLAYER1 = 1
    PLAYER2 = 2
    PLAYER3 = 3
    PLAYER4 = 4
    PLAYER5 = 5
    PLAYER6 = 6
    PLAYER7 = 7
    PLAYER8 = 8
    PLAYER9 = 9



class Table:
    SLEEP_TIME = 0.000001
    LEFT = True
    RIGHT = False

    POT_LENGTH = 7                # Length of the {P#POT}
    PLAYER_LENGTH = 9             # Length of the {PLAYER#}
    STRAIGHT_LENGTH = 110         # Length of the "X" straigh

    DEALER_SPACING = 50           # The space between "DEALER" to the border
    BORDER_SPACING = 5            # Spacing from border to content

    TOP_PLAYER_BORDER_DIFF = 5    # The distance between the border and player
    TOP_PLAYER_SPACING_DIFF = 82  # The distance between player 0 and player 9

    TOP_POT_BORDER_DIFF = 8       # The distance between the border and their total money
    TOP_POT_SPACING_DIFF = 84     # The dostamce between the 2 players money
    TOP_POT_SPACING = {
        True: {
            "start_player_index": 25,
            "start_money_index": 26,
            "end_money_index": 33
        },
        False: {
            "start_player_index": 125,
            "start_money_index": 124,
            "end_money_index": 118
        }
    }

    BIG_BLANK_4 = 119
    BIG_BLANK_5 = 123
    BIG_BLANK_6 = 127
    BIG_BLANK_7 = 131
    SMALL_BLANK_1 = 133
    
    BOARD_SPACING = 63

    SB_3_TOTAL_SPACING = 36
    SB_3_MIDDLE_TEXT = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    SB_4_TOTAL_SPACING = 36
    SB_4_MIDDLE_TEXT = "x   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   x"
    SB_5_SPACING = 36
    SB_5_MIDDLE_TEXT = "x    │  C      │ │  C      │ │  C      │ │  C      │ │  C      │    x"

    NO_BEND_1_SPACING = 36
    NO_BEND_1_MIDDLE_TEXT = "x     │   A     │ │   A     │ │   A     │ │   A     │ │   A     │     x"
    NO_BEND_2_SPACING = 36
    NO_BEND_2_MIDDLE_TEXT = "x     │    R    │ │    R    │ │    R    │ │    R    │ │    R    │     x"

    UNDER_SB_5_SPACING = 36
    UNDER_SB_5_MIDDLE_TEXT = "x    │     D   │ │     D   │ │     D   │ │     D   │ │     D   │    x"
    UNDER_SB_4_SPACING = 36
    UNDER_SB_4_MIDDLE_TEXT = "x   │      1  │ │      2  │ │      3  │ │      4  │ │      5  │   x"
    UNDER_SB_3_SPACING = 36
    UNDER_SB_3_MIDDLE_TEXT = "x  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘  x"
    UNDER_SB_2_MIDDLE_TEXT = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    UNDER_SB_2_SPACING = 36
    UNDER_SB_1_SPACING = 133

    UNDER_BIG_BLANK_6 = 129
    UNDER_BIG_BLANK_5 = 125
    UNDER_BIG_BLANK_4 = 121
    UNDER_BIG_BLANK_3 = 117
    UNDER_BIG_BLANK_2 = 113
    UNDER_BIG_BLANK_1 = 109

    def __init__(self, players: list[Poker_Player]) -> None:
        self.border = "XXXX"
        self.players = players
        self.build_order = {
            "straight": {
                "function": self._create_straight
            },
            "big_bend_1": {
                "function": self._print_text,
                "args": {
                    "text": "DEALER",
                    "spacing": self.DEALER_SPACING
                }
            },
            "big_bend_2": {
                "function": self.setup_top_players,
                "args": {
                    "player0": self.players[Player.PLAYER0],
                    "player9": self.players[Player.PLAYER9],
                }
            },
            "big_bend_3": {
                "function": self.setup_top_pot,
                "args": {
                    "player0": self.players[Player.PLAYER0],
                    "player9": self.players[Player.PLAYER9],
                }
            },
            "big_bend_4": {
                "function": self.print_blank,
                "args": {
                    "x": self.BIG_BLANK_4
                }
            },
            "big_bend_5": {
                "function": self.print_blank,
                "args": {
                    "x": self.BIG_BLANK_5
                }
            },
            "big_bend_6": {
                "function": self.print_blank,
                "args": {
                    "x": self.BIG_BLANK_6
                }
            },
            # "big_bend_7": {
            #     "function": self.print_blank,
            #     "args": {
            #         "x": self.BIG_BLANK_7
            #     }
            # },
            "small_bend_1": {
                "function": self.print_blank,
                "args": {
                    "x": self.SMALL_BLANK_1
                }
            },
            "small_bend_2": {
                "function": self._print_text,
                "args": {
                    "text": "The Board",
                    "spacing": self.BOARD_SPACING
                }
            },
            "small_bend_3": {
                "function": self.setup_middle,
                "args": {
                    "string1": self.players[Player.PLAYER1].name,
                    "string2": self.players[Player.PLAYER8].name,
                    "spacing": self.SB_3_TOTAL_SPACING,
                    "middle_text": self.SB_3_MIDDLE_TEXT
                }
            },
            "small_bend_4": {
                "function": self.setup_middle,
                "args": {
                    "string1": f"${self.players[Player.PLAYER1].money}",
                    "string2": f"${self.players[Player.PLAYER8].money}",
                    "spacing": self.SB_4_TOTAL_SPACING,
                    "middle_text": self.SB_4_MIDDLE_TEXT
                }
            },
            "small_bend_5": {
                "function": self._print_text,
                "args": {
                    "text": self.SB_5_MIDDLE_TEXT,
                    "spacing": self.SB_5_SPACING
                }
            },
            "no_bend_1": {
                "function": self._print_text,
                "args": {
                    "text": self.NO_BEND_1_MIDDLE_TEXT,
                    "spacing": self.NO_BEND_1_SPACING
                }
            },
            "no_bend_2": {
                "function": self._print_text,
                "args": {
                    "text": self.NO_BEND_2_MIDDLE_TEXT,
                    "spacing": self.NO_BEND_2_SPACING
                }
            },
            "under_small_bend_5": {
                "function": self._print_text,
                "args": {
                    "text": self.UNDER_SB_5_MIDDLE_TEXT,
                    "spacing": self.UNDER_SB_5_SPACING
                }
            },
            "under_small_bend_4": {
                "function": self.setup_middle,
                "args": {
                    "string1": self.players[Player.PLAYER2].name,
                    "string2": self.players[Player.PLAYER7].name,
                    "spacing": self.UNDER_SB_4_SPACING,
                    "middle_text": self.UNDER_SB_4_MIDDLE_TEXT
                }
            },
            "under_small_bend_3": {
                "function": self.setup_middle,
                "args": {
                    "string1": f"${self.players[Player.PLAYER1].money}",
                    "string2": f"${self.players[Player.PLAYER8].money}",
                    "spacing": self.UNDER_SB_3_SPACING,
                    "middle_text": self.UNDER_SB_3_MIDDLE_TEXT
                }
            },
            "under_small_bend_2": {
                "function": self._print_text,
                "args": {
                    "text": self.UNDER_SB_2_MIDDLE_TEXT,
                    "spacing": self.UNDER_SB_2_SPACING
                }
            },
            "under_small_bend_1": {
                "function": self.print_blank,
                "args": {
                    "x": self.UNDER_SB_1_SPACING
                }
            },
            "under_big_bend_6": {
                "function": self.print_blank,
                "args": {
                    "x": self.UNDER_BIG_BLANK_6
                }
            },
            "under_big_bend_5": {
                "function": self.print_blank,
                "args": {
                    "x": self.UNDER_BIG_BLANK_5
                }
            },
            "under_big_bend_4": {
                "function": self.print_blank,
                "args": {
                    "x": self.UNDER_BIG_BLANK_4
                }
            },
            "under_big_bend_3": {
                "function": self.print_blank,
                "args": {
                    "x": self.UNDER_BIG_BLANK_3
                }
            },
            "under_big_bend_2": {
                "function": self.print_blank,
                "args": {
                    "x": self.UNDER_BIG_BLANK_2
                }
            },
            "under_big_bend_1": {
                "function": self.print_blank,
                "args": {
                    "x": self.UNDER_BIG_BLANK_1
                }
            },
            "under_straight": {
                "function": self._create_straight,
                "args": {
                    "end": True
                }
            }
        }
    


    def _create_space(self, x: int) -> str:
        string = []
        for _ in range(x):
            string.append(" ")
        
        return "".join(string)



    def _create_straight(self, end=False) -> None:
        length = self.STRAIGHT_LENGTH if not end else self.STRAIGHT_LENGTH + 3
        string = "".join(["X" for _ in range(length)])
        self.print_string(string)
    


    def _print_text(self, text: str, spacing: int) -> None:
        build_order = [
            self.border,
            self._create_space(spacing),
            text,
            self._create_space(spacing),
            self.border
        ]

        for order in build_order:
            self.print_string(order)

    

    def _update_diff_between_players(self, left_name: str, right_name: str, diff: int) -> int:
        left_len, right_len = len(left_name), len(right_name)

        new_diff = diff
        left_diff = self.PLAYER_LENGTH - left_len
        new_diff += left_diff      
        
        right_diff = self.PLAYER_LENGTH - right_len   
        new_diff += right_diff

        return new_diff + 1
    


    def _normalize_pot_diff(self, name: str, money_str: str, side: bool):
        start_player_index = self.TOP_POT_SPACING[side]["start_player_index"]
        start_money_index = self.TOP_POT_SPACING[side]["start_money_index"]
        end_money_index = self.TOP_POT_SPACING[side]["end_money_index"]

        name_mid_length = len(name) // 2
        new_player_mid = start_player_index + name_mid_length if side else start_player_index - name_mid_length

        money_length = len(money_str)
        money_mid = money_length // 2
        money_end = new_player_mid + len(money_str[money_mid:]) if side else new_player_mid - len(money_str[:money_mid - 1])

        left_diff = (new_player_mid - len(money_str[:money_mid])) - start_money_index if side else money_end - end_money_index
        right_diff = money_end - end_money_index if side else start_money_index - (new_player_mid + len(money_str[money_mid:]))

        return left_diff, right_diff
    


    def _update_diff_between_pots(self, left_name: str, left_money: int, right_name: str, right_money: int):
        left_money_str = f"${left_money}"
        right_money_str = f"${right_money}"

        left_change, right_change = self._normalize_pot_diff(left_name, left_money_str, self.LEFT)

        left = self.TOP_POT_BORDER_DIFF + left_change
        mid = self.TOP_POT_SPACING_DIFF - right_change

        left_change, right_change = self._normalize_pot_diff(right_name, right_money_str, self.RIGHT)

        mid += left_change
        right = self.TOP_POT_BORDER_DIFF + right_change
        return left, mid + 1, right
    


    def _center_text(self, text: str, total_spacing: int) -> tuple[int, int]:
        name_length = len(text)
        leftover_space = total_spacing - name_length
        left_add = leftover_space // 2
        right_add = leftover_space - left_add
        return left_add, right_add



    def print_string(self, string: str) -> None:
        for char in string:
            print(char, end="", flush=True)
            time.sleep(self.SLEEP_TIME)



    def setup_top_players(self, player0: Poker_Player, player9: Poker_Player) -> None:
        new_diff = self._update_diff_between_players(player0.name, player9.name, self.TOP_PLAYER_SPACING_DIFF)

        build_steps = [
            self.border,
            self._create_space(self.BORDER_SPACING),
            player0.name,
            self._create_space(new_diff),
            player9.name,
            self._create_space(self.BORDER_SPACING),
            self.border
        ]

        for step in build_steps:
            self.print_string(step)

        return build_steps
    


    def setup_top_pot(self, player0: Poker_Player, player9: Poker_Player) -> None:
        left, mid, right = self._update_diff_between_pots(player0.name, player0.money, player9.name, player9.money)
        build_order = [
            self.border,
            self._create_space(left),
            f"${player0.money}",
            self._create_space(mid),
            f"${player9.money}",
            self._create_space(right),
            self.border
        ]

        for order in build_order:
            self.print_string(order)
    


    def print_blank(self, x: int) -> None:
        build_order = [
            self.border,
            self._create_space(x),
            self.border
        ]

        for order in build_order:
            self.print_string(order)
    


    def setup_middle(self, string1: str, string2: str, spacing: int, middle_text: str) -> None:
        player1_left, player1_right = self._center_text(string1, spacing)
        player2_left, player2_right = self._center_text(string2, spacing)
        build_order = [
            self.border,
            self._create_space(player1_left),
            string1,
            self._create_space(player1_right),
            middle_text,
            self._create_space(player2_left),
            string2,
            self._create_space(player2_right),
            self.border
        ]

        for order in build_order:
            self.print_string(order)
    


    def print_table(self):
        padding = 20

        for count, order in enumerate(self.build_order):
            pad = "".join([" " for _ in range(padding)])
            self.print_string(pad)

            # Check if this function call has arguments
            if "args" in self.build_order[order]:
                # Call function with unpacked arguments using **kwargs
                self.build_order[order]["function"](**self.build_order[order]["args"])
            else:
                # Call function without arguments
                self.build_order[order]["function"]()
            
            if count < 6:
                padding -= 2
            elif count < 12:
                padding -= 1
            elif count < 13:
                padding += 0
            elif count < 18:
                padding += 1
            elif count >= 18:
                padding += 2

            
            print() # Adding a new line




if __name__ == "__main__":
    # Create dummy players for testing
    dummy_players = [Poker_Player(2, True) for i in range(10)]
    table = Table(dummy_players)
    table.print_table()