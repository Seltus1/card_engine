import os
import sys
import time
import shutil

from typing import List
from enum import IntEnum

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.cards import Card
from entities.player import Poker_Player
from models.enums import Ascii_Rank, Symbols
from utils.table_config import TableConfigManager, LayoutSection


def format_money(amount: int, show_cents: bool = False) -> str:
    if show_cents:
        return f"${amount:,.2f}"
    else:
        return f"${amount:,}"


MAX_TABLE_WIDTH = 149


def center_text() -> str:
    terminal_width = shutil.get_terminal_size().columns
    padding = " " * ((terminal_width - MAX_TABLE_WIDTH) // 2)
    return padding


CENTER_SCREEN_PADDING = center_text()


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


class TableRenderer:
    SLEEP_TIME = 0.00001
    LEFT = True
    RIGHT = False

    POT_LENGTH = 7
    PLAYER_LENGTH = 9
    STRAIGHT_LENGTH = 111

    TOP_PLAYER_BORDER_DIFF = 5
    TOP_PLAYER_SPACING_DIFF = 83
    TOP_POT_BORDER_DIFF = 8
    TOP_POT_SPACING_DIFF = 85
    
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

    P3_P4_DIFF = 21
    P4_P5_DIFF = 23
    P5_P6_DIFF = 21
    BOTTOM_PLAYER_BORDER_DIFF = 7
    BOTTOM_MONEY_DIFF = 6
    BOTTOM_MONEY_SPACING = 23
    BOTTOM_MONEY_MIDDLE_SPACING = 25

    def __init__(self, players: List[Poker_Player], total_pot: int, river: list[Card], config_path: str = None):
        self.border = "XXXX"
        self.players = players
        self.total_pot = total_pot
        self.river = river
        
        # Default config path
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "config", "table_layout.json"
            )
        
        self.config_manager = TableConfigManager(config_path)



    def _create_space(self, x: int) -> str:
        return " " * x



    def _print_order(self, order: List[str]) -> None:
        self.print_string(CENTER_SCREEN_PADDING)
        for step in order:
            self.print_string(step)



    def print_string(self, string: str) -> None:
        for char in string:
            print(char, end="", flush=True)
            time.sleep(self.SLEEP_TIME)



    def create_straight(self) -> None:
        string = "X" * self.STRAIGHT_LENGTH
        self._print_order([string])
    


    def _find_char_index(self, text: str, char: str, amount: int) -> list[int]:
        index = 0
        indices = []
        while len(indices) < amount:
            curr = text[index]
            if curr == char or (curr in ["1", "2", "3", "4", "5"] and char == "#"):
                indices.append(index)
            index += 1
        return indices



    def _alter_card_text(self, text: str) -> str:
        replacements = [
            "│  C      │",
            "│   A     │",
            "│    R    │",
            "│     D   │",
            "│      1  │"
        ]

        symbols = ["C", "A", "R", "D", "#"]

        change = -1
        for index, rep in enumerate(replacements):
            if rep in text:
                change = index
                break
        
        if change == -1:
            return text
        
        symbol = symbols[change]
        river_length = len(self.river)
        indices = self._find_char_index(text, symbol, river_length)
        text = list(text)

        for card_index, index in enumerate(indices):
            match symbol:
                case "C":
                    rank = Ascii_Rank[self.river[card_index].rank].value
                    if rank == "10":
                        text[index] = "1"
                        text[index + 1] = "0"
                    else:
                        text[index] = rank

                case "A":
                    text[index] = " "

                case "R":
                    card_symbol = Symbols[self.river[card_index].suit].value
                    text[index] = card_symbol

                case "D":
                    text[index] = " "

                case "#":
                    rank = Ascii_Rank[self.river[card_index].rank].value
                    if rank == "10":
                        text[index - 1] = "1"
                        text[index] = "0"
                    else:
                        text[index] = rank
        
        return "".join(text)





    def _print_text(self, text: str, spacing: int, uneven: bool = False) -> None:
        text = self._alter_card_text(text)
        build_order = [
            self.border,
            self._create_space(spacing),
            text,
            self._create_space(spacing + (1 if uneven else 0)),
            self.border
        ]
        self._print_order(build_order)



    def print_blank(self, spacing: int) -> None:
        build_order = [
            self.border,
            self._create_space(spacing),
            self.border
        ]
        self._print_order(build_order)



    def print_pot(self, spacing: int) -> None:
        pot_str = format_money(self.total_pot)
        length = len(pot_str)
        diff = length - 5
        left_diff = diff // 2
        right_diff = diff - left_diff

        left = spacing - left_diff
        right = spacing - right_diff

        build_order = [
            self.border,
            self._create_space(left),
            pot_str,
            self._create_space(right),
            self.border
        ]
        self._print_order(build_order)



    def _get_player_data(self, player_key: str, data_type: str = "name") -> str:
        player_index = getattr(Player, player_key)
        player = self.players[player_index]
        
        if data_type == "name":
            return player.name
        elif data_type == "money":
            return format_money(player.money)
        else:
            raise ValueError(f"Unknown data type: {data_type}")



    def _resolve_function_args(self, section: LayoutSection) -> dict:
        args = {}
        
        if section.text is not None:
            args['text'] = section.text
        if section.spacing is not None:
            args['spacing'] = section.spacing
        if section.uneven is not None:
            args['uneven'] = section.uneven
        
        # Handle player-specific arguments
        if section.players:
            if section.function == "setup_top_players":
                args['player0'] = self.players[Player.PLAYER0]
                args['player9'] = self.players[Player.PLAYER9]
            elif section.function == "setup_top_pot":
                args['player0'] = self.players[Player.PLAYER0]
                args['player9'] = self.players[Player.PLAYER9]
            elif section.function == "setup_bottom_players":
                args.update({
                    'player3': self.players[Player.PLAYER3],
                    'player4': self.players[Player.PLAYER4],
                    'player5': self.players[Player.PLAYER5],
                    'player6': self.players[Player.PLAYER6]
                })
            elif section.function == "setup_bottom_pot":
                args.update({
                    'player3': self.players[Player.PLAYER3],
                    'player4': self.players[Player.PLAYER4],
                    'player5': self.players[Player.PLAYER5],
                    'player6': self.players[Player.PLAYER6]
                })
            elif section.function == "setup_middle":
                if len(section.players) >= 2:
                    player1_data = self._get_player_data(section.players[0], section.data_type or "name")
                    player2_data = self._get_player_data(section.players[1], section.data_type or "name")
                    args.update({
                        'string1': player1_data,
                        'string2': player2_data,
                        'spacing': section.spacing,
                        'middle_text': section.middle_text
                    })
        
        return args



    def _call_section_function(self, section: LayoutSection) -> None:
        func = getattr(self, section.function)
        args = self._resolve_function_args(section)
        
        if args:
            func(**args)
        else:
            func()




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



    def setup_top_players(self, player0: Poker_Player, player9: Poker_Player) -> None:
        new_diff = self._update_diff_between_players(player0.name, player9.name, self.TOP_PLAYER_SPACING_DIFF)

        build_steps = [
            self.border,
            self._create_space(5),  # BORDER_SPACING
            player0.name,
            self._create_space(new_diff),
            player9.name,
            self._create_space(5),  # BORDER_SPACING
            self.border
        ]
        self._print_order(build_steps)



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
        self._print_order(build_order)



    def setup_middle(self, string1: str, string2: str, spacing: int, middle_text: str) -> None:
        player1_left, player1_right = self._center_text(string1, spacing)
        player2_left, player2_right = self._center_text(string2, spacing)
        middle_text = self._alter_card_text(middle_text)
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
        self._print_order(build_order)



    def setup_bottom_players(self, player3: Poker_Player, player4: Poker_Player, player5: Poker_Player, player6: Poker_Player) -> None:
        spaces = [
            self.TOP_POT_BORDER_DIFF,
            self.P3_P4_DIFF,
            self.P4_P5_DIFF,
            self.P5_P6_DIFF,
            self.BOTTOM_PLAYER_BORDER_DIFF
        ]

        players = [player3, player4, player5, player6]
        for i in range(len(players)):
            left_change, right_change = self._edit_bottom_distance(players[i].name, True)
            spaces[i] -= left_change
            spaces[i + 1] -= right_change

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
        self._print_order(build_order)



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
        self._print_order(build_order)



    def print_table(self):
        """Render the complete table using configuration."""
        padding = 20
        
        for count, section in enumerate(self.config_manager.config.layout_sections):
            
            # Print left padding
            pad = " " * padding
            self.print_string(pad)
            
            # Execute the section
            self._call_section_function(section)
            
            # Update padding based on configuration
            padding_change = self.config_manager.get_padding_change(count)
            padding += padding_change
            
            print()  # New line


if __name__ == "__main__":
    # Create dummy players for testing
    dummy_players = [Poker_Player(2, True) for i in range(10)]
    total_pot = 10000
    river = [Card("HEART", "TEN"), Card("DIAMOND", "ACE"), Card("CLUB", "KING")]
    table = TableRenderer(dummy_players, total_pot, river)
    table.print_table()
    river = [Card("HEART", "TEN"), Card("DIAMOND", "ACE"), Card("CLUB", "KING"), Card("SPADE", "ACE")]
    table = TableRenderer(dummy_players, total_pot, river)
    table.print_table()
    river = [Card("HEART", "TEN"), Card("DIAMOND", "ACE"), Card("CLUB", "KING"), Card("SPADE", "ACE"), Card("HEART", "ACE")]
    table = TableRenderer(dummy_players, total_pot, river)
    table.print_table()
