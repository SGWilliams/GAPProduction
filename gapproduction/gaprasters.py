## This module facilitates common tasks for processing rasters.
##
##
## The public functions are:
##
## SpModel() -- Finds the path to the species' model 
##
## RemoveEmptyRasters() -- Deletes empty rasters from the passed directory.
##
## CompareRasterProperties() -- Compares the raster properties in the given
##      workspace to those of the reference raster.
##
## RasterPropertiesDictionaries() -- Returns dictionaries of the raster's
##      properties.
##
## GetSnapGrid() -- Returns the path to the GAP snap raster
##
## SubtractRasters() -- Subtracts one raster from another, but avoids the extent
##      and NoData issues of default raster calculations
##
## ValueField() -- Gets the name of the raster's value field
##
## RasterType() -- Gets the name of the raster's file format
##
## SetNullsToValue() -- Change NoData or Null values in a raster to the passed
##       value. Overwrites the input raster. Returns the input raster's path/name.
##
## CheckModelTable() -- Checks to see that a valid raster attribute table exists
##      and that it has rows.
##
## CheckModelExtents() -- Checks a list of species model ouputs to collect a list of
##      ones with extents that are too large relative to the species' range.
## 
## CheckRasterProperties() -- Checks the properties of species model raster.

import os, gapconfig


def CheckRasterProperties(rasters):
    '''
    (list) -> dictionary
    
    A function to check that the properties of a list of rasters, match the desired 
        properties species models (TIFF, Albers projection, 8 bit unsigned pixel type, 
        NoDataValue = 0)
    
    Argument:
    rasters -- A list of rasters to check.

    Examples:
    >>> BadProperties = CheckRasterProperties(arcpy.ListRasters())
    >>> a = BadProperties["WrongNoDataValue"]
    >>> a
    ['amwlfx.tif', 'andsax.tif']
    '''
    import arcpy, time
    
    WrongProjection = []
    WrongNoDataValue = []
    WrongPixelType = []
    WrongFormat = []
    WrongMinimum = []
    WrongMaximum = []
    
    for r in rasters:
        print r
        time.sleep(.1)
        rasObj = arcpy.Raster(r)
        desObj = arcpy.Describe(rasObj)
        
        if desObj.spatialReference.projectionName != "Albers":
            WrongProjection.append(r)
        if desObj.format != "TIFF":
            WrongFormat.append(r)
        if desObj.pixelType != "U8":
            WrongPixelType.append(r)
        if desObj.nodataValue != 0:
            WrongNoDataValue.append(r)
        if rasObj.maximum > 3:
            WrongMaximum.append(r)
        if rasObj.minimum > 3:
            WrongMinimum.append(r)
            
    return {"WrongProjection":WrongProjection, "WrongNoDataValue":WrongNoDataValue,
            "WrongPixelType":WrongPixelType, "WrongFormat":WrongFormat, "WrongMinimum":WrongMinimum,
            "WrongMaximum":WrongMaximum}


