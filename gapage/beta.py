# -*- coding: utf-8 -*-
'''
This a place to put functions that are in development.
'''
import gapageconfig, gapdb, dictionaries

def RangeTable_NEW(sp, outDir, state=False, includeMigratory=True, includeHistoric=True):
    '''
    (string, string, string, string, string) -> string

    Creates a comma-delimited text file of the species' range, with fields indicating
        12-digit HUC, origin, presence, reproductive use, and seasonality. Returns
        the full, absolute path to the output text file.

    Arguments:
    sp -- The species six-character unique GAP code
    outDir -- The directory within which you wish to place the output text file
    state -- An optional parameter to indicate a state to which you wish to
        limit the result
    includeMigratory -- An optional boolean parameter indicating whether to
        include migratory range in the output. By default, it is set to True
    includeHistoric -- An optional boolean parameter indicating whether to
        include historic/extirpated range in the output. By default, it is set
        to True

    Example:
    >>> RangeTable('mNAROx', 'My_Range_Folder', state="OH")
    ''' 
    import pandas as pd, os
    try:
        # Ensure that the output directory exists if the directory exists, go on
        # If the directory does not yet exist, create it and all necessary parent directories
        oDir = os.path.abspath(outDir)
        if not os.path.exists(oDir):
            os.makedirs(oDir)
        
        ## Connect to the Species Database
        sppCursor, sppConn = gapdb.ConnectSppDB()
        
        # Build an SQL statement that returns relevant fields in the
        # appropriate taxa table tblRanges_<taxa> using a species code
        # First get the taxon code then get a dataframe of the hucs used by the species, 
        # then clean it up
        tax = dictionaries.taxaDict[sp[0]]
        sql = """SELECT t.strUC, t.strHUC12RNG, intGapOrigin, intGapPres, intGapRepro, intGapSeas
            FROM dbo.tblRanges_""" + tax + """ as t
            WHERE (t.strUC = ?)""" 
        spDF = pd.io.sql.read_sql(sql, sppConn, params=sp.split())
        spDF.drop(["strUC"], axis=1, inplace=True)
        spDF.columns=["HUC12","Origin","Presence","Repro","Season"]
        spDF["HUC12"] = [str(i) for i in spDF["HUC12"]]  
    except Exception as e:
        print("There was an error getting the species dataframe- {0}".format(e))
    
    try:    
        # Apply any filters specified
        if not includeMigratory:
            # Filter out migratory records
            spDF = spDF.loc[(spDF["Season"] != 2) & (spDF["Season"] != 5) & (spDF["Season"] != 8)]
            
        if not includeHistoric:
            # Filter out historic records
            spDF = spDF.loc[spDF["Presence"] != 7]
    except Exception as e:
        print("There was an error filtering the dataframe- {0}".format(e))   
    
    try:    
        if state:
            # Make sure that the user entered a valid state abbreviation or name
            fromAbbr = dictionaries.stateDict_From_Abbr
            toAbbr = dictionaries.stateDict_To_Abbr
            if state in fromAbbr:
                stateName = fromAbbr[state]
            elif state in toAbbr:
                stateName = state
           
           ## Get a dataframe of hucs in the state
            sql_State = """SELECT s.strHUC12RNG
                        FROM dbo.tblBoundaryCrosswalk as s
                        WHERE (s.strStateName = ?)"""
            stateDF = pd.io.sql.read_sql(sql_State, sppConn, params=[stateName])  
            
            #Join the state-huc dataframe with the species-huc dataframe to get hucs in state the 
            #species uses. Clean up.
            spDF = pd.merge(spDF, stateDF, left_on="HUC12", right_on="strHUC12RNG", how='right')
            spDF.drop(["strHUC12RNG"], inplace=True, axis=1)
    except Exception as e:
        print("There was an error with the state-huc dataframe - {0}".format(e))
        
    try:
        #Write final dataframe to csv file    
        spDF.to_csv(outDir + "/" + sp + "_RangeTable.txt", sep=",", index=False)
        # Close the database connection
        sppConn.close()
    except Exception as e:
        print("There was an error writing to txt file - {0}".format(e))
    
    # Return the path to the table
    return outDir + "/" + sp + "_RangeTable.txt"


def MakeRemapList(mapUnitCodes, reclassValue):
    '''
    (list, integer) -> list of lists

    Returns a RemapValue list for use with arcpy.sa.Reclassify()

    Arguments:
    mapUnitCodes -- A list of land cover map units that you with to reclassify.
    reclassValue -- The value that you want to reclassify the mapUnitCodes that you
        are passing to.

    Example:
    >>> MakeRemap([1201, 2543, 5678, 1234], 1)
    [[1201, 1], [2543, 1], [5678, 1], [1234, 1]]
    '''
    remap = []
    for x in mapUnitCodes:
        o = []
        o.append(x)
        o.append(reclassValue)
        remap.append(o)
    return remap  
            
