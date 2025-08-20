from art import text2art
from rich.live import Live
from rich import print
import os
import time
from rich.text import Text
import asyncio

currFont = "tarty1"

async def stringColorChange(text: str, colors: list[str], swapTime, totalTime, staticText: str):
    styled = text2art(text,font=currFont)
    startTime = time.time()
    colorIndex = 0
    while(time.time() - startTime < totalTime):
        colorIndex+=1
        colorIndex %= len(colors)
        animated = f"[{colors[colorIndex]}]{styled}[/{colors[colorIndex]}]"
        finalOut = animated + f"\n{staticText}"
        yield finalOut
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
    text = "GlizzyyMaxxxx"

    with Live(auto_refresh=False) as live:
        animation1 = stringColorChange(text, ["yellow", "red"], .2, 2, "printing after but while async")
        animation2 = stringColorChange(text, ["green", "red"], .2, 2, "this is the 2nd print statement")
        while True:
            try:
                frame1, frame2 = await asyncio.gather(
                    anext(animation1),
                    anext(animation2)
                )
                combinedFrames = f"{frame1}\n{frame2}"
                live.update(combinedFrames, refresh=True)
        # charFlash(live, text,["green", "white", "white", "white", "white", "white"],.05,10)
        # await stringWave(live,text,["black","red"], .2,1)
        # await stringColorChange(live, text,["yellow","red"], .2,2)
        # await charFlash(live, text,["red", "orange", "yellow", "green", "blue", "purple"],.05,200)
            except StopAsyncIteration:
                print("animations complete")
                break                
if __name__ == "__main__":
    asyncio.run(main())