def CheckModelExtents(sp, workDir, threshold, modelDir=gapconfig.output_location, 
                      hucTable=gapconfig.HUC_Extents, saveTables=False):
    '''
    (list, string, int, string, string, boolean) -> dictionary, list
    
    Checks the extent of a list of species model raster objects against the extents 
        of  the hucs that the species occurs or occurred in.  Returns a dictionary
        and list.  The dictionary is of species for which the raster is too 
        large compared to the hucs where it occurs and has species names as keys and 
        tuples of what the extent should ideally be as values.  The tuple is formatted
        as (XMin, YMin, XMax, YMax) in hopes that it plays nicely with arcpy.env.extent.
        The list is of species for which there was an error in the process (usually 
        related to range data in the database for hawaiian species). Runtime can be 
        hours to check all models.  Extents are deemed "too big" if one of a raster's 
        corners is more than the threshold distance away from the corner of the corresponding huc.
    
    Arguments:
    sp -- List of species model tifs to check the extent of.  This code assumes 
        they are geotiffs (name ending in ".tif").
    workDir -- The directory within which you wish to place the range tables.  
        Consider a temp location.
    threshold -- Differences above this value in meters will cause a species to be 
        included in the dictionary of models that are too big.  Most model's extents 
        are about 5000 m different from that of the species' range.  
    modelDir -- The directory containing the geotifs to check.
    hucTable -- Path to a csv file with the extents for each huc in Albers 
        projection. Defaults to the table in gapage's data directory.
    saveTables -- True or False for whether you want to save the range tables 
        that will be generated during processing.
    
    Example:
    >>> dicto, listt = CheckModelExtents(['aambux.tif', 'bamgox.tif'], 'C:/temp', 
                          'C:/data/HUCS_Extent.txt', threshold=500000)
    '''
    import pandas as pd, arcpy, os, gaprange, beta
    # Make a list to collect extra large extent models
    errors = []
    oversized = {}
    # Read in the huc extent table as a dataframe
    hucDF = pd.read_csv(hucTable)
    # Filter out unnecessary fields
    hucDF.drop([u'FID', u'OBJECTID', u'STATES', u'HUC_8', u'HUC_10', u'HUC12RNG',
                u'Shape_Leng',], axis=1, inplace=True) 
    print "Printing table minus map differences in this order:"
    print ("XMin", "YMin", "XMax", "YMax")        
    for t in sp:
        r = t[:-4]
        print r
        # Get a dataframe of the species range table
        try:
            sp_table = beta.RangeTable_NEW(r, workDir, includeMigratory=False, 
                                              includeHistoric=False)
            spDF = pd.read_csv(sp_table)
            if saveTables == False:
                os.remove(sp_table)
            else:
                pass
            
            # Join dataframes
            sp_hucDF = pd.merge(hucDF, spDF, how='right', left_on='HUC_12', 
                                right_on='HUC12')
           
           # Get the outer points from species range table
            sp_hucYMin = min(sp_hucDF['YMin'])
            sp_hucYMax = max(sp_hucDF['YMax'])
            sp_hucXMin = min(sp_hucDF['XMin'])
            sp_hucXMax = max(sp_hucDF['XMax'])
            
            # Get the outer points from species raster
            ras = arcpy.Raster(modelDir + t)
            rasprop = arcpy.Describe(ras)
            rasterYMin = rasprop.Extent.YMin
            rasterYMax = rasprop.Extent.YMax
            rasterXMin = rasprop.Extent.XMin
            rasterXMax = rasprop.Extent.XMax
            
            # Make a list to pass along if exent is too big
            extent = [sp_hucXMin, sp_hucYMin, sp_hucXMax, sp_hucYMax]  
            
            # Find problem outputs
            if abs(sp_hucXMax - rasterXMax) > threshold or \
                abs(sp_hucXMin - rasterXMin) > threshold or \
                abs(sp_hucYMax - rasterYMax) > threshold or \
                abs(sp_hucYMin - rasterYMin) > threshold:
                    oversized[t] = tuple(extent)
            
            print(int(sp_hucXMin - rasterXMin), int(sp_hucYMin - rasterYMin),
                  int(sp_hucXMax - rasterXMax), int(sp_hucYMax - rasterYMax))      
        
        except Exception as e:
            print("ERROR - {0}".format(e))
            errors.append(t)
            
    #Return the lists, with duplicates removed.
    return oversized, list(set(errors))
  
      