def ReclassLandCover(MUlist, reclassTo, keyword, workDir):
    '''
    (list) -> map
    
    Builds a national map of select systems from the GAP Landcover used in species
        modeling. Takes several hours to run.
        
    Arguments:
    MUlist -- A list of land cover map unit codes that you want to reclass.
    reclassTo -- Value to reclass the MUs in MUlist to.
    keyword -- A keyword to use for output name.  Keep to <13 characters.
    workDir -- Where to save output and intermediate files.
    '''    
    try:
        import arcpy
        arcpy.CheckOutExtension("Spatial")
        
        #Some environment settings  
        LCLoc = gapageconfig.land_cover + "/"
        arcpy.env.overwriteOutput = True
        arcpy.env.cellSize = "30"
        arcpy.env.snapraster = gapageconfig.snap_raster
        
        #Get list of regional land covers to reclassify, reset workspace to workdir.
        arcpy.env.workspace = LCLoc
        regions = arcpy.ListRasters()
        regions  = [r for r in regions if r in ['lcgap_gp', 'lcgap_ne', 'lcgap_nw', 'lcgap_se',
                                                'lcgap_sw', 'lcgap_um']]
        arcpy.env.workspace = workDir
        
        #Make a remap object
        remap = arcpy.sa.RemapValue(MakeRemapList(MUlist, reclassTo))
        
    #    # Reclass the first region
    #    seed = arcpy.sa.Raster(LCLoc + regions[0])
    #    seed = arcpy.sa.Reclassify(seed, "VALUE", remap, "NODATA")
    #    seed.save(workDir + "TT")
        
        #A list to append to
        MosList = []
        
        #Reclass the rest of the regions
        for lc in regions:
            grid = arcpy.sa.Raster(LCLoc + lc)
            RegReclass = arcpy.sa.Reclassify(grid, "VALUE", remap, "NODATA")
            MosList.append(RegReclass)
            RegReclass.save(workDir + "TT" + lc)
        
        #Mosaic regional reclassed land covers
        arcpy.management.MosaicToNewRaster(MosList, workDir, keyword,"", "", 
                                           "", "1", "MAXIMUM", "")
        #arcpy.management.CalculateStatistics(workDir + "\\" + keyword)
        #arcpy.management.BuildPyramids(workDir + "\\" + keyword)
    except:
        print "May not have been able to load arcpy"


