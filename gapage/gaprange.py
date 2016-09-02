## This module facilitates common tasks involving GAP ranges.
##
## Public variables:
##
## HUCs -- The path to the CONUS HUCs shapefile
##
## Public functions:
##
## RangeTable() -- Create a comma-delimited table of the species' range, with
##      fields for HUC12 code, presence, origin, season, and reproductive use.
##
## RangeShp() -- Create a shapefile of the species' range
##
## EcoSysInRange() -- Gets a list of ecological systems that occur within the
##      species' range
##
## ListIntroducedSpp() -- Gets a list of species that have any introduced range
##

import os, gapageconfig, gapdb, dictionaries, docs

try:
    import arcpy
    arcpy.CheckOutExtension("Spatial")
    arcpy.env.pyramid = "NONE"
    arcpy.env.overwriteOutput = "TRUE"
    arcpy.env.qualifiedFieldNames = False
except:
    print("Can't load arcpy")

__headingsList = ['Origin', 'Presence', 'Repro', 'Season']

HUCs = gapageconfig.hucs

"""
def GetRangeFile(speciesCode, dissolved=False):
    '''
    (string, [boolean]) -> string

    Returns the path to the species' GAP range shapefile, if it exists.

    Arguments:
    speciesCode -- The species' 6-character GAP unique ID
    dissolved -- An optional, boolean parameter indicating whether you wish to
        return the dissolved range. By default, it is set to False, meaning that
        the file contains individual HUC records and features.
    '''
    # Find the clownfish drive letter
    import paths
    cf = paths.clownfish
    if not cf:
        return False

    # Initialize a 'shp' variable
    shp = False
    # If the user wishes to return the full, HUC-level range
    if not dissolved:
        # For each of the potential directories
        for d in [os.path.join(cf, 'NAT_Data', 'NAT_Ranges'), os.path.join(cf, 'NAT_Data', 'Nat_Ranges_Mammals'), os.path.join(cf, 'NAT_Data', 'Nat_Ranges_Mammals')]:
            # If the species has a range file within that directory, set the shp
            # variable to that path and break the loop
            spShp = os.path.join(d, speciesCode + '.shp')
            if arcpy.Exists(spShp):
                shp = spShp
                break
    # If the user wishes to return the dissolved range
    else:
        spShp = os.path.join(cf, 'NAT_Data', 'NAT_Ranges_dissolved', speciesCode + '.shp')
        # If the dissolved range exists, set the shp variable to its path
        if arcpy.Exists(spShp):
            shp = spShp

    return shp



##class Range:
##    def __init__(self, sp, outputFile, includeMigratory=True, includeHistoric=True):
##        self.sp = sp
##        self.featureClass = outputFile
##        self.outputDirectory = os.path.dirname(self.outputFile)
##        self.__CheckOutputDirectory()
##        self.gdb = self.outputDirectory.endswith('.gdb')
##        self.includeMigratory = includeMigratory
##        self.includeHistoric = includeHistoric
##
##    def __CheckOutputDirectory(self):
##        if self.gdb:
##            if not arcpy.Exists(self.outputDirectory):
##                arcpy.CreateFileGDB_management(os.path.dirname(self.outputDirectory), os.path.basename(self.outputDirectory))
##        else:
##            if not os.path.exists(self.outputDirectory):
##                os.makedirs(self.outputDirectory)
##
##    def __CreateRange(self):
##        pass
##
##    def ClipToState(self, state):
##        pass
##
##    def Dissolve(self):
##        pass
"""

#######################################
##### Private function for verifying/creating a directory
def __CheckDir(outDir):
    '''
    A private function that should be called only by other functions
        within ranges.py.
    '''
    oDir = os.path.abspath(outDir)
    # If the directory exists, return
    if os.path.exists(oDir):
        return
    # If the directory does not yet exist, create it and all necessary
    # parent directories
    else:
        os.makedirs(oDir)
        return



