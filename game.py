"""Contains all of the \"wonderful\" game logic. Any Userinterfaceing is right next door in runGame.py."""

import json

defaultSaveData = {
    "money":100,
    "tutorialProgress":0
    }

class SaveData:
    """Takes the dictionary from json.load and objectifies it."""
    def __init__(self, jsonDict: dict = defaultSaveData):
        self.money: int = jsonDict["money"]
        self.tutorialProgress = jsonDict["tutorialProgress"]

with open("saveData.json") as f:
    try:
        saveData = SaveData(json.load(f))
    except json.JSONDecodeError:
        saveData = SaveData()
    except KeyError:
        saveData = SaveData()

def tutorialNext():
    if saveData.tutorialProgress == -1:
        return
    saveData.tutorialProgress += 1
    if saveData.tutorialProgress >= len(tutorialText):
        saveData.tutorialProgress = -1
        return

paperClipCompanyName = "Paperclips LLC LTD GmbH Inc. Sp.z.o.o. SRL Co."
tutorialText = [f"""Welcome to PaperClip Space Program! {paperClipCompanyName} (the first company to employ a Superintelligent AGI as 
                its CEO) has recently decided to help fund our space program!""",
                "This works fine."]