def ProcessRichnessNew(spp, groupName, outLoc, modelDir, season, interval_size, log, expand=False):    
    '''
    (list, str, str, str, str, int, str) -> str, str

    Creates a species richness raster for the passed species. Also includes a
      table listing all the included species. Intermediate richness rasters are
      retained. That is, the code processes the rasters in groups of the given interval
      size, to keep from overloading ArcPy's cell statistics function; the intermediate
      richness rasters are retained for spot-checking and for potential re-running of 
      species subsets. Refer to the output log file for a list of species included in 
      each intermediate raster as well as the code that was run for the process.

    Returns the path to the output richness raster and the path to the species
      table.

    Arguments:
    spp -- A list of GAP species codes to include in the calculation
    groupName -- The name you wish to use to identify the output directories
        and files (e.g., 'raptors')
    outLoc -- The directory in which you wish to place output and intermediate files.
    modelDir -- The directory that holds all of the GAP habitat map .tifs needed for the 
        analysis.
    season -- Seasonal criteris for reclassifying the output.  Choose "Summer", "Winter", 
        or "Any". "Any" will reclassify output so that any value > 0 gets reclassed to "1" and
        is the default. 
    interval_size -- How many rasters to include in an intermediate batch.  20 is a good number.
    log -- Path and name of log file to save print statements, errors, and code to.  Recommended
        location is "os.path.join(outLoc, 'log_' + groupName + '.txt')"
    expand -- Default to False.  If you set to true, then each reclassed raster will be added to
        a raster of CONUS extent with the top, left 9 pixels having a value of 1, and all others 
        with a value of zero.  Doing this provides a check that each model was added during the 
        processing, but it slows things down A LOT.  The CONUS extent grid lives in the GAPage
        data directory.

    Example:
    >>> ProcessRichness(['aagtox', 'bbaeax', 'mnarox'], 'MyRandomSpecies', 
                        outLoc='C:/GIS_Data/Richness', modelDir='C:/Data/Model/Output',
                        season="Summer", interval_size=20, 
                        log='C:/GIS_DATA/Richness/log_MyRandomSpecies.txt')
    C:\GIS_Data\Richness\MyRandomSpecies_04_Richness\MyRandomSpecies.tif, C:\GIS_Data\Richness\MyRandomSpecies.csv
    '''    
    
    import os, datetime, arcpy, shutil  
    arcpy.CheckOutExtension('SPATIAL')
    arcpy.env.overwriteOutput=True
    arcpy.env.extent = 'MAXOF'
    arcpy.env.pyramid = 'NONE'
    
    ############################################# create directories for the output
    ###############################################################################
    starttime = datetime.datetime.now()       
    scratch = os.path.join(outLoc, groupName + '_01_scratch')
    reclassDir = os.path.join(outLoc, groupName + '_02_reclassed')
    intDir = os.path.join(outLoc, groupName + '_03_Richness_intermediate')
    outDir = os.path.join(outLoc, groupName + '_04_Richness')
    for x in [scratch, reclassDir, intDir, outDir]:
        if not os.path.exists(x):
            os.makedirs(x)
    
    ######################################## Function to write data to the log file
    ###############################################################################
    def __Log(content):
        print content
        with open(log, 'a') as logDoc:
            logDoc.write(content + '\n')
    
    ############################### Write a table with species included in a column
    ###############################################################################
    outTable = os.path.join(outDir, groupName + '.csv')
    spTable = open(outTable, "a")
    for s in spp:
        spTable.write(str(s) + ",\n")
    spTable.close()
    
    ###################################################### Write header to log file
    ###############################################################################
    __Log("\n" + ("#"*67))
    __Log("The results from richness processing")
    __Log("#"*67)    
    __Log(starttime.strftime("%c"))
    __Log('\nProcessing {0} species as "{1}".\n'.format(len(spp), groupName).upper())
    __Log('Season of this calculation: ' + season)
    __Log('Table written to {0}'.format(outTable))
    __Log('The species that will be used for analysis:')
    __Log(str(spp) + '\n')
    
    # Maximum number of species to process at once
    interval = interval_size
    # Initialize an empty list to store the intermediate richness rasters
    richInts = list()
    
    ############  Process the batches of species to make intermediate richness maps
    ###############################################################################
    # Iterate through the list interval # at a time
    for x in range(0, len(spp), interval):
        # Grab a subset of species
        sppSubset = spp[x:x+interval]
        # Assigned the species subset a name
        gn = '{0}_{1}'.format(groupName, x)
        # Process the richness for the subset of species
        __Log('Processing {0}: {1}'.format(groupName, spp))  
              
        #########################################  Copy models to scratch directory
        ###########################################################################
        # Get a list of paths to the models on the local machine
        __Log('\tCopying models to local drive')
        # Initialize an empty list to store paths to the local models
        sppLocal = list()
        # For each species
        for sp in sppSubset:
            try:
                # Get the path to the species' raster
                sp = sp.lower()
                startTif = modelDir + "/" + sp
                # Set the path to the local raster
                spPath = os.path.join(scratch, sp)
                # If the species does not have a raster, print a
                # warning and skip to the next species
                if not arcpy.Exists(startTif):
                    __Log('\tWARNING! The species\' raster could not be found -- {0}'.format(sp))
                    raw_input("Fix, then press enter to resume")
                # Copy the species' raster from the  species model output directory to 
                # the local drive
                arcpy.management.CopyRaster(startTif, spPath, nodata_value=0, 
                                            pixel_type="8_BIT_UNSIGNED")
                __Log('\t\t{0}'.format(sp))
                # Add the path to the local raster to the list of species rasters
                sppLocal.append(spPath)    
            except Exception as e:
                __Log('ERROR in copying a model - {0}'.format(e))
        __Log('\tAll models copied to {0}'.format(scratch))
      
       ############################################  Reclassify the batch of models
       ############################################################################
       # Get a list of models to reclassify
        arcpy.env.workspace = reclassDir
        __Log('\tReclassifying')
        # Initialize an empty list to store the paths to the reclassed rasters
        sppReclassed = list()
        # Designate a where clause to use in the conditional calculation
        if season == "Summer":
            wc = "VALUE = 1 OR VALUE = 3"
        elif season == "Winter":
            wc = "VALUE = 2 OR VALUE = 3"
        elif season == "Any":
            wc = "VALUE > 0"
        # For each of the local species rasters
        for sp in sppLocal:
            ############################################################ Reclassify              
            try:
                __Log('\t\t{0}'.format(os.path.basename(sp)))
                # Set a path to the output reclassified raster
                reclassed = os.path.join(reclassDir, os.path.basename(sp))
                # Make sure that the copied model exists, pause if not.
                if not arcpy.Exists(sp):
                    __Log('\tWARNING! The species\' raster could not be found -- {0}'.format(sp))
                    raw_input("Fix, then press enter to resume")
                # Create a temporary raster from the species' raster, setting all
                # values meeting the condition to 1
                tempRast = arcpy.sa.Con(sp, 1, where_clause = wc)
                # Check that the reclassed raster has valid values (should be 1's and nodatas)
                if tempRast.minimum != 1:
                    __Log('\tWARNING! Invalid minimum raster value -- {0}'.format(sp))
                elif tempRast.minimum == 1:
                    __Log('\tValid minimum raster value')
                if tempRast.maximum != 1:
                    __Log('\tWARNING! Invalid maximum raster value -- {0}'.format(sp))
                elif tempRast.maximum == 1:
                    __Log('\tValid maximum raster value')
                if tempRast.mean != 1:
                    __Log('\tWARNING! Invalid mean raster value -- {0}'.format(sp))
                elif tempRast.mean == 1:
                    __Log('\tValid mean raster value')
            except Exception as e:
                __Log('ERROR in reclassifying a model - {0}'.format(e))                
            
            ###################################### Optional: expand to CONUS extent    
            try:
                if expand == True:
                    tempRast = arcpy.sa.CellStatistics([tempRast, gapageconfig.CONUS_extent], 
                                                        "SUM", "DATA")
            except Exception as e:
                __Log('ERROR expanding reclassed raster - {0}'.format(e))
                # Save the reclassified raster
            
            tempRast.save(reclassed)
            # Add the reclassed raster's path to the list
            sppReclassed.append(reclassed)
            # Make sure that the reclassified model exists, pause if not.
            if not arcpy.Exists(reclassed):
                __Log('\tWARNING! This reclassed raster could not be found -- {0}'.format(sp))
            
        __Log('\tAll models reclassified')
    
        ########################################  Calculate richness for the subset
        ###########################################################################
        try:
            richness = arcpy.sa.CellStatistics(sppReclassed, 'SUM', 'DATA')
            __Log('\tRichness processed')
            outRast = os.path.join(intDir, gn + '.tif')
            richness.save(outRast)
            __Log('\tSaved to {0}'.format(outRast))
            # Add the subset's richness raster to the list of intermediate rasters
            richInts.append(outRast)
        except Exception as e:
            __Log('ERROR in making intermediate richness - {0}'.format(e))
        
        ############# If the expand option used, check max count to see if it right
        ###########################################################################
        if expand == True:
            try:
                __Log('Checking intermediate raster count')        
                if richness.maximum != len(sppSubset):
                    __Log('A raster was skipped in intermediate richness calculation...quiting')
                    quit
                elif richness.maximum == len(sppSubset):
                    __Log('Intermediate richness used the right number of rasters')
            except Exception as e:
                __Log('ERROR in checking intermediate richness raster count - {0}'.format(e))
          
        ################  Delete each of the copied and reclassified species models
        ###########################################################################
        try:
            for rast in sppReclassed:
                arcpy.Delete_management(rast)
            for sp in sppSubset:
                arcpy.Delete_management(os.path.join(scratch, sp))
        except Exception as e:
            __Log('ERROR in deleting intermediate models - {0}'.format(e))
            
    #################  Sum the intermediate rasters to calculate the final richness
    ###############################################################################
    try:
        __Log('Calculating final richness')
        richness = arcpy.sa.CellStatistics(richInts, 'SUM', 'DATA')
        __Log('Richness calculated')
        outRast = os.path.join(outDir, groupName + '.tif')
        __Log('Saving richness raster to {0}'.format(outRast))
        richness.save(outRast)
        __Log('Richness raster saved.')    
    except Exception as e:
        __Log('ERROR in final richness calculation - {0}'.format(e))
    
    ############# If the expand option used, check max count to see if it right
    ###########################################################################
    if expand == True:
        try:
            __Log('Checking final richness raster count')        
            if richness.maximum != len(spp):
                __Log('A raster(s) was skipped somewhere...quiting')
                quit
            elif richness.maximum == len(spp):
                __Log('Final richness has the right number of rasters')
        except Exception as e:
            __Log('ERROR in checking intermediate richness raster count - {0}'.format(e))
      
    shutil.rmtree(scratch)
    shutil.rmtree(reclassDir)
    
    endtime = datetime.datetime.now()
    runtime = endtime - starttime
    __Log("Total runtime was: " + str(runtime))

    return outRast, outTable