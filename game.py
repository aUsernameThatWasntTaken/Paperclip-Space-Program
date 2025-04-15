"""Contains all of the \"wonderful\" game logic. Any Userinterfaceing is right next door in runGame.py."""

import json
from typing import Callable, Iterable
from math import pi, log

#TODO: Add body class

defaultSaveData = {
    "money":100,
    "tutorialProgress":0,
    "colonies":[{"body":"Earth"}],
    "unlockedNodes":[]
    }

#CONSTANTS:
densityOfLox = 1141
densityOfLiquidMethane = 422
MethaneLoxRatio = 1/3.6 #according to reddit.
densityOfMethalox = int((densityOfLox*1+densityOfLiquidMethane*MethaneLoxRatio)/(1+MethaneLoxRatio))
milimetre = 1/1000
paperClipCompanyName = "Paperclips LLC LTD GmbH Inc. Sp.z.o.o. SRL Co."
fuelTankWallThickness = 10*milimetre
densityOfSteel = 7850 #kg/m³
earthFirstStageDV = 1000 #change this later
earthSurfaceGravity = 9.80665 #m/s²

#FORMULAS:
surfaceAreaOfCylinder: Callable[[int,int],float] = lambda r, h: 2*pi*(r**2) + 2*pi*r*h
volumeOfCylinder: Callable[[int,int],float] = lambda r,h: pi*h*(r**2)

#TESTS for formulas:
if surfaceAreaOfCylinder(1,2) != 6*pi:
    raise ArithmeticError(f"{surfaceAreaOfCylinder(1,2)=}, should be {6*pi}")
if volumeOfCylinder(1,2) != 2*pi:
    raise ArithmeticError(f"{volumeOfCylinder(1,2)=}, should be {2*pi}")

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
    
    def addToQueue(self):
        pass #TODO: do something here

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
        def __init__(self, name:str, dryMass:int, wetMass:int):
            self.name = name
            self.dryMass = dryMass
            self.wetMass = wetMass

    class PartType:
        """The base class for parts. Mass is measured in Kg."""
        def __init__(self, name: str, MassFunc: Callable[[int,int],int]):
            self.name = name
            self.dryMassFunc = MassFunc
            self.wetMassFunc = MassFunc
        def __call__(self, radius = 0, height = 0):
            return Parts.Part(self.name, self.dryMassFunc(radius, height), self.wetMassFunc(radius, height))

    class ControlUnit(PartType):
        def __init__(self, name: str, massFunc: Callable[[int,int],int]):
            super().__init__(name, massFunc)

    class Thruster(PartType):
        """Mass in kg, thrust in N"""
        def __init__(self, name: str, mass: int, thrust: int, specificImpulse: int):
            super().__init__(name, lambda _,__: mass)
            self.thrust = thrust
            self.specificImpulse = specificImpulse
    
    class FuelTank(PartType):
        def __init__(self, name: str, dryMassFunc: Callable[[int,int],int], wetMassFunc: Callable[[int,int],int]):
            super().__init__(name, dryMassFunc)
            self.wetMassFunc = wetMassFunc

    controlUnits: list[ControlUnit] = [ControlUnit("Mercury Command Pod", massFunc=lambda _,__: 1118)]
    thrusters: list[Thruster] = [Thruster("RocketDyne A7", mass=658, thrust=346_961, specificImpulse=235)]
    fuelTanks: list[FuelTank] = [FuelTank("Cylindrical", dryMassFunc=(lambda r, h: int(densityOfSteel*fuelTankWallThickness*surfaceAreaOfCylinder(r,h))),
                                                         wetMassFunc=(lambda r,h: int(densityOfSteel*fuelTankWallThickness*surfaceAreaOfCylinder(r,h)+densityOfMethalox*volumeOfCylinder(r,h))))]

class SpacecraftDesign:
    def __init__(self, name: str, type: str, controlUnit: str, thrusters: tuple[str, int], fuelTank: tuple[str, tuple[int]]):
        self.name = name
        self.type = type
        thruster, self.numThrusters = thrusters
        thrusterType: Parts.Thruster = findPart(thruster, Parts.thrusters, lambda part: part.name)
        self.thrust = thrusterType.thrust*self.numThrusters
        self.specificImpulse = thrusterType.specificImpulse
        fuelTankName, self.fuelTankDimentions = fuelTank
        self.controlUnit = findPart(controlUnit, Parts.controlUnits, lambda part: part.name)()
        self.thrusters = thrusterType()
        self.fuelTank = findPart(fuelTankName, Parts.fuelTanks, lambda part: part.name)()
        self.wetMass = sum([part.wetMass for part in [self.controlUnit,self.fuelTank,*[self.thrusters for _ in range(self.numThrusters)]]])
        self.dryMass = sum([part.dryMass for part in [self.controlUnit,self.fuelTank,*[self.thrusters for _ in range(self.numThrusters)]]])
        self.deltaV = self.specificImpulse*earthSurfaceGravity*log(self.wetMass/self.dryMass) #Should work I think.

class Satelite:
    def __init__(self, mass):
        self.mass = mass

class Satelites:
    tutorial = Satelite(250)

def findPart(name: str, partType: Iterable[Parts.PartType], partAttribute: Callable[[Parts.PartType], str]):
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
                f"First, we must design and launch a rocket. In the drawing board, make an Earth second Stage rocket which can carry {Satelites.tutorial.mass}kg to orbit.",
                "Next, design a first stage rocket capable of lifting the first stage to a suborbital trajectory.",
                "Now that we have all that we need, we can launch out first rocket! On the Earth Rocket Assembly Panel, select the Tutorial satelite and your 2 rocket stages, and press LAUNCH."]

def update():
    global researchSpeed
    researchSpeed = researcherCount*researcherEfficiency