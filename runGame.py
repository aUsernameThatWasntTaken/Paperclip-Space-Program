import game
import tkinter
import time

largeLabelFont = ("Segoe UI", 18)

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
    tutorial.grid(row=0,column=1, columnspan=2)
#</Tutorial>
moneyStrVar = tkinter.StringVar(value=("Available funds: "+str(game.saveData.money)))
moneyTeller = tkinter.Label(screen, textvariable=moneyStrVar)
moneyTeller.grid(row=0,column=0)

class ColonyManagement:
    def __init__(self, targetScreen: tkinter.Misc):
        self.frame = tkinter.Frame(targetScreen, highlightbackground="black", highlightthickness=2)   # A 2 by 2 grid.

        self.label = tkinter.Label(self.frame, text="Colony Management", font=largeLabelFont)
        self.label.grid(row=0,column=0)

        self.productionMenu = tkinter.Label(self.frame, text="Colony Production")  #change this later
        self.productionMenu.grid(row=1,column=0)

        self.selectedPlanet = tkinter.StringVar(value="Select Planet/Moon")
        self.planetSelection = tkinter.OptionMenu(self.frame, self.selectedPlanet, *[body.displayedName for body in game.celestialBodies])
        self.planetSelection.grid(row=0,column=1)

        self.buildMenu = tkinter.Label(self.frame, text="Colony build menu") #Change this later too.
        self.buildMenu.grid(row=1, column=1)
    
    def grid(self, row: int, column: int, rowSpan = 1, columnSpan = 1):
        self.frame.grid(row=row, column=column, rowspan=rowSpan, columnspan=columnSpan)

class ColonyResourceDashboard:
    def __init__(self, targetScreen):
        self.frame = tkinter.Frame(targetScreen, highlightbackground="black", highlightthickness=2)

        self.label = tkinter.Label(self.frame, text="Colonisation Dashboard", font=largeLabelFont)
        self.label.pack()

        self.productionConsumptionView = tkinter.Label(self.frame, text="(Production and consumption values for different resources go here.)")
        self.productionConsumptionView.pack()

        self.colonyCrewCounter = tkinter.StringVar(value="(Crew amount goes here)")
        self.colonyCrewCounterLabel = tkinter.Label(self.frame, textvariable=self.colonyCrewCounter)
        self.colonyCrewCounterLabel.pack()

        self.selectedBody = tkinter.StringVar(value="Select Planet/Moon")
        self.bodySelector = tkinter.OptionMenu(self.frame, self.selectedBody, *[body.displayedName for body in game.celestialBodies])
        self.bodySelector.pack()

    def grid(self, row: int, column: int):
        self.frame.grid(row=row,column=column)

colonyManagement = ColonyManagement(screen)  #A 2 by 2 grid.
colonyManagement.grid(row=1, column=0)

colonyResourceDashboard = ColonyResourceDashboard(screen)
colonyResourceDashboard.grid(row=1,column=1)

drawingBoard = tkinter.Label(screen, text="Drawing Board", font=largeLabelFont)
drawingBoard.grid(row = 2, column = 1)

researchMenu = tkinter.Label(screen, text="Research Menu", font=largeLabelFont)
researchMenu.grid(row=1, column=2, rowspan=2)

running = True
def close():
    global running
    running = False
    screen.destroy()
screen.protocol("WM_DELETE_WINDOW", close)


while running:
    time.sleep(1/30)
    if colonyResourceDashboard.selectedBody.get() != "Select Planet/Moon":
        colonyResourceDashboard.colonyCrewCounter.set(f"Crew: {[colony.crew for colony in game.saveData.colonies if colony.body == game.bodyDisplayedNameToNameConverter(colonyResourceDashboard.selectedBody.get())][0]}")
    if game.saveData.tutorialProgress == -1:
        tutorial.destroy()
    else:
        tutorialTextVar.set(game.tutorialText[game.saveData.tutorialProgress])
    screen.update()
    screen.update_idletasks()
print("Closed")