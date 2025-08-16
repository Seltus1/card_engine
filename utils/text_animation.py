from rich.live import Live
from rich import print
import os
import time

def stringColorChange(text: str, colors: list[str], swapTime, totalTime):
    startTime = time.time()
    lastFlashTime = 0
    colorIndex = 0
    lines = text.count("\n") + 1
    # print(f"[{colors[colorIndex]}]{text}[/{colors[colorIndex]}]", end="\r")
    with Live(refresh_per_second=10) as live:
        while(True):
            currTime = time.time()
            live.update(f"[{colors[colorIndex]}]{text}[/{colors[colorIndex]}]")
            if currTime - startTime > totalTime: break
            if (currTime - lastFlashTime) > swapTime:
                live.update(f"[{colors[colorIndex]}]{text}[/{colors[colorIndex]}]")
                colorIndex+=1
                colorIndex %= len(colors)
                lastFlashTime = time.time()
            

if __name__ == "__main__":
    ascii_win = r"""
    .----------------.  .----------------.  .-----------------. .-----------------. .----------------.  .----------------. 
    | .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
    | | _____  _____ | || |     _____    | || | ____  _____  | || | ____  _____  | || |  _________   | || |  _______     | |
    | ||_   _||_   _|| || |    |_   _|   | || ||_   \|_   _| | || ||_   \|_   _| | || | |_   ___  |  | || | |_   __ \    | |
    | |  | | /\ | |  | || |      | |     | || |  |   \ | |   | || |  |   \ | |   | || |   | |_  \_|  | || |   | |__) |   | |
    | |  | |/  \| |  | || |      | |     | || |  | |\ \| |   | || |  | |\ \| |   | || |   |  _|  _   | || |   |  __ /    | |
    | |  |   /\   |  | || |     _| |_    | || | _| |_\   |_  | || | _| |_\   |_  | || |  _| |___/ |  | || |  _| |  \ \_  | |
    | |  |__/  \__|  | || |    |_____|   | || ||_____|\____| | || ||_____|\____| | || | |_________|  | || | |____| |___| | |
    | |              | || |              | || |              | || |              | || |              | || |              | |
    | '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
    '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 
    """ 
    stringColorChange(ascii_win,["white","green"], .3, 2)