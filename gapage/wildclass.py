# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 10:28:52 2016

@author: nmtarr

This module enables you to retrieve pythons sets of groups of GAP LC map units with a common
feature.  Sets can then be intersected, subtracted, etc. for use in model building.  At the 
point of creation, this module isn't complete: many functions/sets are empty.  Sets will be 
built over time and updated.  

This code is based on a pkl file (data/WildlifeMUClassification.pkl) that holds a dictionary 
of sets("classes") that are managed by NMT in an excel workbook.  The pkl may be updated 
periodically, "git pull" to retrieve the updates.

This code can be used to update the function definitions.  Run it in the shell and copy 
and paste the results.

for k in LoadMUSets().keys():   
    functionstring = "def zzz():\n    return set(MUSets['zzz'][0])\nzzz.__doc__ = MUSets['zzz'][1]\n\n"      
    print(functionstring.replace("zzz", k))

"""
import pickle, gapageconfig

def LoadMUSets():
    '''
    () -> dictionary

    For use in model building workflow.  Returns a dictionary with map unit sets
    and their descriptions. Use LoadMUSets().keys() to list all of the map unit
    sets included in the dictionary.
    '''
    filename = open(gapageconfig.wildclass)
    MUSets = pickle.load(filename)
    filename.close()
    return MUSets

MUSets = LoadMUSets()
  
def isHerbaceous():
    return set(MUSets['isHerbaceous'][0])
isHerbaceous.__doc__ = MUSets['isHerbaceous'][1]


def hasSaturatedSoil():
    return set(MUSets['hasSaturatedSoil'][0])
hasSaturatedSoil.__doc__ = MUSets['hasSaturatedSoil'][1]


def isPrairie():
    return set(MUSets['isPrairie'][0])
isPrairie.__doc__ = MUSets['isPrairie'][1]


def isWoodland():
    return set(MUSets['isWoodland'][0])
isWoodland.__doc__ = MUSets['isWoodland'][1]


def hasAnthroForest():
    return set(MUSets['hasAnthroForest'][0])
hasAnthroForest.__doc__ = MUSets['hasAnthroForest'][1]


def hasShoreline():
    return set(MUSets['hasShoreline'][0])
hasShoreline.__doc__ = MUSets['hasShoreline'][1]


def isPlaya():
    return set(MUSets['isPlaya'][0])
isPlaya.__doc__ = MUSets['isPlaya'][1]


def isRegenerating():
    return set(MUSets['isRegenerating'][0])
isRegenerating.__doc__ = MUSets['isRegenerating'][1]


def hasGrass():
    return set(MUSets['hasGrass'][0])
hasGrass.__doc__ = MUSets['hasGrass'][1]


def isIce():
    return set(MUSets['isIce'][0])
isIce.__doc__ = MUSets['isIce'][1]


def hasForest():
    return set(MUSets['hasForest'][0])
hasForest.__doc__ = MUSets['hasForest'][1]


def isForest():
    return set(MUSets['isForest'][0])
isForest.__doc__ = MUSets['isForest'][1]


def isShrubDom():
    return set(MUSets['isShrubDom'][0])
isShrubDom.__doc__ = MUSets['isShrubDom'][1]


def hasOpen():
    return set(MUSets['hasOpen'][0])
hasOpen.__doc__ = MUSets['hasOpen'][1]


def hasDesert():
    return set(MUSets['hasDesert'][0])
hasDesert.__doc__ = MUSets['hasDesert'][1]


def isNeedleTree():
    return set(MUSets['isNeedleTree'][0])
isNeedleTree.__doc__ = MUSets['isNeedleTree'][1]


def isWoodyWetland():
    return set(MUSets['isWoodyWetland'][0])
isWoodyWetland.__doc__ = MUSets['isWoodyWetland'][1]


def hasSteppe():
    return set(MUSets['hasSteppe'][0])
hasSteppe.__doc__ = MUSets['hasSteppe'][1]


def isEmergWetland():
    return set(MUSets['isEmergWetland'][0])
isEmergWetland.__doc__ = MUSets['isEmergWetland'][1]


def hasShrubDom():
    return set(MUSets['hasShrubDom'][0])
hasShrubDom.__doc__ = MUSets['hasShrubDom'][1]


def hasBroadTree():
    return set(MUSets['hasBroadTree'][0])
hasBroadTree.__doc__ = MUSets['hasBroadTree'][1]


def isSagebrush():
    return set(MUSets['isSagebrush'][0])
isSagebrush.__doc__ = MUSets['isSagebrush'][1]


def hasBarren():
    return set(MUSets['hasBarren'][0])
hasBarren.__doc__ = MUSets['hasBarren'][1]


def hasRocky():
    return set(MUSets['hasRocky'][0])
hasRocky.__doc__ = MUSets['hasRocky'][1]


def isDeveloped():
    return set(MUSets['isDeveloped'][0])
isDeveloped.__doc__ = MUSets['isDeveloped'][1]


def isSandy():
    return set(MUSets['isSandy'][0])
isSandy.__doc__ = MUSets['isSandy'][1]


def hasPrairie():
    return set(MUSets['hasPrairie'][0])
hasPrairie.__doc__ = MUSets['hasPrairie'][1]


def hasArid():
    return set(MUSets['hasArid'][0])
hasArid.__doc__ = MUSets['hasArid'][1]


def isGravel():
    return set(MUSets['isGravel'][0])
isGravel.__doc__ = MUSets['isGravel'][1]


def isBarren():
    return set(MUSets['isBarren'][0])
isBarren.__doc__ = MUSets['isBarren'][1]


def hasEphemeralPool():
    return set(MUSets['hasEphemeralPool'][0])
hasEphemeralPool.__doc__ = MUSets['hasEphemeralPool'][1]


def isWetland():
    return set(MUSets['isWetland'][0])
isWetland.__doc__ = MUSets['isWetland'][1]


def isSaturatedSoil():
    return set(MUSets['isSaturatedSoil'][0])
isSaturatedSoil.__doc__ = MUSets['isSaturatedSoil'][1]


def isOpen():
    return set(MUSets['isOpen'][0])
isOpen.__doc__ = MUSets['isOpen'][1]


def hasNeedleTree():
    return set(MUSets['hasNeedleTree'][0])
hasNeedleTree.__doc__ = MUSets['hasNeedleTree'][1]


def isMudflat():
    return set(MUSets['isMudflat'][0])
isMudflat.__doc__ = MUSets['isMudflat'][1]


def hasSandy():
    return set(MUSets['hasSandy'][0])
hasSandy.__doc__ = MUSets['hasSandy'][1]


def isSaltwater():
    return set(MUSets['isSaltwater'][0])
isSaltwater.__doc__ = MUSets['isSaltwater'][1]


def hasPlantation():
    return set(MUSets['hasPlantation'][0])
hasPlantation.__doc__ = MUSets['hasPlantation'][1]


def hasHerbaceous():
    return set(MUSets['hasHerbaceous'][0])
hasHerbaceous.__doc__ = MUSets['hasHerbaceous'][1]


def isGrass():
    return set(MUSets['isGrass'][0])
isGrass.__doc__ = MUSets['isGrass'][1]


def isRiparian():
    return set(MUSets['isRiparian'][0])
isRiparian.__doc__ = MUSets['isRiparian'][1]


def hasRiparian():
    return set(MUSets['hasRiparian'][0])
hasRiparian.__doc__ = MUSets['hasRiparian'][1]


def hasWoodland():
    return set(MUSets['hasWoodland'][0])
hasWoodland.__doc__ = MUSets['hasWoodland'][1]


def isRowCrop():
    return set(MUSets['isRowCrop'][0])
isRowCrop.__doc__ = MUSets['isRowCrop'][1]


def hasRegenerating():
    return set(MUSets['hasRegenerating'][0])
hasRegenerating.__doc__ = MUSets['hasRegenerating'][1]


def isDesert():
    return set(MUSets['isDesert'][0])
isDesert.__doc__ = MUSets['isDesert'][1]


def isMixedTree():
    return set(MUSets['isMixedTree'][0])
isMixedTree.__doc__ = MUSets['isMixedTree'][1]


def hasWoodyWetland():
    return set(MUSets['hasWoodyWetland'][0])
hasWoodyWetland.__doc__ = MUSets['hasWoodyWetland'][1]


def hasIce():
    return set(MUSets['hasIce'][0])
hasIce.__doc__ = MUSets['hasIce'][1]


def isArid():
    return set(MUSets['isArid'][0])
isArid.__doc__ = MUSets['isArid'][1]


def isAquatic():
    return set(MUSets['isAquatic'][0])
isAquatic.__doc__ = MUSets['isAquatic'][1]


def hasWetland():
    return set(MUSets['hasWetland'][0])
hasWetland.__doc__ = MUSets['hasWetland'][1]


def hasSagebrush():
    return set(MUSets['hasSagebrush'][0])
hasSagebrush.__doc__ = MUSets['hasSagebrush'][1]


def hasGravel():
    return set(MUSets['hasGravel'][0])
hasGravel.__doc__ = MUSets['hasGravel'][1]


def hasMixedTree():
    return set(MUSets['hasMixedTree'][0])
hasMixedTree.__doc__ = MUSets['hasMixedTree'][1]


def isOrchard():
    return set(MUSets['isOrchard'][0])
isOrchard.__doc__ = MUSets['isOrchard'][1]


def hasEmergWetland():
    return set(MUSets['hasEmergWetland'][0])
hasEmergWetland.__doc__ = MUSets['hasEmergWetland'][1]


def isSteppe():
    return set(MUSets['isSteppe'][0])
isSteppe.__doc__ = MUSets['isSteppe'][1]


def isShoreline():
    return set(MUSets['isShoreline'][0])
isShoreline.__doc__ = MUSets['isShoreline'][1]


def isRocky():
    return set(MUSets['isRocky'][0])
isRocky.__doc__ = MUSets['isRocky'][1]


def hasSaltwater():
    return set(MUSets['hasSaltwater'][0])
hasSaltwater.__doc__ = MUSets['hasSaltwater'][1]


def isAnthro():
    return set(MUSets['isAnthro'][0])
isAnthro.__doc__ = MUSets['isAnthro'][1]


def isBroadTree():
    return set(MUSets['isBroadTree'][0])
isBroadTree.__doc__ = MUSets['isBroadTree'][1]