def CheckModelTable(rasterList):
    '''
    (list) -> dict

    Returns a dictionary of lists, one for each error that the function tests for.
        It looks for tables with a count of values less than zero, raster values
        greater than 3, and rasters that have an issue with search cursors.  
        Designed for testing GAP species model output specifically.

    Argument:
    rasterList -- A list of rasters to check.

    Examples:
    >>> CheckModelTable(['X:/Name/Name.tif'])
    {'Negatives': [], 'cursorProblem': [], 'OverThree': []}
    '''
    try:
        import arcpy, time
        #arcpy.CheckOutExtension("Spatial")
        #arcpy.env.workspace = workspace
        #rasterList = arcpy.ListRasters()

        # MAke empty list to collect rasters with issues        
        noRows = []        
        badCount = []
        cursorProblem = []
        overThree = []
        zero = []

        # Loop through rasters and process
        for d in rasterList:            
            print d
            d = arcpy.Raster(d)
            try:
                # Make an indicator variable for checking whether the cursor is empty,
                # otherwise the cursor will quietly pass tables with no rows.
                RowsOK = False                
                # Make a cursor as a test to see if there's a vat                
                cursor = arcpy.SearchCursor(d)
                for c in cursor:
                    countt = c.getValue("COUNT")
                    if countt < 0 or countt == 0:
                        print d + "  - has bad counts"
                        badCount.append(d.name)
                        #arcpy.management.BuildRasterAttributeTable(d, overwrite=True)
                        #arcpy.management.CalculateStatistics(d)
                        #print "New VAT built" 
                        # Change RowsOK to True since the table has rows.                        
                        RowsOK = True
                    elif countt > 0:
                        # Change RowsOK to True since the table has rows.                          
                        RowsOK = True
                    else:
                        pass
                    time.sleep(.1)
                    value = c.getValue("VALUE")
                    if value > 3:
                        print d + " - has a value greater than 3"
                        overThree.append(d.name)
                    if value == 0:
                        print d + " - has a value equal to 0"
                        zero.append(d.name)
                if RowsOK == False:
                    noRows.append(d.name)
            except:
                print "No Cursor"
                cursorProblem.append(d.name)
        return {"BadCount":badCount, "CursorProblem":cursorProblem, "OverThree":overThree, 
                "NoRows":noRows, "Zeros":zero}
    except:
        print("There was a problem.  Is arcpy accessible?")


def GetSnapGrid():
    '''
    () -> str

    Returns the path to a valid GAP snap raster.
    '''
    import gapconfig
    return gapconfig.snap_raster


def SpModel(sp):
    '''
    (str) -> str

    Return the path to the final, mosaicked distribution raster for the species.
        Returns False if no model is found.

    Argument:
    sp -- The species' 6-character GAP unique ID...capitalization irrelevant.

    Examples:
    >>> SpModel('bBAEAx')
    \\QNAPNAS1\Clownfish\NAT_Data\Nat_Models_Birds\bBAEAx
    >>> SpModel('flurbx')
    False
    '''
    try:
        import arcpy, gapconfig
        sp = sp.lower()
        try:
            # Root directory to search
            outputDir = gapconfig.output_location
            rast = outputDir + "/" + sp
            if arcpy.Exists(rast):
                return rast
            else:
                return False

        except Exception as e:
            print e
    except:
        print("This function is not available without access to arcpy")


def __CompareDescribe(rast, descDic, match):
    '''
    A private function, intended to be called only by other functions within
    this module.

    Compares two rasters' properties to determine whether they match. If a
    property does not match between the two rasters, the property's name and the
    rasters' settings will be printed
    '''
    try:
        import arcpy
        # Create an ArcGIS describe object for the raster
        d = arcpy.Describe(rast)
        # For each entry in the describe dictionary
        for k in descDic.iterkeys():
            # If the current file's property does not match that found in the
            # dictionary...
            if eval('d.' + k) <> descDic[k]:
                # Print a notification
                print d.name, k, eval('d.' + k)
                # and set the test to false
                match = False

        return d, match
    except:
        print("Couldn't import arcpy")



def __CompareRaster(d, rast, rastDic, match):
    '''
    A private function, intended to be called only by other functions within
    this module.
    '''
    try:
        import arcpy
        # Create an ArcGIS raster object
        r = arcpy.Raster(rast)
        # For each entry in the raster dictionary
        for k in rastDic.iterkeys():
            # If the current raster's property does not match that found in the
            # dictionary...
            if eval('r.' + k) <> rastDic[k]:
                # Print a notification
                print d.name, k, eval('r.' + k)
                # and set the test to False
                match = False

        return match
    except:
        print("Couldn't load arcpy")


