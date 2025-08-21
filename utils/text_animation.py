from art import text2art
from rich.live import Live
from rich import print
import os
import re
import time
from rich.text import Text
import asyncio

currFont = "random"

async def stringColorChange(text: str, colors: list[str], swapTime, totalTime):
    styled = text2art(text,font=currFont)
    startTime = time.time()
    colorIndex = 0
    while(time.time() - startTime < totalTime):
        colorIndex+=1
        colorIndex %= len(colors)
        animated = f"[{colors[colorIndex]}]{styled}[/{colors[colorIndex]}]"
        yield animated
        await asyncio.sleep(swapTime)        

            
async def stringWave(text: str, colors: list[str], swapTime, loops:int):
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
        yield fullString
        flashingIndex += incrementer
        lastFlashTime = time.time()
        if flashingIndex >= len(styledChars) or flashingIndex < 0:
            incrementer *= -1
            currLoop += 1
            flashingIndex += incrementer
            if currLoop == loops:
                break


async def charFlash(text: str, colors: list[str], swapTime, totalTime: float):
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
        yield fullString
        flashingIndex += incrementer
        lastFlashTime = time.time()


                


async def main():
    text = "Winner"
    text2 = "Now This Is Epic"

    with Live(auto_refresh=False) as live:
        animations = [
            stringColorChange(text, ["black", "white", "red"], .2, 2),
            stringColorChange(text, ["black", "white", "red"], .2, 2),
        ]
        frames = []
        while True:
            try:
                frames = []
                for animation in animations:
                    frame = await anext(animation)
                    frames.append(frame)
                combinedFrames = "\n".join(frames)
                live.update(combinedFrames, refresh=True)
            except StopAsyncIteration:
                print("animations complete")
                break                
if __name__ == "__main__":
    asyncio.run(main())