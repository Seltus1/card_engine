from art import text2art
from rich.live import Live
from rich import print
import os
import time

def stringColorChange(text: str, colors: list[str], swapTime, totalTime):
    styled = text2art(text,font="block")
    startTime = time.time()
    lastFlashTime = 0
    colorIndex = 0
    with Live(refresh_per_second=60) as live:
        while(True):
            currTime = time.time()
            live.update(f"[{colors[colorIndex]}]{styled}[/{colors[colorIndex]}]")
            if currTime - startTime > totalTime: break
            if (currTime - lastFlashTime) > swapTime:
                live.update(f"[{colors[colorIndex]}]{styled}[/{colors[colorIndex]}]")
                colorIndex+=1
                colorIndex %= len(colors)
                lastFlashTime = time.time()
            
def stringWave(text: str, colors: list[str], swapTime, loops):
    styledChars = [text2art(letter, font="block").splitlines() for letter in text]
    flashingIndex = -1
    lastFlashTime = 0
    currLoop = 0
    incrementer = 1
    with Live(refresh_per_second=60) as live:
        while True:
            if time.time() - lastFlashTime > swapTime:
                flashingIndex += incrementer
                lastFlashTime = time.time()
            
            if flashingIndex >= len(styledChars) or flashingIndex < 0:
                incrementer *= -1
                currLoop += 1
                flashingIndex += incrementer
                if currLoop == loops:
                    break
            
            fullStringLines = []
            for i in range(len(styledChars[0])):
                line = ""
                for j in range(len(styledChars)):
                    char_lines = styledChars[j]
                    if j == flashingIndex:
                        line += f"[{colors[1]}]{char_lines[i]}[/{colors[1]}]"
                    else:
                        line += f"[{colors[0]}]{char_lines[i]}[/{colors[0]}]"
                fullStringLines.append(line)
            
            fullString = "\n".join(fullStringLines)
            live.update(fullString)




if __name__ == "__main__":
    text = "Hi Stimmer"
    stringWave(text,["green","white"], .2, 4)