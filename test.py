import timeit


def check_in_set():
    natural_ranks = ("QUEEN", "JACK", "KING", "TEN", "ACE")
    rank = "KING"
    return rank in natural_ranks

def check_in_list():
    natural_ranks = ["QUEEN", "JACK", "KING", "TEN", "ACE"]
    rank = "KING"
    return rank in natural_ranks

time_taken_list = timeit.timeit(check_in_list, number=1000)
time_taken_set = timeit.timeit(check_in_set, number=1000)

# print(f"The time taken for the set function is {time_taken_set} after 1000 iters")
# print("----------------")
# print(f"The time taken for the LIST function is {time_taken_list} after 1000 iters")

# print()
# rows, cols = 3, 4
# grid = np.zeros((rows, cols), dtype=int)
# print(grid)

from models.cards import *
hand = Hand(10)
ace_of_spaces = Card("SPADE", "ACE") 
hand.add_card(ace_of_spaces)
hand.add_card(ace_of_spaces)
hand.add_card(ace_of_spaces)
hand.add_card(ace_of_spaces)
hand.add_card(ace_of_spaces)
print(hand)

from rich import print
from rich.panel import Panel

print(Panel("Welcome to [bold red]BLACKJACK[/bold red]!", expand=False))

from art import *
print(text2art("BLACKJACK"))

from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.table import Table

console = Console()

# Styled text
print("[bold red]BLACKJACK[/bold red] [green]IS ON![/green]")

# Panel (like a box)
print(Panel("Welcome to [bold yellow]BLACKJACK[/bold yellow]!", expand=False))

# Table (great for cards)
table = Table(title="Player Hand")
table.add_column("Card", style="cyan", no_wrap=True)
table.add_column("Value", style="magenta")
table.add_row("Ace of Spades", "11")
table.add_row("7 of Hearts", "7")
console.print(table)

# Combining effects
print("[bold green on black]YOU WIN![/bold green on black]")

# Text banner
print(text2art("BLACKJACK"))

# Predefined ASCII figures
print(art("coffee"))     # prints a coffee cup
print(art("dragon"))     # prints a dragon figure

# Fun fonts for text
print(text2art("WIN", font="block"))
print(text2art("LOSS", font="random"))

# Emojis
print(art("heart"))
print(art("smile"))


from art import text2art, tprint
from rich.console import Console
from rich.text import Text
# from rich.markup import escape, markup

console = Console()

ascii_art = text2art("Dealer's Hand", font="charact1-small")
print(ascii_art)
tprint("Dealer's Hand", font="small")

from art import text2art
from rich.console import Console

console = Console()

ascii_art = text2art("Womp womp, there goes the kid's college fund..", font="doom")
console.print(ascii_art, style="green", markup=False)
print(ascii_art)

Console.print(Text(ascii_thing, style="green"))