#######################################
##### Private function for creating the table of the species' range
def __CreateText(sp, rangeAtts, outDir):
    '''
    A private function that should be called only by other functions
        within ranges.py.
    '''
    try:
        # Create a text file for the species
        txtFile = os.path.join(outDir, sp + ".txt")

        os.chdir(outDir)

        with open(txtFile, 'w') as outTxt:
            # Headings for the text file
            fieldHeadings = 'HUC12,' + ','.join(__headingsList)
            # Write the headings to the text file
            outTxt.write(fieldHeadings)

            # Write the species' range info to the txt
            for item in rangeAtts:

                # First insert a newline, followed by quotation marks around the HUC code
                outTxt.write('\n"' + item[0] + '"')
                # Then write each subsequent cell from the row
                for subItem in item[1:]:
                    outTxt.write("," + str(subItem))

        schemaBaseList = ["[insertspp.txt]", "Format=CSVDelimited", "Col1=HUC12 Text",
                          "Col2=ORIGIN Short", "Col3=PRESENCE Short", "Col4=REPRO Short", 
                          "Col5=SEASON Short"]
        schemaBase = '\n'.join(schemaBaseList)
        schemaContent = schemaBase.replace('insertspp', sp)

        schemaFile = os.path.join(os.getcwd(), "schema.ini")
        docs.Write(schemaFile, schemaContent)

        if os.path.exists(txtFile):
            return txtFile
        else:
            print 'Range text file was not created.'
    except Exception as e:
        print 'Error in gaprange.__CreateText()'
        print e

#######################################
##### Query class to be used by RangeTable() function
class __RangeQuery:
    try:
        def __init__(self, sp, state=False, includeMigratory=True, includeHistoric=True):
            self.sp = sp
            self.includeHistoric = includeHistoric
            self.includeMigratory = includeMigratory
            self.state = self.__ConfirmState(state)
            self.query = self.__ConstructQuery()

        # Compile the query
        def __ConstructQuery(self):
            # Get the taxon code
            tax = dictionaries.taxaDict[self.sp[0]]
            # Base query
            queryBase = """SELECT DISTINCT rt.strHUC12RNG, intGapOrigin, intGapPres, intGapRepro, intGapSeas
                        FROM dbo.tblRanges_""" + tax + """ AS rt
                        INNER JOIN dbo.tblBoundaryCrosswalk AS bc
                        ON rt.strHUC12RNG = bc.strHUC12RNG """
            # List of where statements
            wheres = ['(rt.strUC = ?)']
            # Add the appropriate where statements
            if self.state:
                wheres.append('(bc.strStateName=\'' + self.state + '\')')
            if not self.includeHistoric:
                wheres.append('(intGapPres<>4)')
            if not self.includeMigratory:
                wheres.append('(intGapSeas<>2)')
            # Combine the where statements
            queryWhere = 'WHERE ' + ' AND '.join(wheres) + ';'
            # Return the full query
            return queryBase + queryWhere

        # Ensure that the passed state is valid
        def __ConfirmState(self, state):
            # Make sure that the user entered a valid state abbreviation or name
            fromAbbr = dictionaries.stateDict_From_Abbr
            toAbbr = dictionaries.stateDict_To_Abbr
            if state in fromAbbr:
                state = fromAbbr[state]
            elif state in toAbbr:
                pass
            return state
            
    except Exception as e:
        print 'Error in gaprange.__RangeQuery()'
        print e


#######################################
##### Function for creating the species' range table in comma-delimited
##### text format.
def RangeTable(sp, outDir, state=False, includeMigratory=True, includeHistoric=True):
    '''
    (string, string, [string]) -> string

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
    >>> RangeTable('mNAROx', 'My_Range_Folder')
    '''
    try:
        # Ensure that the output directory exists
        __CheckDir(outDir)

        qry = __RangeQuery(sp, state, includeMigratory, includeHistoric)

        rangeAtts = __RunQuery(qry)

        # If the query returned something
        if rangeAtts:
            # Call the CreateText() function to create a text file table
            rText = __CreateText(sp, rangeAtts, outDir)
        # If the query returned nothing, notify the user and return False
        else:
            print "\t%s does not have any published range rows in the species database." % sp
            return False

        # Return the text file.
        return rText
    except Exception as e:
        print 'Error in gaprange.RangeTable()'
        print e

