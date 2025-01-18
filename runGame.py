import game
import tkinter
import time

screen = tkinter.Tk()
screen.title("PaperClip Space Program")
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
    tutorial.grid(row=0,column=1)
#</Tutorial>
moneyStrVar = tkinter.StringVar(value=("Available funds: "+str(game.saveData.money)))
moneyTeller = tkinter.Label(screen, textvariable=moneyStrVar)
moneyTeller.grid(row=0,column=0)

class ColonyManagement:
    def __init__(self, targetScreen: tkinter.Misc):
        self.frame = tkinter.Frame(targetScreen)   # A 2 by 2 grid.

        self.label = tkinter.Label(self.frame, text="Colony Management", font=("Segoe UI",18))
        self.label.grid(row=0,column=0)

        self.productionMenu = tkinter.Label(self.frame, text="Colony Production")  #change this later
        self.productionMenu.grid(row=1,column=0)

        self.selectedPlanet = tkinter.StringVar(value="Select Planet/Moon")
        self.planetSelection = tkinter.OptionMenu(self.frame, self.selectedPlanet, *game.Planets)
        self.planetSelection.grid(row=0,column=1)

        self.buildMenu = tkinter.Label(self.frame, text="Colony build menu") #Change this later too.
        self.buildMenu.grid(row=1, column=1)
    
    def grid(self, row: int, column: int):
        self.frame.grid(row=row, column=column)



colonyManagement = ColonyManagement(screen)  #A 2 by 2 grid.
colonyManagement.grid(row=1, column=0)

running = True
def close():
    global running
    running = False
    screen.destroy()
screen.protocol("WM_DELETE_WINDOW", close)


while running:
    time.sleep(1/30)
    if game.saveData.tutorialProgress == -1:
        tutorial.destroy()
    else:
        tutorialTextVar.set(game.tutorialText[game.saveData.tutorialProgress])
    screen.update()
    screen.update_idletasks()
print("Closed")