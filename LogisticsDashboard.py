import tkinter
from GUIUtils import largeLabelFont
from game import celestialBodies, bodyDisplayedNameToNameConverter, saveData

class LogisticsDashboard:
    def __init__(self, targetScreen):
        self.frame = tkinter.Frame(targetScreen, highlightbackground="black", highlightthickness=2)
        self.grid = self.frame.grid

        self.label = tkinter.Label(self.frame, text="Colonisation Dashboard", font=largeLabelFont)
        self.label.pack()

        self.productionConsumptionView = tkinter.Label(self.frame, text="(Production and consumption values for different resources go here.)")
        self.productionConsumptionView.pack()

        self.colonyCrewCounter = tkinter.StringVar(value="(Crew amount goes here)")
        self.colonyCrewCounterLabel = tkinter.Label(self.frame, textvariable=self.colonyCrewCounter)
        self.colonyCrewCounterLabel.pack()

        self.selectedBody = tkinter.StringVar(value="Select Planet/Moon")
        self.bodySelector = tkinter.OptionMenu(self.frame, self.selectedBody, *[body.displayedName for body in celestialBodies])
        self.bodySelector.pack()
    
    def update(self):
        if self.selectedBody.get() == "Select Planet/Moon":
            return
        nameOfSelectedBody = bodyDisplayedNameToNameConverter(self.selectedBody.get())
        crewNumbersFound = [colony.crew for colony in saveData.colonies if colony.body == nameOfSelectedBody]
        if len(crewNumbersFound) > 1:
            raise RuntimeError(f"There are {len(crewNumbersFound)} colonies that are on the body {nameOfSelectedBody}. There should be 1")
        elif len(crewNumbersFound) == 1:
            self.colonyCrewCounter.set(f"Crew: {crewNumbersFound[0]}")
        else:
            self.colonyCrewCounter.set(f"{nameOfSelectedBody} has no colony.")