def __RunQuery(qry):
    try:
        # Connect to the database
        sppCursor, sppConn = gapdb.ConnectSppDB()
        # Get the range table for the species
        rangeAtts = sppCursor.execute(qry.query, qry.sp).fetchall()
        # Close the database connection
        sppConn.close()

        return rangeAtts
    except Exception as e:
        print 'Error in gaprange.__RunQuery()'
        print e


#######################################
##### Private function for creating the range shapefile from the table
def __CreateRange(sp, rTable, outDir):
    '''
    A private function that should be called only by other functions
        within ranges.py.
    '''
    try:
        import arcpy
        arcpy.env.workspace = outDir
        arcpy.env.scratchWorkspace = outDir
    
        try:
            # Search for a nationwide HUC layer
            shpHUCs = gapageconfig.hucs
            if not shpHUCs:
                raise Exception('A national HUCs shapefile could not be located.')
    
            # Create a feature layer from the HUCs
            hucLyr = 'hucs'
            arcpy.MakeFeatureLayer_management(shpHUCs, hucLyr)
    
            try:
                # Join the species' range table to the HUCs layer
                arcpy.AddJoin_management(hucLyr, 'HUC12RNG', rTable, 'HUC12', 'KEEP_COMMON')
    
                outShp = os.path.join(outDir, sp + ".shp")
                # Export the joined layer to a shapefile
                arcpy.CopyFeatures_management(hucLyr, outShp)
            except Exception as e:
                print e
            finally:
                d = arcpy.Describe(hucLyr)
                if d.dataType == 'FeatureLayer':
                    arcpy.Delete_management(hucLyr)

            return outShp
        except Exception as e:
            print 'Error in gaprange.__CreateRange()'
            print e
    
    except:
        print("Couldn't load arcpy")


#######################################
##### Private function for deleting extraneous fields from the shapefile
def __DelFields(shp):
    '''
    A private function that should be called only by other functions
        within ranges.py.
    '''
    try:
        import arcpy
        # A list of fields to be deleted
        fields = ['Shape_Leng','Shape_Area','HUC12','HUC12RNG','OBJECTID','HUC_8','HUC_10']
        # Delete the fields
        for field in fields:
            try:
                arcpy.DeleteField_management(shp, field)
            except Exception as e:
                pass
    ##            print 'Exception in gaprange.__DelFields: %s;\n\tCould not delete %s' % (os.path.abspath(shp), field)
    ##            print e

    except:
        print("Couldn't load arcpy")

#######################################
##### Function for creating a species' range shapefile
def RangeShp(sp, outDir=os.getcwd(), dissolve=False, state=False, includeMigratory=True, 
             includeHistoric=True, HUCs=True):
    '''
    (string, string, [boolean], [string], [boolean], [boolean], [boolean]) -> string

    Creates a shapefile of the species' range and returns the full absolute
        path to the shapefile.

    Arguments:
    sp -- The species' six-character unique GAP code
    outDir -- The directory within which you wish to place the output shapefile
    dissolve -- Optional argument; a boolean indicating whether you wish to
        dissolve the output. The default is False.
    state -- An optional parameter to indicate a state to which you wish to
        limit the result
    includeMigratory -- An optional, boolean parameter indicating whether to
        include migratory range in the output. By default, it is set to True
    includeHistoric -- An optional, boolean parameter indicating whether to
        include historic/extirpated range in the output. By default, it is set
        to True
    HUCs -- An optional, boolean parameter only effective when state is not
        False. Indicates whether you wish to clip the range to the HUCs that
        intersect the passed state (True) or to the administrative boundaries of
        the state (False). By default, it is set to True.

    Example:
    >>> RangeShp('mNAROx', 'My_ranges')
    '''
    try:
        import arcpy
        try:
            # Make sure that the output directory exists
            __CheckDir(outDir)
    
            # Get the working directory
            initialCWD = os.getcwd()
    
            # Set the workspace and working directory
            arcpy.env.scratchWorkspace = outDir
            arcpy.env.workspace = outDir
            os.chdir(outDir)
    
            # Call the RangeTable() function
            rTable = RangeTable(sp, outDir, state, includeMigratory, includeHistoric)
    
            # Call the CreateRange() function
            outShp = __CreateRange(sp, rTable, outDir)
    
            # Delete the range table
            arcpy.Delete_management(rTable)
    
            # Call the function to delete unncessary fields
            __DelFields(outShp)
    
            # If the user submitted the argument to dissolve the output...
            if dissolve == True:
                __Dissolve(sp, outShp)
    
            # If a state was passed and HUCs is False
            if state and not HUCs:
                # Clip the file to the state's administrative boundaries
                __AdministrativeBoundary(outShp, state)
    
            outFile = os.path.join(outDir, outShp)
    
            # Set the working directory back to what it was prior to this function
            os.chdir(initialCWD)
    
            if arcpy.Exists(outFile):
                return outFile
                
        except Exception as e:
            print 'Error in gaprange.RangeShp()'
            print e

    except:
        print("Couldn't load arcpy")        

