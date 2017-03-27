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
        sql = """SELECT DISTINCT t.strUC, t.strHUC12RNG, intGapOrigin, intGapPres, intGapRepro, intGapSeas
            FROM dbo.tblRanges_""" + tax + """ as t
            WHERE (t.strUC = ?)""" 
        spDF = pd.io.sql.read_sql(sql, sppConn, params=sp.split())
        if len(spDF) == 0:
            print("ERROR - No range data was retrieved for {0}".format(sp))
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


