import tkinter
from GUIUtils import largeLabelFont
from game import celestialBodies

class ColonyManagement:
    def __init__(self, targetScreen: tkinter.Misc):
        self.frame = tkinter.Frame(targetScreen, highlightbackground="black", highlightthickness=2)   # A 2 by 2 grid.

        self.label = tkinter.Label(self.frame, text="Colony Management", font=largeLabelFont)
        self.label.grid(row=0,column=0)

        self.productionMenu = tkinter.Label(self.frame, text="Colony Production")  #change this later
        self.productionMenu.grid(row=1,column=0)

        self.selectedPlanet = tkinter.StringVar(value="Select Planet/Moon")
        self.planetSelection = tkinter.OptionMenu(self.frame, self.selectedPlanet, *[body.displayedName for body in celestialBodies])
        self.planetSelection.grid(row=0,column=1)

        self.buildMenu = tkinter.Label(self.frame, text="Colony build menu") #Change this later too.
        self.buildMenu.grid(row=1, column=1)
    
    def grid(self, row: int, column: int, rowSpan = 1, columnSpan = 1, sticky: str = ""):
        self.frame.grid(row=row, column=column, rowspan=rowSpan, columnspan=columnSpan, sticky=sticky)