def __Dissolve(sp, outShp):
    '''
    Private function optionally called by RangeShp()
    '''
    try:
        import arcpy
        outDiss1 = sp + 'diss1.shp'
        outDiss2 = sp + 'diss2.shp'
        # Dissolve the range twice, because nationwide ranges often result in large
        # blocks not being dissolved on the first run.
        arcpy.Dissolve_management(outShp, outDiss1, __headingsList)
        # Delete the undissolved range
        arcpy.Delete_management(outShp)
        arcpy.Dissolve_management(outDiss1, outDiss2, __headingsList)
        # Delete the first dissolved range
        arcpy.Delete_management(outDiss1)
        # Rename the dissolved range
        arcpy.Rename_management(outDiss2, os.path.basename(outShp))
        return
    except:
        print("May not have been able to load arcpy")


def __AdministrativeBoundary(inShp, state):
    '''
    Private function optionally called by RangeShp()
    '''
    try:
        import arcpy
        arcpy.env.scratchWorkspace = os.path.basename(inShp)
        arcpy.env.workspace = os.path.basename(inShp)
        try:
            inShpSplit = inShp.split('.')
            inShpTemp = inShpSplit[0] + '_TEMP.' + inShpSplit[1]
            if arcpy.Exists(inShpTemp):
                arcpy.Delete_management(inShpTemp)
            arcpy.Rename_management(inShp, inShpTemp)
    
            import states
            stateLyr = states.GetStateLayer(state)
    
            arcpy.Clip_analysis(inShpTemp, stateLyr, inShp)
            arcpy.Delete_management(inShpTemp)
    
        except Exception as e:
            print 'ERROR in __AdministrativeBoundary()'
            print e
    except:
        print("May not have been able to load arcpy")


#######################################
##### Public function to get a list of ecological systems that occur within
##### the species' range.
def EcoSysInRange(sp, season=1, regions=[]):
    '''
    (str, [int], [list]) -> list

    Returns a list of ecological systems that occur within the species range.

    Arguments:
    sp -- The species six-character GAP code.
    season -- An optional parameter representing the integer code for the season
        of interest. By default, the function only searches within year-round
        range. If you pass either 3 or 4 (winter or summer), the script will
        also search within year-round range, as this function is intended for
        use in setting model parameters.
    regions -- A list of the GAP modeling regions, indicated by region number,
        that you wish to be considered in the analysis. By default, the function
        will determine the regions in which the species occurs, and it will
        process all relevant regions.
    '''
    tDir = gapageconfig.temp_directory
    # If the temp directory doesn't exist, create it
    if os.path.exists(tDir) is False:
        os.makedirs(tDir)
    # Create the species' range shapefile
    spShp = RangeShp(sp, tDir, dissolve=True, includeMigratory=False, includeHistoric=False)

    lcsExtracted = __ClipLC(tDir, spShp, season, regions)

    ess = __ListESS(lcsExtracted)

    # Translate the MU codes to eco sys names
    mus = gapdb.MUCodesToNames(ess)
    # Sort the list alphabetically
    mus.sort()

    return mus


