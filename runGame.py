import game
import tkinter
import time

# Import each GUI element to make this file smaller
from DrawingBoard import DrawingBoard
from colonyManagementDashboard import ColonyManagement
from LogisticsDashboard import LogisticsDashboard
from ResearchMenu import ResearchMenu

FrameClass = tkinter.Misc

screen = tkinter.Tk()
screen.title("PaperClip Space Program")

screen.columnconfigure(0, weight=2)
screen.columnconfigure(1, weight=1)
screen.columnconfigure(2, weight=0)

screen.rowconfigure(1, weight=1)
screen.rowconfigure(2, weight=1)
#Defines a frame for the tutorial text, next, and skip tutorial buttons.
if game.saveData.tutorialProgress != -1:
    tutorial = tkinter.Frame(screen)
    tutorialTextVar = tkinter.StringVar(value=game.tutorialText[game.saveData.tutorialProgress])
    tutorialText = tkinter.Label(tutorial, textvariable=tutorialTextVar)
    tutorialText.grid(row=0,column=0)
    tutorialNextButton = tkinter.Button(tutorial, text="Next", command=game.tutorialNext)
    tutorialNextButton.grid(row=0,column=1)
    tutorialSkipButton = tkinter.Button(tutorial,text="Skip", command=game.tutorialSkip)
    tutorialSkipButton.grid(row=0,column=2)
    tutorial.grid(row=0,column=1, columnspan=2)
#</Tutorial>
moneyStrVar = tkinter.StringVar(value=("Available funds: "+str(game.saveData.money)))
moneyTeller = tkinter.Label(screen, textvariable=moneyStrVar)
moneyTeller.grid(row=0,column=0)

colonyManagement = ColonyManagement(screen)  #A 2 by 2 grid.
colonyManagement.grid(row=1, column=0, sticky="news", rowSpan=2)

logisticsDashboard = LogisticsDashboard(screen)
logisticsDashboard.grid(row=1,column=1, sticky = "news")

drawingBoard = DrawingBoard(screen)
drawingBoard.grid(row = 2, column = 1, sticky="news")

researchMenu = ResearchMenu(screen, game.TechTreeNodes)
researchMenu.grid(row=1, column=2, rowSpan=2, sticky="news")

running = True
def close():
    global running
    running = False
    screen.destroy()
screen.protocol("WM_DELETE_WINDOW", close)


while running:
    time.sleep(1/30)
    game.update()
    logisticsDashboard.update()
    researchMenu.researcherCounter.set("Researchers: "+str(game.researcherCount))
    researchMenu.researchSpeedVar.set("Research Speed: "+str(game.researchSpeed)+" points per second")
    if game.saveData.tutorialProgress == -1:
        tutorial.destroy()
    else:
        tutorialTextVar.set(game.tutorialText[game.saveData.tutorialProgress])
    screen.update()
    screen.update_idletasks()
print("Closed")