def __CompareField(d, rast, field, fieldDic, match):
    '''
    A private function, intended to be called only by other functions within
    this module.
    '''
    try:
        import arcpy
        # If the field dictionary is not empty
        if len(fieldDic) > 0:
            # List the fields that match the passed field name
            fL = arcpy.ListFields(rast, field)
            # If matching fields are found
            if len(fL) > 0:
                # Inspect the first of those fields
                f = fL[0]
                # For each entry in the field dictionary
                for k in fieldDic.iterkeys():
                    # If the current field's property does not match that found
                    # in the dictionary...
                    if eval('f.' + k) <> fieldDic[k]:
                        # Print out the identifying information
                        print d.name, k, eval('f.' + k)
                        # and set the test to False
                        match = False
            # If no matching field was found
            else:
                # Print a notification
                print d.name, " - No field named %s." % field
                # and set the test to False
                match = False
        # Otherwise, if the field dictionary is empty, do nothing
        else:
            pass

        return match
    except:
        print("Couldn't load arcpy")


def __Compare(rast, field, descDic, rastDic, fieldDic):
    '''
    A private function, intended to be called only by other functions within
    this module.
    '''
    # Initialize a test variable, and set it to true...this will track
    # whether any properties are mismatched.
    match = True

    d, match = __CompareDescribe(rast, descDic, match)
    match = __CompareRaster(d, rast, rastDic, match)
    match = __CompareField(d, rast, field, fieldDic, match)

    return match


def __ProcessComparisons(rasts, field, descDic, rastDic, fieldDic):
    '''
    A private function, intended to be called only by other functions within
    this module.
    '''
    # Initialize the empty lists to track which rasters matched and which did
    # not.
    matching = []
    nonmatching = []

    for rast in rasts:
        match = __Compare(rast, field, descDic, rastDic, fieldDic)

        if match is True:
            matching.append(rast)
        else:
            nonmatching.append(rast)

    return matching, nonmatching



def CompareRasterProperties(directory, referenceRaster='', wildcard='', field='', omitProperties=[]):
    '''
    (string, [string], [string], [string], [list]) -> list, list

    Compares the raster properties in the given workspace to those of the
        reference raster; prints discrepancies and returns two lists, the first
        of which contains the names of rasters with properties that match those
        of the reference file, and the second of which contains names of rasters
        with properties that do not match those of the reference file.

    Arguments:
    directory -- The directory containing the rasters that you wish to compare
        to the reference raster.
    referenceRaster -- An optional parameter indicating the raster to which you
        wish to compare all other rasters. If no raster is entered, then the
        first raster encountered in the directory will be treated as the
        reference raster.
    wildcard -- An optional parameter indicating the search string that each
        raster name must match in order to be processed. The parameter treats
        asterisks as any number (including zero) of characters. In this way,
        it works just like ArcGIS wildcards, in which '*x' would match species-
        level GAP data, whereas 'x' would only match rasters named exactly 'x'.
    field -- If you wish to assess the presence or properties of a given raster
        attribute, you may enter the exact field name.
    omitProperties -- An optional list indicating the names of properties that
        you do not wish to examine. For example, in comparing the Gap Analysis
        results, one would pass ['maximum', 'pixelType'] as this argument,
        because the rasters all have difference maximum values and they have a
        range of pixelTypes, and we would not want these known differences to
        return mismatches of which we are already aware.

    Examples:
    >>> gappack.gaprasters.CompareRasterProperties(myRasterDirectory)

    >>> gappack.gaprasters.CompareRasterProperties(myRasterDirectory, myCorrectRaster,
                                                   'a*', 'count', ['maximum', 
                                                   'pixelType', 'noDataValue'])
    '''
    try:
        import arcpy, match_and_filter
        # Store the original workspace in order to restore it prior to returning
        oWorkspace = arcpy.env.workspace
        # If the user submitted a reference raster, get the full path to it
        if referenceRaster <> '':
            if os.path.basename(referenceRaster) == referenceRaster:
                refRast = os.path.join(oWorkspace, referenceRaster)
            else:
                refRast = referenceRaster

        # Get the list of rasters to examine
        arcpy.env.workspace = directory
        rasts = arcpy.ListRasters()
        # If the user entered a wildcard, filter the list
        if wildcard <> '':
            rasts = match_and_filter.FilterList(rasts, wildcard)

        # If the user did not submit a reference raster, set it now
        if referenceRaster == '':
            refRast = rasts[0]

        print 'Comparisons will be made to: %s.' % refRast

        # Create the dictionaries that contain the 'correct' values for each
        # property.
        descDic, rastDic, fieldDic = RasterPropertiesDictionaries(refRast, omitProperties, field)

        # Process the comparisons
        matching, nonmatching = __ProcessComparisons(rasts, field, descDic, rastDic, fieldDic)

        arcpy.env.workspace = oWorkspace

        # Return the lists of matching and non-matching rasters
        return matching, nonmatching
    except:
        print("Couldn't load arcpy")



