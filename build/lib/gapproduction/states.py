# A module for accessing state boundaries datasets.
#
# Public functions:
#
# GetStatesLayer() -- Returns an arcpy layer object for the state of interest.
#
# GetStatesShp() -- Returns the path to the shapefile of U.S. state and
#   territory boundaries.
#
# GetStateLayer() -- Returns an arcpy layer object for the state boundary.
#
# CreateStateFC() -- Creates a feature class of the boundaries for the passed
#   state.
#
#

def GetStatesLayer(includeMarine=True):
    '''
    ([boolean]) -> arcpy layer object

    Returns an arcpy layer object for the U.S. states' and territories'
        boundaries.

    Argument:
    includeMarine -- An optional, boolean parameter indicating whether you wish
        to return a layer including both terrestrial and marine administrative
        boundaries or just terrestrial boundaries. By default, it is set to
        True, meaning that all boundaries will be returned.
    '''
    try:
        import arcpy
        # Find the states shapefile
        states = GetStatesShp(includeMarine)
        # Create a feature layer from that file
        sLyr = arcpy.MakeFeatureLayer_management(states, sLyr)
        return sLyr
    except:
        print("May not have been able to load arcpy")


def GetStatesShp(includeMarine=True):
    '''
    ([boolean]) -> string

    Returns the path to a shapefile of the U.S. states' and territories'
        boundaries.

    Argument:
    includeMarine -- An option, boolean parameter indicating whether you wish to
        the shapefile to include both terrestrial and marine administrative
        boundaries or just terrestrial boundaries. By default, it is set to
        True, meaning that all boundaries will be returned.
    '''
    # Find the path to the data directory
    import os, gapconfig
    dd = gapconfig.data_directory
    # Select the proper file based on whether use wishes to include marine
    # territory
    if includeMarine:
        shpName = 'States_Admin.shp'
    else:
        shpName = 'States.shp'
    # The full path to the proper file
    states = os.path.join(dd, shpName)
    # If the file exists, return it
    if os.path.exists(states):
        return states


def GetStateLayer(state, includeMarine=True):
    '''
    (string, [boolean]) -> arcpy layer object

    Returns an arcpy layer object for the state boundary.

    Arguments:
    state -- The two-letter, postal code abbreviation for the state or territory
        of interest.
    includeMarine -- An option, boolean parameter indicating whether you wish to
        return a layer including both terrestrial and marine administrative
        boundaries or just terrestrial boundaries. By default, it is set to
        True, meaning that all boundaries will be returned.
    '''
    try:
        import arcpy
        # Find the states shapefile
        states = GetStatesShp(includeMarine)
    
        sLyr = 'sLyr'
        # Create the where clause depending on the whether the use passed a state
        # abbreviation or a full state name
        if len(state) == 2:
            wc = '"STPOSTAL" = \'' + state + '\''
        else:
            wc = '"STATE" = \'' + state + '\''
    
        # Create the feature layer
        statesLyr = arcpy.MakeFeatureLayer_management(states, sLyr, wc)
    
        return statesLyr
    except:
        print("May not have been able to import arcpy")

def CreateStateFC(state, outputFeatureClass, includeMarine=True):
    '''
    (string, string, [boolean]) -> arcpy layer object

    Creates a feature class of the boundaries for the passed state.

    Arguments:
    state -- The two-letter, postal code abbreviation for the state or territory
        of interest.
    outputFeatureClass -- The path and name of the feature class you wish to
        create.
    includeMarine -- An option, boolean parameter indicating whether you wish to
        create a feature class including both terrestrial and marine
        administrative boundaries or just terrestrial boundaries. By default, it
        is set to True, meaning that all boundaries will be returned.
    '''
    try:
        import arcpy
        # Call the function to get the state's feature layer
        sLyr = GetStateLayer(state, includeMarine)
        # Save the feature layer as a feature class
        arcpy.CopyFeatures_management(sLyr, outputFeatureClass)
        return outputFeatureClass
    except:
        print("May not have been able to import arcpy")

if __name__ == '__main__':
    pass
