"""Contains all of the \"wonderful\" game logic. Any Userinterfaceing is right next door in runGame.py."""

import json
from typing import Callable, Iterable

#TODO: Add body class

defaultSaveData = {
    "money":100,
    "tutorialProgress":0,
    "colonies":[{"body":"Earth"}],
    "unlockedNodes":[]
    }

paperClipCompanyName = "Paperclips LLC LTD GmbH Inc. Sp.z.o.o. SRL Co."
researcherCount = 10
researcherEfficiency = 10 #research points per researcher Second
researchSpeed = researcherCount*researcherEfficiency

class TechTreeNode:
    def __init__(self,name: str, displayedName: str, prerequisites: list[str], unlocks: list[str], desc: str):
        self.prerequisites = prerequisites
        self.name = name #works like an ID
        self.displayedName = displayedName
        self.unlocks = unlocks
        self.desc = desc

    def canUnlock(self):
        returnBool = True
        for prerequisite in self.prerequisites:
            if prerequisite not in saveData.unlockedNodes:
                returnBool = False
        return returnBool

class SaveData:
    """Takes the dictionary from json.load and objectifies it."""
    def __init__(self, jsonDict: dict = defaultSaveData):
        self.money: int = jsonDict.get("money", defaultSaveData["money"])
        self.tutorialProgress: int = jsonDict.get("tutorialProgress", 0)
        self.colonies: list[Colony] = [Colony(colony) for colony in jsonDict.get("colonies",defaultSaveData["colonies"])]
        self.unlockedNodes: list[str] = jsonDict.get("unlockedNodes", defaultSaveData["unlockedNodes"])
        self.spacecraftDesigns: list[SpacecraftDesign] = [SpacecraftDesign(**spacecraftDict) for spacecraftDict in jsonDict.get("SpacecraftDesigns", [])]

class CelestialBody:
    def __init__(self, name: str, displayedName: str|None = None):
        self.name = name
        if displayedName is None:
            self.displayedName = self.name
        else:
            self.displayedName = displayedName

class Colony:
    def __init__(self, jsonDict: dict):
        self.body: str = jsonDict["body"]
        self.crew: int = jsonDict.get("crew", 0)

class Parts:
    class Part:
        def __init__(self, name: str):
            self.name = name

    class ControlUnit(Part):
        def __init__(self, name):
            super().__init__(name)

    class Thruster(Part):
        def __init__(self, name):
            super().__init__(name)
    
    class FuelTank(Part):
        def __init__(self, name):
            super().__init__(name)

    controlUnits: list[ControlUnit] = [ControlUnit(name="Mercury Command Pod")]
    thrusters: list[Thruster] = [Thruster(name = "RocketDyne A7")]
    fuelTanks: list[FuelTank] = [FuelTank(name = "Cylindrical")]

class SpacecraftDesign:
    def __init__(self, name: str, type: str, controlUnit: str, thrusters: tuple[str, int], fuelTank: str):
        self.name = name
        self.type = type
        thruster, self.numThrusters = thrusters
        self.controlUnit = findPart(controlUnit, Parts.controlUnits, lambda part: part.name)
        self.thrusters = findPart(thruster, Parts.thrusters, lambda part: part.name)
        self.fuelTank = findPart(fuelTank, Parts.fuelTanks, lambda part: part.name)

def findPart(name: str, partType: Iterable[Parts.Part], partAttribute: Callable[[Parts.Part], str]):
    """Finds a part by name, using partAttribute to decide whether to find the name or the display name, once those are added."""
    matchingParts = [part for part in partType if partAttribute(part) == name]
    if len(matchingParts) != 1:
        raise RuntimeError(f"There are {len(matchingParts)} parts in the provided list that match the name {name}. There should be one.")
    return matchingParts[0]

def bodyDisplayedNameToNameConverter(bodyDisplayedName: str):
    matchingBodies = [body.name for body in celestialBodies if body.displayedName == bodyDisplayedName]
    if len(matchingBodies) != 1:
        raise RuntimeError(f"Encountered invalid Body Display name: {bodyDisplayedName}. There were {len(matchingBodies)} bodies with that displayed name.")
    return matchingBodies[0]

TechTreeNodes: list[TechTreeNode] = [
    TechTreeNode("Root", "Start", [], [], 
                 f"""As part of their sponsorship, {paperClipCompanyName} has kindly provided us with 10 researchers to get us started! 
                 They should be able to complete this bit of research in around 2 months, but with how much fun we're having,
                 it will only feel like 10 seconds.""")
]

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

tutorialText = [f"""Welcome to PaperClip Space Program! {paperClipCompanyName} (the first company to employ a Superintelligent AGI as 
                its CEO) has recently decided to help fund our space program!""",
                "This works fine."]

def update():
    global researchSpeed
    researchSpeed = researcherCount*researcherEfficiency