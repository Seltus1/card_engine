from art import text2art
from rich.live import Live
from rich import print
import os
import time
from rich.text import Text

currFont = "tarty1"

def stringColorChange(live: Live, text: str, colors: list[str], swapTime, totalTime):
    styled = text2art(text,font=currFont)
    startTime = time.time()
    lastFlashTime = 0
    colorIndex = 0
    while(True):
        currTime = time.time()
        if currTime - startTime > totalTime: break
        if (currTime - lastFlashTime) > swapTime:
            colorIndex+=1
            colorIndex %= len(colors)
            lastFlashTime = time.time()
            live.update(f"[{colors[colorIndex]}]{styled}[/{colors[colorIndex]}]", refresh=True)

            
def stringWave(live:Live, text: str, colors: list[str], swapTime, loops:int):
    styledChars = [text2art(letter, font=currFont).splitlines() for letter in text]
    fullString = ""
    flashingIndex = -1
    lastFlashTime = 0
    currLoop = 0
    incrementer = 1
    while True:
        if time.time() - lastFlashTime < swapTime: continue
        fullStringLines = []
        for i in range(len(styledChars[0])):
            line = ""
            for j in range(len(styledChars)):
                char_lines = styledChars[j]
                if j == flashingIndex:
                    line += f"[{colors[1]}]{char_lines[i]}[/{colors[1]}]"
                    continue
                line += f"[{colors[0]}]{char_lines[i]}[/{colors[0]}]"
            fullStringLines.append(line)
        fullString = "\n".join(fullStringLines)
        live.update(fullString, refresh=True)
        flashingIndex += incrementer
        lastFlashTime = time.time()
        if flashingIndex >= len(styledChars) or flashingIndex < 0:
            incrementer *= -1
            currLoop += 1
            flashingIndex += incrementer
            if currLoop == loops:
                break


def charFlash(live: Live,text: str, colors: list[str], swapTime, totalTime: float):
    styledChars = [text2art(letter, font=currFont).splitlines() for letter in text]
    startTime = time.time()
    fullString = ""
    flashingIndex = -1
    lastFlashTime = 0
    currLoop = 0
    incrementer = 0
    while True:
        if(time.time() - startTime > totalTime):
            break
        if time.time() - lastFlashTime < swapTime: continue
        fullStringLines = []
        for i in range(len(styledChars[0])):
            line = ""
            for j in range(len(styledChars)):
                char_lines = styledChars[j]
                line += f"[{colors[incrementer]}]{char_lines[i]}[/{colors[incrementer]}]"
                incrementer += 1
                incrementer %= len(colors)
            fullStringLines.append(line)
        fullString = "\n".join(fullStringLines)
        live.update(fullString, refresh=True)
        flashingIndex += incrementer
        lastFlashTime = time.time()


                





if __name__ == "__main__":
    text = "GlizzyyMaxxxx"
    with Live(auto_refresh=False) as live:
        # charFlash(live, text,["green", "white", "white", "white", "white", "white"],.05,10)
        stringWave(live,text,["black","red"], .2,1)
        stringColorChange(live, text,["yellow","red"], .2,2)
        charFlash(live, text,["red", "orange", "yellow", "green", "blue", "purple"],.05,200)
        stringColorChange(live, text,["yellow","red"], .2,2)