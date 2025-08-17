import json
import os
from models.enums import States
from entities.player import Player


class Stats:
    
    def __init__(self):
        f_path = os.path.dirname(__file__)
        self.file_path = os.path.join(f_path, "player_stats.json")
        with open(self.file_path, "r") as f:
            self.data = json.load(f)

    def update_stat(self,player: Player, state: States):
        match state:
            case States.WIN | States.BLACKJACK:
                self.data["total_wins"] += 1
                self.data["win_streak"] += 1
                self.data["total_matches"] += 1
                self.data["money_gained"] += player.curr_bet
                if state == States.BLACKJACK:
                    self.data["blackjacks_won"] += 1
                if player.curr_bet > self.data["biggest_win"]:
                    self.data["biggest_win"] == player.curr_bet
            case States.TIE:
                self.data["total_ties"] += 1
                self.data["total_matches"] += 1
            case States.BUST | States.LOSE:
                self.data["total_losses"] += 1
                self.data["total_matches"] += 1
                self.data["loss_streak"] += 1
                self.data["money_lost"] += player.curr_bet
                if state == States.BUST:
                    self.data["bust_loss"] += 1
                if player.curr_bet > self.data["biggest_loss"]:
                    self.data["biggest_loss"] == player.curr_bet
    
    def save_data(self):
        with open(self.file_path, "w") as f:
            json.dump(self.data, f, indent=4)


if __name__ == "__main__":
    x = Stats()
    x.update_stat(States.TIE)