def __ClipLC(tDir, spShp, season, regions):
    # Determine the regions in which the species occurs
    try:
        import arcpy
        regionLCs = __SpRegions(spShp, season, regions)
    
        # Initialize empty list to store the clipped land cover rasters
        lcsExtracted = []
    
        # For each region
        for lcRast in regionLCs:
            # Clip the land cover raster to the species' range
            extracted = arcpy.sa.ExtractByMask(lcRast, spShp)
            # name for the output raster
            outP = os.path.join(tDir, 'lc' + lcRast.split('_')[-1])
            # Save the clipped raster
            extracted.save(outP)
            # Add the clipped raster to the list
            lcsExtracted.append(outP)
    
        return lcsExtracted
    except:
        print("May not have been able to import arcpy")

def __ListESS(lcsExtracted):
    # Initialize an empty list to store the map unit codes
    try:
        import arcpy
        ess = []
    
        # For each clipped raster...
        for i in lcsExtracted:
            # Create a search cursor
            rows = arcpy.SearchCursor(i)
            for row in rows:
                # Get the mu code
                t = int(row.VALUE)
                # If the code is not in the list...
                if t not in ess:
                    # ...add it to the list
                    ess.append(t)
            del row, rows
    
        return ess
    except:
        print("May not have been able to import arcpy")

############################
##### Private function for getting the list of regions in which the species
##### occurs.
def __SpRegions(spShp, season, regions):
    '''
    Private function to be called only by other scripts within this module
    '''
    try:
        import arcpy
        # If the user has requested no specific region(s)
        if regions == []:
            # The where clause
            wc = '"Season" = ' + str(season)
            # If the season is winter or summer...
            if season == 3 or season == 4:
                # ...add content to the where clause to search for year-round range
                # as well
                wc = wc + ' OR "Season" = 1'
    
            # Make a feature layer from the species' range
            spLyr = arcpy.MakeFeatureLayer_management(spShp, 'spLayer', wc)
    
            # Find the modeling regions shapefile
            regionShp = gapageconfig.regions_shapefile
    
            while arcpy.Exists(regionShp) is False:
                regionShp = raw_input("Hey, I can't find the modeling regions shapefile. I'm looking for it at " +
                                      regionShp + ", but it's not there. Where is it?\nFull path to modeling region shapefile: ")
    
            # Make a feature layer of the modeling regions
            regionLyr = arcpy.MakeFeatureLayer_management(regionShp, 'regionLayer')
            # Select regions that intersect the species' range
            arcpy.SelectLayerByLocation_management(regionLyr, "INTERSECT", spLyr)
    
            # Create a search cursor
            rows = arcpy.SearchCursor(regionLyr)
            for row in rows:
                # Add each intersected region to the list
                regions.append(row.REGIONID)
            del row, rows
    
        # The directory where the land cover rasters are stored
        lcDir = paths.GetLCDir()
        while os.path.exists(lcDir) is False:
            lcDir = raw_input("The directory containing the land cover rasters is not found at \n" +
                                    lcDir + ".\nPlease enter the full path to the directory: ")
    
        # Create a list containing the full paths to each relevant region's land
        # cover raster
        regionLCs = [os.path.join(lcDir, 'lcgap_' + dictionaries.regionsDict_Num_To_Abbr[i].lower()) for i in regions]
    
        return regionLCs
    except:
        print("May not have been able to load arcpy")

