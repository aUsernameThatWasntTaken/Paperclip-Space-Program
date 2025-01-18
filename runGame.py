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

# colony management Dashboard TODO: Put this in a class to allow making the names shorter
colonyManagement = tkinter.Frame(screen)  #A 2 by 2 grid.

colonyManagementLabel = tkinter.Label(colonyManagement, text="Colony Management", font=("Segoe UI",18))
colonyManagementLabel.grid(row=0,column=0)

colonyManagementProductionMenu = tkinter.Label(colonyManagement, text="Colony Production")  #change this later
colonyManagementProductionMenu.grid(row=1,column=0)

colonyManagementSelectedPlanet = tkinter.StringVar(value="Select Planet/Moon")
colonyManagementPlanetSelection = tkinter.OptionMenu(colonyManagement, colonyManagementSelectedPlanet, *game.Planets)
colonyManagementPlanetSelection.grid(row=0,column=1)

colonyManagementBuildMenu = tkinter.Label(colonyManagement, text="Colony build menu") #Change this later too.
colonyManagementBuildMenu.grid(row=1, column=1)

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