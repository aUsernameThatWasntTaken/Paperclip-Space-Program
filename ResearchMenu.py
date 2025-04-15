import tkinter
from game import TechTreeNode
from GUIUtils import smallLabelFont, largeLabelFont

class ResearchMenu:
    class ResearchNodeText:
        def __init__(self, techtreeNode: TechTreeNode, targetFrame):
            self.node = techtreeNode
            self.frame = tkinter.Frame(targetFrame)
            self.grid = self.frame.grid

            self.nameLabel = tkinter.Label(self.frame, text=techtreeNode.displayedName)
            self.nameLabel.grid(row=0,column=0)
            self.descLabel = tkinter.Label(self.frame, text=techtreeNode.desc, font=smallLabelFont)
            self.descLabel.grid(row=1,column=0)

    def __init__(self, targetFrame, researchNodes: list[TechTreeNode]):
        nextRow = iter(range(100)).__next__ # Raise number if needed (probebly not)

        self.frame = tkinter.Frame(targetFrame, highlightbackground="black", highlightthickness=2)

        self.label = tkinter.Label(self.frame, text="Research Menu", font=largeLabelFont)
        self.label.grid(row=nextRow(),column=0, columnspan=2)

        self.researcherCounter = tkinter.StringVar(value="Resaecher count goes heer.")
        self.researcherCounterLabel = tkinter.Label(self.frame, textvariable=self.researcherCounter)
        researcherCounterRow = nextRow()
        self.researcherCounterLabel.grid(row=researcherCounterRow, column=0)

        self.researchSpeedVar = tkinter.StringVar(value="Reaeaearch spead gooes hear.")
        self.researchSpeedLabel = tkinter.Label(self.frame, textvariable=self.researchSpeedVar)
        self.researchSpeedLabel.grid(row=researcherCounterRow,column=1)

        researchNodeTexts = [self.ResearchNodeText(node, self.frame) for node in researchNodes]
        for researchNodeText in researchNodeTexts:
            row = nextRow()
            researchNodeText.grid(row=row,column=0)
            addToQueueButton = tkinter.Button(self.frame,command=researchNodeText.node.addToQueue, text="add to queue")
            addToQueueButton.grid(row=row,column=1)

    def grid(self, row: int, column: int, rowSpan = 1, columnSpan = 1, sticky: str = ""):
        self.frame.grid(row=row, column=column, rowspan=rowSpan, columnspan=columnSpan, sticky=sticky)
