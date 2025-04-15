import tkinter
largeLabelFont = ("Segoe UI", 18)
# default Font = ("Segoe UI", 9)    but there's no need to think about that.
smallLabelFont = ("Segoe UI", 4)

class LabeledDropdown:
    def __init__(self, frame: tkinter.Misc, row: int, column: int, label: str, defaultValue: str, *options: str):
        self.label = tkinter.Label(frame, text=label)
        self.label.grid(row=row, column=column)
        self.stringVar = tkinter.StringVar(value=defaultValue)
        self.get = self.stringVar.get
        self.Dropdown = tkinter.OptionMenu(frame, self.stringVar, *options)
        self.Dropdown.grid(row=row, column=column+1, sticky="news")

class LabeledEntry:
    def __init__(self, frame: tkinter.Misc, row: int, column: int, label: str, defaultValue: str):
        self.label = tkinter.Label(frame, text=label)
        self.label.grid(row=row, column=column)
        self.stringVar = tkinter.StringVar(value=defaultValue)
        self.get = self.stringVar.get
        self.entry = tkinter.Entry(frame, textvariable=self.stringVar)
        self.entry.grid(row=row, column=column+1, sticky="news")
        