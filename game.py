"""Contains all of the \"wonderful\" game logic. Any Userinterfaceing is right next door in runGame.py."""

import json

#TODO: Add body class

defaultSaveData = {
    "money":100,
    "tutorialProgress":0,
    "colonies":[{"body":"Earth"}]
    }

class SaveData:
    """Takes the dictionary from json.load and objectifies it."""
    def __init__(self, jsonDict: dict = defaultSaveData):
        self.money: int = jsonDict.get("money", defaultSaveData["money"])
        self.tutorialProgress: int = jsonDict.get("tutorialProgress", 0)
        self.colonies: list[Colony] = [Colony(colony) for colony in jsonDict.get("colonies",defaultSaveData["colonies"])]

class CelestialBody:
    def __init__(self, name: str, displayedName: str|None = None):
        self.name = name
        if displayedName is None:
            self.displayedName = self.name
        else:
            self.displayedName = displayedName

class Colony:
    def __init__(self, jsonDict: dict):
        self.body = jsonDict["body"]
        self.crew = jsonDict.get("crew", 0)

def bodyDisplayedNameToNameConverter(bodyDisplayedName: str):
    matchingBodies = [body.name for body in celestialBodies if body.displayedName == bodyDisplayedName]
    if len(matchingBodies) != 1:
        raise RuntimeError(f"""Encountered invalid Body Display name: {bodyDisplayedName}. 
                           There were {len(matchingBodies)} bodies with that displayed name.""")
    return matchingBodies[0]

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

def tutorialSkip():
    saveData.tutorialProgress = -1

celestialBodies: list[CelestialBody] = [
    CelestialBody("Earth"),
    CelestialBody("Luna","Luna (moon of Earth)"),
    CelestialBody("Mars"),
    CelestialBody("Deimos","Deimos (moon of Mars)"),
    CelestialBody("Phobos","Phobos (moon of Mars)")
]

paperClipCompanyName = "Paperclips LLC LTD GmbH Inc. Sp.z.o.o. SRL Co."
tutorialText = [f"""Welcome to PaperClip Space Program! {paperClipCompanyName} (the first company to employ a Superintelligent AGI as 
                its CEO) has recently decided to help fund our space program!""",
                "This works fine."]