#####################
## Returns three dictionaries, each storing some of the raster's properties
def RasterPropertiesDictionaries(raster, omitProperties=[], field=''):
    '''
    (string, [list], [string]) -> dictionary, dictionary, dictionary

    Returns three dictionaries:
        1) Keys represent the raster's describe property names, with values
            being the actual properties for the given raster
        2) Keys represent the raster's raster property names, with values
            being the actual properties for the given raster
        3) Keys represent the field property names, with values being the actual
            properties for the given field

    Arguments:
    raster -- The raster name or the full path to the raster (if the workspace is not
        set to the raster's directory).
    omitProperties -- An optional list of properties to omit from the results.
    field -- An optional string indicating the field for which you wish to
        return a dictionary of properties.

    Example:
    >>> gap.gaprasters.RasterPropertiesDictionaries(myRaster)

    >>> gap.gaprasters.RasterPropertiesDictionaries(myRaster, field='count')
    '''
    try:
        import arcpy
        # The base properties to use for each data type
        propsDict = {'descProps':['bandCount', 'format', 'datasetType', 'tableType', 'compressionType', 'isInteger', 'primaryField', 'pixelType'], 'rastProps':['minimum', 'hasRAT', 'noDataValue', 'pixelType', 'maximum'], 'fieldProps':['name', 'type', 'length', 'precision', 'isNullable', 'required', 'scale', 'baseName']}

        # Initialize the empty dictionaries for each data type
        descDic = {}
        rastDic = {}
        fieldDic = {}

        # For each item in the base dictionary
        for i in propsDict.iterkeys():
            # Remove items that occur in the 'omitProperties' list
            propsDict[i] = list(set(propsDict[i]) - set(omitProperties))

        # Create a describe object for the raster
        d = arcpy.Describe(raster)
        # Populate a dictionary of the describe properties
        for i in propsDict['descProps']:
            descDic[i] = eval("d." + i)

        # Create a arcgis raster object for the raster
        rast = arcpy.Raster(raster)
        # Populate a dictionary of the raster properties
        for i in propsDict['rastProps']:
            rastDic[i] = eval('rast.' + i)

        # If a field was submitted
        if field <> '':
            # Create a list of available fields
            fs = [i.name.lower() for i in arcpy.ListFields(raster)]
            # If the submitted field is in that list
            if field in fs:
                # Find the appropriate field
                f = arcpy.ListFields(raster, field)[0]
                # Populate a dictionary of the field properties
                for i in propsDict['fieldProps']:
                    fieldDic[i] = eval('f.' + i)
            # If the submitted field name does not match the layer's fields
            else:
                # Notify the user
                print 'The field name that you submitted, "%s", is not a valid field name for the raster %s.' % (field, raster)
                print 'As a result, the field dictionary will be empty.'

        # Return the dictionaries for each data type
        return descDic, rastDic, fieldDic
    except:
        print("Couldn't load arcpy")


