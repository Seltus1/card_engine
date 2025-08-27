import os
import sys
import time

from enum import IntEnum

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entities.player import Poker_Player


def format_money(amount: int, show_cents: bool = False) -> str:
    if show_cents:
        return f"${amount:,.2f}"
    else:
        return f"${amount:,}"


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
    SLEEP_TIME = 0.001
    LEFT = True
    RIGHT = False

    POT_LENGTH = 7                # Length of the {P#POT}
    PLAYER_LENGTH = 9             # Length of the {PLAYER#}
    STRAIGHT_LENGTH = 111         # Length of the "X" straigh


    DEALER_SPACING = 50           # The space between "DEALER" to the border
    BORDER_SPACING = 5            # Spacing from border to content

    TOP_PLAYER_BORDER_DIFF = 5    # The distance between the border and player
    TOP_PLAYER_SPACING_DIFF = 83  # The distance between player 0 and player 9

    TOP_POT_BORDER_DIFF = 8       # The distance between the border and their total money
    TOP_POT_SPACING_DIFF = 85     # The dostamce between the 2 players money
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

    BIG_BLANK_4_SPACING = 56
    BIG_BLANK_5_SPACING = 59
    BIG_BLANK_6 = 127
    SMALL_BLANK_1 = 131
    
    BOARD_SPACING = 62

    SB_3_TOTAL_SPACING = 35
    SB_3_MIDDLE_TEXT = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    SB_4_TOTAL_SPACING = 35
    SB_4_MIDDLE_TEXT = "x   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   x"
    SB_5_SPACING = 35
    SB_5_MIDDLE_TEXT = "x    │  C      │ │  C      │ │  C      │ │  C      │ │  C      │    x"

    NO_BEND_1_SPACING = 35
    NO_BEND_1_MIDDLE_TEXT = "x     │   A     │ │   A     │ │   A     │ │   A     │ │   A     │     x"
    NO_BEND_2_SPACING = 35
    NO_BEND_2_MIDDLE_TEXT = "x     │    R    │ │    R    │ │    R    │ │    R    │ │    R    │     x"

    UNDER_SB_5_SPACING = 35
    UNDER_SB_5_MIDDLE_TEXT = "x    │     D   │ │     D   │ │     D   │ │     D   │ │     D   │    x"
    UNDER_SB_4_SPACING = 35
    UNDER_SB_4_MIDDLE_TEXT = "x   │      1  │ │      2  │ │      3  │ │      4  │ │      5  │   x"
    UNDER_SB_3_SPACING = 35
    UNDER_SB_3_MIDDLE_TEXT = "x  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘  x"
    UNDER_SB_2_MIDDLE_TEXT = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    UNDER_SB_2_SPACING = 35
    UNDER_SB_1_SPACING = 131

    UNDER_BIG_BLANK_6 = 127
    UNDER_BIG_BLANK_5 = 123
    UNDER_BIG_BLANK_4 = 119
    UNDER_BIG_BLANK_3 = 115
    UNDER_BIG_BLANK_2 = 111
    UNDER_BIG_BLANK_1 = 107

    BOTTOM_PLAYER_BORDER_DIFF = 7
    P3_P4_DIFF = 21
    P4_P5_DIFF = 23
    P5_P6_DIFF = 21

    BOTTOM_MONEY_DIFF = 6
    BOTTOM_MONEY_SPACING = 23
    BOTTOM_MONEY_MIDDLE_SPACING = 25

    def __init__(self, players: list[Poker_Player], total_pot: int) -> None:
        self.border = "XXXX"
        self.players = players
        self.total_pot = total_pot
        self.build_order = {
            "straight": {
                "function": self._create_straight
            },
            "big_bend_1": {
                "function": self._print_text,
                "args": {
                    "text": "DEALER",
                    "spacing": self.DEALER_SPACING,
                    "uneven": True
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
                "function": self._print_text,
                "args": {
                    "text": "THE POT",
                    "spacing": self.BIG_BLANK_4_SPACING
                }
            },
            "big_bend_5": {
                "function": self.print_pot,
                "args": {
                    "pot": self.total_pot,
                    "spacing": self.BIG_BLANK_5_SPACING
                }
            },
            "big_bend_6": {
                "function": self.print_blank,
                "args": {
                    "x": self.BIG_BLANK_6
                }
            },
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
                    "string1": format_money(self.players[Player.PLAYER1].money),
                    "string2": format_money(self.players[Player.PLAYER8].money),
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
                    "string1": format_money(self.players[Player.PLAYER1].money),
                    "string2": format_money(self.players[Player.PLAYER8].money),
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
                "function": self.setup_bottom_players,
                "args": {
                    "player3": self.players[Player.PLAYER3],
                    "player4": self.players[Player.PLAYER4],
                    "player5": self.players[Player.PLAYER5],
                    "player6": self.players[Player.PLAYER6],
                }
            },
            "under_big_bend_2": {
                "function": self.setup_bottom_pot,
                "args": {
                    "player3": self.players[Player.PLAYER3],
                    "player4": self.players[Player.PLAYER4],
                    "player5": self.players[Player.PLAYER5],
                    "player6": self.players[Player.PLAYER6],
                }
            },
            "under_big_bend_1": {
                "function": self.print_blank,
                "args": {
                    "x": self.UNDER_BIG_BLANK_1
                }
            },
            "under_straight": {
                "function": self._create_straight
            }
        }
    


    def _create_space(self, x: int) -> str:
        string = []
        for _ in range(x):
            string.append(" ")
        
        return "".join(string)



    def _create_straight(self) -> None:
        string = "".join(["X" for _ in range(self.STRAIGHT_LENGTH)])
        self.print_string(string)
    


    def _print_text(self, text: str, spacing: int, uneven: bool = False) -> None:
        build_order = [
            self.border,
            self._create_space(spacing),
            text,
            self._create_space(spacing),
            self.border
        ]

        if uneven:
            build_order[3] = self._create_space(spacing + 1)

        for order in build_order:
            self.print_string(order)

    

    def _update_diff_between_players(self, left_name: str, right_name: str, diff: int) -> int:
        left_len, right_len = len(left_name), len(right_name)

        new_diff = diff
        left_diff = self.PLAYER_LENGTH - left_len
        new_diff += left_diff      
        
        right_diff = self.PLAYER_LENGTH - right_len   
        new_diff += right_diff

        return new_diff
    


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
        left_money_str = format_money(left_money)
        right_money_str = format_money(right_money)

        left_change, right_change = self._normalize_pot_diff(left_name, left_money_str, self.LEFT)

        left = self.TOP_POT_BORDER_DIFF + left_change
        mid = self.TOP_POT_SPACING_DIFF - right_change

        left_change, right_change = self._normalize_pot_diff(right_name, right_money_str, self.RIGHT)

        mid += left_change
        right = self.TOP_POT_BORDER_DIFF + right_change
        return left, mid, right
    


    def _center_text(self, text: str, total_spacing: int) -> tuple[int, int]:
        name_length = len(text)
        leftover_space = total_spacing - name_length
        left_add = leftover_space // 2
        right_add = leftover_space - left_add
        return left_add, right_add
    


    def _edit_bottom_distance(self, text: str, is_player: bool) -> tuple[int, int]:
        text_len = len(text)
        place_holder = self.PLAYER_LENGTH if is_player else self.POT_LENGTH
        diff = text_len - place_holder
        left_diff = diff // 2
        right_diff = diff - left_diff
        return left_diff, right_diff



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
            format_money(player0.money),
            self._create_space(mid),
            format_money(player9.money),
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
    


    def print_pot(self, pot: int, spacing: int) -> None:
        length = len(format_money(pot)) 
        diff = length - 5
        left_diff = diff // 2
        right_diff = diff - left_diff

        left = spacing - left_diff
        right = spacing - right_diff

        build_order = [
            self.border,
            self._create_space(left),
            format_money(pot),
            self._create_space(right),
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
    


    def setup_bottom_players(self, player3: Poker_Player, player4: Poker_Player, player5: Poker_Player, player6: Poker_Player) -> None:
        spaces = [
            self.TOP_POT_BORDER_DIFF,       # space1: between border and player3
            self.P3_P4_DIFF,                # space2: between player3 and player4
            self.P4_P5_DIFF,                # space3: between player4 and player5
            self.P5_P6_DIFF,                # space4: between player5 and player6
            self.BOTTOM_PLAYER_BORDER_DIFF  # space5: between player6 and border
        ]

        players = [player3, player4, player5, player6]
        for i in range(len(players)):
            left_change, right_change = self._edit_bottom_distance(players[i].name, True)
            spaces[i] -= left_change        # Adjust left spacing
            spaces[i + 1] -= right_change   # Adjust right spacing

        space1, space2, space3, space4, space5 = spaces
        
        build_order = [
            self.border,
            self._create_space(space1),
            player3.name,
            self._create_space(space2),
            player4.name,
            self._create_space(space3),
            player5.name,
            self._create_space(space4),
            player6.name,
            self._create_space(space5),
            self.border
        ]

        for order in build_order:
            self.print_string(order)
    


    def setup_bottom_pot(self, player3: Poker_Player, player4: Poker_Player, player5: Poker_Player, player6: Poker_Player) -> None:
        spaces = [
            self.BOTTOM_MONEY_DIFF,
            self.BOTTOM_MONEY_SPACING,
            self.BOTTOM_MONEY_MIDDLE_SPACING,
            self.BOTTOM_MONEY_SPACING,
            self.BOTTOM_MONEY_DIFF
        ]

        players = [player3, player4, player5, player6]
        for i in range(len(players)):
           left_change, right_change = self._edit_bottom_distance(format_money(players[i].money), False)
           spaces[i] -= left_change
           spaces[i + 1] -= right_change

        space1, space2, space3, space4, space5 = spaces

        build_order = [
            self.border,
            self._create_space(space1),
            format_money(player3.money),
            self._create_space(space2),
            format_money(player4.money),
            self._create_space(space3),
            format_money(player5.money),
            self._create_space(space4),
            format_money(player6.money),
            self._create_space(space5),
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
            
            if count < 7:
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
    total_pot = 10000
    table = Table(dummy_players, total_pot)
    table.print_table()