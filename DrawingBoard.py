from game import SpacecraftDesign, Parts, saveData
import tkinter
from GUIUtils import LabeledDropdown, LabeledEntry, largeLabelFont
FrameClass = tkinter.Misc

class DrawingBoard:
    class ShipStatDisplay:
        def __init__(self, targetFrame: FrameClass):
            self.frame = tkinter.Frame(targetFrame)
            self.grid = self.frame.grid

        def update(self, design: SpacecraftDesign|None):
            if design is None:
                return
            else:
                nextRow = iter(range(100)).__next__
                for stat, value in design.statDict.items():
                    row = nextRow()
                    statLabel = tkinter.Label(self.frame, text=stat)
                    statLabel.grid(row=row, column=0)
                    valueLabel = tkinter.Label(self.frame, text=str(value))
                    valueLabel.grid(row=row, column=1)

    def __init__(self, targetFrame: FrameClass):
        self.frame = tkinter.Frame(targetFrame, highlightbackground="black", highlightthickness=2)
        self.grid = self.frame.grid

        self.label = tkinter.Label(self.frame, text="Drawing Board", font=largeLabelFont)
        self.label.grid(row=0, column=0, columnspan=2)

        self.shipName = LabeledEntry(self.frame, 1,0, "Ship Name: ", "Untitled Spacecraft")
        self.controlUnit = LabeledDropdown(self.frame, 2, 0, "Ship's contol Unit: ", "Select a Contol Unit", *[part.name for part in Parts.controlUnits])
        self.thrusters = LabeledDropdown(self.frame, 3, 0, "Ship's Thrusters: ", "Select a type of Thruster", *[part.name for part in Parts.thrusters])
        self.fuelTank = LabeledDropdown(self.frame, 4,0, "Fuel Tank: ", "Select Fuel Tank", *[part.name for part in Parts.fuelTanks])
        self.evalShipButton = tkinter.Button(self.frame, command=self.evaluateShip, text="Evaluate Ship")
        self.evalShipButton.grid(row=5, column=0)
        self.saveShipButton = tkinter.Button(self.frame, command=self.saveShip, text="Save Ship")
        self.saveShipButton.grid(row=5, column=1)
        self.shipStatDisplay = self.ShipStatDisplay(self.frame)
        self.shipStatDisplay.grid(row=6,column=0, columnspan=2)

        self.fuelTankDiameter = LabeledEntry(self.frame, 4,2, "Diameter", "1.75")
        self.fuelTankHeight = LabeledEntry(self.frame, 4,4, "Height", "10")
    
    def getShipDesign(self):
        try:
            return SpacecraftDesign(self.shipName.get(), 
                                    "Lander", 
                                    self.controlUnit.get(), 
                                    (self.thrusters.get(), 1), 
                                    (self.fuelTank.get(), (self.fuelTankDiameter.get(),self.fuelTankHeight.get())))
        except RuntimeError:
            return None

    def evaluateShip(self):
        self.shipStatDisplay.update(self.getShipDesign())

    def saveShip(self):
        design = self.getShipDesign()
        if design is not None:
            saveData.spacecraftDesigns.append(design)