def ListIntroducedSpp(anyIntroducedHUCs=True):
    '''
    () -> list

    Gets a list of GAP species codes for all species/subspecies that have any
        introduced range.

    Arguments:

    anyIntroducedHUCs - Boolean argument indicating whether species with any
        introduced range--as opposed to all introduced range--are returned.
        By default, it is set to True, meaning that species with even a single
        introduced HUC among any number of native or reintroduced HUCs will be
        returned.
    '''
    qry = '''
    SELECT DISTINCT dbo.tblAllSpecies.strUniqueID
    FROM dbo.tblAllSpecies INNER JOIN dbo.tblRanges_Birds ON dbo.tblAllSpecies.strUniqueID = dbo.tblRanges_Birds.strUC
    WHERE (((dbo.tblRanges_Birds.intGapOrigin)=2))
    AND dbo.tblAllSpecies.strModelStatus = 'Complete'

    UNION

    SELECT DISTINCT dbo.tblAllSpecies.strUniqueID
    FROM dbo.tblAllSpecies INNER JOIN dbo.tblRanges_Mammals ON dbo.tblAllSpecies.strUniqueID = dbo.tblRanges_Mammals.strUC
    WHERE (((dbo.tblRanges_Mammals.intGapOrigin)=2))
    AND dbo.tblAllSpecies.strModelStatus = 'Complete'

    UNION

    SELECT DISTINCT dbo.tblAllSpecies.strUniqueID
    FROM dbo.tblAllSpecies INNER JOIN dbo.tblRanges_Reptiles ON dbo.tblAllSpecies.strUniqueID = dbo.tblRanges_Reptiles.strUC
    WHERE (((dbo.tblRanges_Reptiles.intGapOrigin)=2))
    AND dbo.tblAllSpecies.strModelStatus = 'Complete'

    UNION

    SELECT DISTINCT dbo.tblAllSpecies.strUniqueID
    FROM dbo.tblAllSpecies INNER JOIN dbo.tblRanges_Amphibians ON dbo.tblAllSpecies.strUniqueID = dbo.tblRanges_Amphibians.strUC
    WHERE (((dbo.tblRanges_Amphibians.intGapOrigin)=2))
    AND dbo.tblAllSpecies.strModelStatus = 'Complete';
    '''

    # Connect to the database
    sppCursor, sppConn = gapdb.ConnectSppDB()
    # Get the range table for the species
    sppInt = sppCursor.execute(qry).fetchall()
    sppInt = [i[0] for i in sppInt]

    if not anyIntroducedHUCs:
        qry = '''
            SELECT DISTINCT dbo.tblAllSpecies.strUniqueID
            FROM dbo.tblAllSpecies INNER JOIN dbo.tblRanges_Birds ON dbo.tblAllSpecies.strUniqueID = dbo.tblRanges_Birds.strUC
            WHERE (((dbo.tblRanges_Birds.intGapOrigin)<>2))
            AND dbo.tblAllSpecies.strModelStatus = 'Complete'

            UNION

            SELECT DISTINCT dbo.tblAllSpecies.strUniqueID
            FROM dbo.tblAllSpecies INNER JOIN dbo.tblRanges_Mammals ON dbo.tblAllSpecies.strUniqueID = dbo.tblRanges_Mammals.strUC
            WHERE (((dbo.tblRanges_Mammals.intGapOrigin)<>2))
            AND dbo.tblAllSpecies.strModelStatus = 'Complete'

            UNION

            SELECT DISTINCT dbo.tblAllSpecies.strUniqueID
            FROM dbo.tblAllSpecies INNER JOIN dbo.tblRanges_Reptiles ON dbo.tblAllSpecies.strUniqueID = dbo.tblRanges_Reptiles.strUC
            WHERE (dbo.tblRanges_Reptiles.intGapOrigin<>2)
            AND dbo.tblAllSpecies.strModelStatus = 'Complete'

            UNION

            SELECT DISTINCT dbo.tblAllSpecies.strUniqueID
            FROM dbo.tblAllSpecies INNER JOIN dbo.tblRanges_Amphibians ON dbo.tblAllSpecies.strUniqueID = dbo.tblRanges_Amphibians.strUC
            WHERE (dbo.tblRanges_Amphibians.intGapOrigin <> 2)
            AND dbo.tblAllSpecies.strModelStatus = 'Complete';
            '''

        sppNative = sppCursor.execute(qry).fetchall()
        sppNative = [i[0] for i in sppNative]

        sppInt = list(set(sppInt) - set(sppNative))


    # Close the database connection
    sppConn.close()

    return sppInt


#######################################
##### Main function
def __main():
    pass


# If this script is run directly, call the main function
if __name__ == '__main__':
    __main()
