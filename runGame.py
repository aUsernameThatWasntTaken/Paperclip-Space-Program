import game
import tkinter
import time

largeLabelFont = ("Segoe UI", 18)

screen = tkinter.Tk()
screen.title("PaperClip Space Program")

screen.columnconfigure(0, weight=2)
screen.columnconfigure(1, weight=1)
screen.columnconfigure(2, weight=0)
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
    
    def grid(self, row: int, column: int, rowSpan = 1, columnSpan = 1, sticky: str = ""):
        self.frame.grid(row=row, column=column, rowspan=rowSpan, columnspan=columnSpan, sticky=sticky)

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

    def grid(self, row: int, column: int, sticky: str = ""):
        self.frame.grid(row=row,column=column, sticky=sticky)

class DrawingBoard:
    def __init__(self, targetFrame: tkinter.Misc):
        self.frame = tkinter.Frame(targetFrame, highlightbackground="black", highlightthickness=2)
        self.grid = self.frame.grid

        self.label = tkinter.Label(self.frame, text="Drawing Board", font=largeLabelFont)
        self.label.grid(row=0, column=0, columnspan=2)

        self.shipNameLabel = tkinter.Label(self.frame, text="Ship Name: ")
        self.shipNameLabel.grid(row=1, column=0)
        self.shipName = tkinter.StringVar(value="Untitled Spacecraft")
        self.shipNameTextbox = tkinter.Entry(self.frame, textvariable=self.shipName)
        self.shipNameTextbox.grid(row=1,column=1)


class ResearchMenu:
    def __init__(self, targetFrame):
        self.frame = tkinter.Frame(targetFrame, highlightbackground="black", highlightthickness=2)

        self.label = tkinter.Label(self.frame, text="Research Menu", font=largeLabelFont)
        self.label.grid(row=0,column=0)

        self.researcherCounter = tkinter.StringVar(value="Resaecher count goes heer.")
        self.researcherCounterLabel = tkinter.Label(self.frame, textvariable=self.researcherCounter)
        self.researcherCounterLabel.grid(row=1, column=0)

        self.researchSpeedVar = tkinter.StringVar(value="Reaeaearch spead gooes hear.")
        self.researchSpeedLabel = tkinter.Label(self.frame, textvariable=self.researchSpeedVar)
        self.researchSpeedLabel.grid(row=1,column=1)

    def grid(self, row: int, column: int, rowSpan = 1, columnSpan = 1, sticky: str = ""):
        self.frame.grid(row=row, column=column, rowspan=rowSpan, columnspan=columnSpan, sticky=sticky)

colonyManagement = ColonyManagement(screen)  #A 2 by 2 grid.
colonyManagement.grid(row=1, column=0, sticky="news", rowSpan=2)

colonyResourceDashboard = ColonyResourceDashboard(screen)
colonyResourceDashboard.grid(row=1,column=1, sticky = "new")

drawingBoard = DrawingBoard(screen)
drawingBoard.grid(row = 2, column = 1, sticky="EW")

researchMenu = ResearchMenu(screen)
researchMenu.grid(row=1, column=2, rowSpan=2, sticky="news")

running = True
def close():
    global running
    running = False
    screen.destroy()
screen.protocol("WM_DELETE_WINDOW", close)


while running:
    time.sleep(1/30)
    if colonyResourceDashboard.selectedBody.get() != "Select Planet/Moon":
        nameOfSelectedBody = game.bodyDisplayedNameToNameConverter(colonyResourceDashboard.selectedBody.get())
        crewNumbersFound = [colony.crew for colony in game.saveData.colonies if colony.body == nameOfSelectedBody]
        if len(crewNumbersFound) > 1:
            raise RuntimeError(f"There are {len(crewNumbersFound)} colonies that are on the body {nameOfSelectedBody}. There should be 1")
        elif len(crewNumbersFound) == 1:
            colonyResourceDashboard.colonyCrewCounter.set(f"Crew: {crewNumbersFound[0]}")
        else:
            colonyResourceDashboard.colonyCrewCounter.set(f"{nameOfSelectedBody} has no colony.")
    if game.saveData.tutorialProgress == -1:
        tutorial.destroy()
    else:
        tutorialTextVar.set(game.tutorialText[game.saveData.tutorialProgress])
    screen.update()
    screen.update_idletasks()
print("Closed")