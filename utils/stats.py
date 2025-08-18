import json
import os
from models.enums import States
from entities.player import Player

json_template = {
    "total_matches": 0,
    "total_bets": 0,
    "total_wins": 0,
    "total_losses": 0,
    "total_ties": 0,
    "money_gained": 0,
    "money_lost": 0,
    "net_profit": 0,
    "total_money": 100000,
    "biggest_win": 0,
    "biggest_loss": 0,
    "win_streak": 0,
    "longest_win_streak": 0,
    "loss_streak": 0,
    "bust_loss": 0,
    "longest_loss_streak": 0,
    "blackjacks_won": 0,
    "blackjacks_against": 0
}
class Stats:
    
    def __init__(self):
        f_path = os.path.dirname(__file__)
        self.file_path = os.path.join(f_path, "player_stats.json")
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump(json_template, f, indent=4)

        with open(self.file_path, "r") as f:
            self.data = json.load(f)

    def update_stat(self,player: Player, state: States):
        match state:
            case States.WIN | States.BLACKJACK:
                self.data["total_wins"] += 1
                self.data["win_streak"] += 1
                self.data["total_matches"] += 1
                self.data["loss_streak"] = 0
                if state == States.BLACKJACK:
                    self.data["blackjacks_won"] += 1
                    self.data["money_gained"] += (player.curr_bet * 1.5)
                    self.data["total_money"] += player.curr_bet
                else:
                    self.data["money_gained"] += player.curr_bet
                    self.data["total_money"] += player.curr_bet

                if player.curr_bet > self.data["biggest_win"]:
                    self.data["biggest_win"] = player.curr_bet
            case States.TIE:
                self.data["total_ties"] += 1
                self.data["total_matches"] += 1
            case States.BUST | States.LOSE:
                self.data["total_losses"] += 1
                self.data["total_matches"] += 1
                self.data["loss_streak"] += 1
                self.data["win_streak"] = 0
                self.data["money_lost"] += player.curr_bet
                self.data["total_money"] -= player.curr_bet
                if state == States.BUST:
                    self.data["bust_loss"] += 1
                if player.curr_bet > self.data["biggest_loss"]:
                    self.data["biggest_loss"] = player.curr_bet
        self.save_data()
    
    def save_data(self):
        self.data["net_profit"] = self.data["money_gained"] - self.data["money_lost"]
        if self.data["win_streak"] > self.data["longest_win_streak"]:
            self.data["longest_win_streak"] = self.data["win_streak"]

        if self.data["loss_streak"] > self.data["longest_loss_streak"]:
            self.data["longest_loss_streak"] = self.data["loss_streak"]

        with open(self.file_path, "w") as f:
            json.dump(self.data, f, indent=4)

    def update_specific_stat(self, stat: str):
        self.data[stat] += 1
    
    def get_stat(self, field: str):
        return self.data[field]
if __name__ == "__main__":
    x = Stats()
    x.update_stat(States.TIE)