#####################
## Function to delete the empty rasters and generate a list of valid rasters:
def RemoveEmptyRasters(directory=False):
    '''
    (string) -> list, list

    Searches the passed directory for empty rasters and deletes them; returns
    a list of the valid rasters remaining in the directory and a list of the
    deleted rasters.

    Argument:
    directory -- An optional parameter indicating the name of the directory or
        the absolute path to the directory you wish to clean up. If no argument
        is entered, the process will run on the current arcpy workspace. In
        either case, the function will reset the workspace to the original arcpy
        workspace prior to returning to the script that called it.
    '''
    try:
        import arcpy
        try:

            # Store the current workspace so that you can return to it later
            originalWrkspc = arcpy.env.workspace

            if directory is False:
                # If the user did not pass a directory, set the directory to the
                # arcpy workspace
                directory = arcpy.env.workspace
            # If the user did pass a directory
            else:
                # Change the workspace to the passed directory
                arcpy.env.workspace = os.path.abspath(directory)

            # Ensure that a valid directory was passed to the function; if not, ask
            # the user to enter one.
            while True:
                if directory is None or os.path.exists(directory) is False:
                    directory = raw_input('The directory that you passed to the function RemoveEmptyRasters\n\
                    does not exist. Please enter a valid directory: ')
                else:
                    break

            # Initialize empty lists to track which rasters are good and which aren't
            goodList = []
            badList = []

            # List rasters
            rasterList = arcpy.ListRasters()

            if len(rasterList) > 0:

                for item in rasterList:
                    try:
                        raster = arcpy.Raster(item)
                        # If raster is empty...maximum values of negative show up in these files,
                        # so we use that to test whether the raster contains any actual distribution
                        if raster.maximum < 0:
                            # Add the raster to the list of deleted rasters
                            badList.append(raster.name)
                            # Delete the raster.
                            arcpy.Delete_management(raster)
                        else:
                            # Add the raster to the list of good rasters
                            goodList.append(raster.name)
                    except:
                        pass

            # Reset the workspace to the original
            arcpy.env.workspace = originalWrkspc

            # Return both lists
            return goodList, badList

        except Exception, e:
            print 'Exception in RemoveEmptyRasters'
            print e.message
            return

    except:
        print("Couldn't load arcpy")

def SubtractRasters(inRaster, subRaster, outRaster):
    '''
    (str, str, str) -> str

    Performs a raster subtraction, but avoids the extent/NoData issues that
        plague the raster calculator.

    Arguments:
    inRaster -- The input raster, from which the subRaster will be subtracted
    subRaster -- The raster containing values to be subtracted from inRaster
    outRaster -- The path/name of the desired output raster
    '''
    try:
        import arcpy
        arcpy.env.extent = 'MAXOF'
        negRaster = arcpy.Raster(subRaster) * -1

        temp = arcpy.sa.CellStatistics([inRaster, negRaster], 'SUM', 'DATA')
        temp.save(outRaster)
        return outRaster

    except:
        print("Couldn't load arcpy")


def ValueField(raster):
    '''
    (str) -> str

    Returns the name of the raster's value field (since capitalization varies
    across raster formats but may be necessary for certain operations)
    '''
    try:
        import arcpy
        fs = [f.name for f in arcpy.ListFields(raster)]
        for x in ['Value', 'VALUE', 'value']:
            if x in fs:
                return x
    except:
        print("Couldn't load arcpy")


def RasterType(raster):
    '''
    (str) -> str

    Returns the name of the raster's file type
    '''
    try:
        import arcpy
        d = arcpy.Describe(raster)
        return d.format
    except:
        print("Couldn't load arcpy")

def SetNullsToValue(raster, value):
    '''
    (str, int/float) -> str

    Change NoData or Null values in a raster to the passed value. Overwrites
      the input raster. Returns the input raster's path/name.

    Note that zeroes will fill the entire square extent of the raster and may
      not be restricted to your area of interest. Changing NoData cells to a
      value can greatly increase the size of your file.

    Arguments:
    raster - The name/path of the raster you wish to update.
    value - The value to which you wish to change NoData cells.
    '''
    try:
        import arcpy
        # A where clause based on the value field name of the input raster
        wc = '{0} = 1'.format(ValueField(raster))
        # Process the value change to a temporary raster
        tempRaster = arcpy.sa.Con(arcpy.sa.IsNull(raster), value, raster, wc)
        # Delete the input raster
        arcpy.Delete_management(raster)
        # Save the temporary raster under the name of the input raster
        tempRaster.save(raster)
        return raster
    except:
        print("Couldn't import arcpy")

if __name__ == '__main__':
    pass
