# Create a species richness raster for the given species
#
# Public functions:
#
# ProcessRichness() -- Calculate a richness raster from the passed species
#
#

import os, shutil, gapageconfig, gaprasters, tables


# Class to organize information about the species to be included and the
# directories to use
class __Models:
    def __init__(self, spp, groupName, season, outDir=gapageconfig.richness_directory):
        self.spp = spp
        self.groupName = groupName
        self.season = season        
        self.outDir = outDir

        global log
        log = os.path.join(self.outDir, 'log_' + self.groupName + '.txt')

        self.root = outDir
        self.scratch = os.path.join(self.root, self.groupName + '_01_scratch')
        self.reclassDir = os.path.join(self.root, self.groupName + '_02_reclassed')
        self.intDir = os.path.join(self.root, self.groupName + '_03_Richness_intermediate')
        self.outDir = os.path.join(self.root, self.groupName + '_04_Richness')
        self.sppIncluded = list()


# Public function to create a species richness raster
def ProcessRichness(spp, groupName, outDir, season="Year-round"):
    '''
    (list, str, [str]) -> str, str

    Creates a species richness raster for the passed species. Also includes a
      csv table listing all the included species and crosswalk information for
      each. Intermediate richness rasters are retained. That is, the code
      processes the rasters in groups of 20, to keep from overloading ArcPy's
      cell statistics; the intermediate richness rasters are retained for
      spot-checking and for potential re-running of species subsets. Refer to
      the output log file for a list of species included in each intermediate
      raster.

    Returns the path to the output richness raster and the path to the species
      table.

    Arguments:
    spp -- A list of GAP species codes to include in the calculation
    groupName -- The name you wish to use to identify the output directories
        and files (e.g., 'raptors')
    outDir -- An optional parameter, indicating the directory in which you wish
        to place output and intermediate files. By default, it is set to
        C:\Species_Richness
    season -- Seasonal criteris for reclassifying the output.  Choose "Summer", "Winter", 
        or "Year-round".  

    Example:
    >>> ProcessRichness(['aagtox', 'bbaeax', 'mnarox'], 'MyRandomSpecies', \
            r'C:\GIS_Data\Richness')
    C:\GIS_Data\Richness\MyRandomSpecies_04_Richness\MyRandomSpecies.tif, C:\GIS_Data\Richness\MyRandomSpecies.csv
    '''
    try:
        import arcpy
        arcpy.CheckOutExtension('SPATIAL')
        arcpy.env.extent = 'MAXOF'
        arcpy.env.pyramid = 'NONE'
    
        models = __Models(spp, groupName, outDir, season)
    
        __PrepDirs(models)
    
        outRast = __Process(models)
    
        sppTable = __WriteSppTable(models)
    
        shutil.rmtree(models.scratch)
        shutil.rmtree(models.reclassDir)
    
        return outRast, sppTable
    except:
        print("Arcpy may not be available")

def __main():
    pass


# Function to write data to the log file
def __Log(content):
    print content
    with open(log, 'a') as logDoc:
        logDoc.write(content + '\n')


# Function to create directories
def __PrepDirs(models):
    for x in [models.scratch, models.reclassDir, models.intDir, models.outDir]:
        if not os.path.exists(x):
            os.makedirs(x)


# Process the group of species
def __Process(models):
    try:
        import arcpy
        __Log('Processing {0} {1}.\n'.format(len(models.spp), models.groupName).upper())
        __Log(str(models.spp) + '\n')
    
        # Maximum number of species to process at once
        interval = 20
        # Initialize an empty list to store the intermediate richness rasters
        richInts = list()
        # Iterate through the list twenty at a time
        for x in range(0, len(models.spp), interval):
            # Grab a subset of species
            sppSubset = models.spp[x:x+interval]
            # Assigned the species subset a name
            gn = '{0}_{1}'.format(models.groupName, x)
            # Process the richness for the subset of species
            intRast = __ProcessGroup(models, gn, sppSubset)
            # Add the subset's richness raster to the list of intermediate rasters
            richInts.append(intRast)
    
        # Sum the intermediate rasters to calculate the final richness
        __Log('Calculating final richness')
        richness = arcpy.sa.CellStatistics(richInts, 'SUM', 'DATA')
        __Log('\tRichness calculated')
        outRast = os.path.join(models.outDir, models.groupName + '.tif')
        __Log('Saving richness raster to {0}'.format(outRast))
        richness.save(outRast)
        __Log('\tRichness raster saved.')
    
        return outRast
    except:
        print("Couldn't import arcpy")

# Function to process a subset of species
def __ProcessGroup(models, groupName, spp, season):
    try:
        import arcpy
        __Log('Processing {0}: {1}'.format(groupName, spp))
        try:
            # Get a list of paths to the models on the local machine
            sppLocal = __CopyModels(models, spp)
            # Get a list of reclassified models
            sppReclassed = __ReclassModels(models, sppLocal, season)
            # Calculate richness for the subset
            richness = arcpy.sa.CellStatistics(sppReclassed, 'SUM', 'DATA')
            __Log('\tRichness processed')
            outRast = os.path.join(models.intDir, groupName + '.tif')
            richness.save(outRast)
            __Log('\tSaved to {0}'.format(outRast))
    
            # Delete each of the reclassified species models
            for rast in sppReclassed:
                try:
                    arcpy.Delete_management(rast)
                except:
                    pass
    
            return outRast
    
        except Exception as e:
            __Log('ERROR in ProcessGroup() - {0}'.format(e))
    except:
        print("Couldn't load arcpy")

# Function to copy a group of models to the local drive
def __CopyModels(models, spp):
    try:
        import arcpy
        __Log('\tCopying models to local drive')
        # Initialize an empty list to store paths to the local models
        sppLocal = list()
        # For each species
        for sp in spp:
            try:
                # Get the path to the species' raster
                spPathClown = gaprasters.SpModel(sp)
                # Set the path to the local raster
                spPath = os.path.join(models.scratch, sp)
                # If the species does not have a raster, print a
                # warning and skip to the next species
                if not spPathClown:
                    __Log('\tWARNING! The species\' raster could not be found -- {0}'.format(sp))
                    continue
                # Copy the species' raster from the  species model output directory to the local drive
                arcpy.Copy_management(spPathClown, spPath)
                __Log('\t\t{0}'.format(sp))
                # Add the path to the local raster to the list of species rasters
                sppLocal.append(spPath)
            except Exception as e:
                __Log('ERROR in CopyModels() - {0}'.format(e))
        __Log('\tAll models copied to {0}'.format(models.scratch))
        # Return the list of local species rasters
        return sppLocal
    except:
        print("Couldn't import arcpy")

# Function to reclassify the local models
def __ReclassModels(models, sppLocal, season):
    try:
        import arcpy
        __Log('\tReclassifying')
        # Initialize an empty list to store the paths to the reclassed rasters
        sppReclassed = list()
        # For each of the local species rasters
        for sp in sppLocal:
            __Log('\t\t{0}'.format(os.path.basename(sp)))
            try:
                # Set a path to the output reclassified raster
                reclassed = os.path.join(models.reclassDir, os.path.basename(sp))
    
                # The where clause to use in the conditional calculation
                if season == "Summer":
                    wc = "VALUE = 1"
                elif season == "Winter":
                    wc = "VALUE = 2"
                elif season == "Year-round":
                    wc = "VALUE > 0"
                #wc = "VALUE > 0"
                # Create a temporary raster from the species' raster, setting all
                # values that are greater than zero to 1
                tempRast = arcpy.sa.Con(sp, 1, where_clause = wc)
                # Save the reclassified raster
                tempRast.save(reclassed)
                # Add the reclassed raster's path to the list
                sppReclassed.append(reclassed)
    
                # Add the species to the list of those included in the richness
                # calculation
                models.sppIncluded.append(os.path.basename(sp))
    
                # Delete the species' raw local raster
                arcpy.Delete_management(sp)
    
            except Exception as e:
                __Log('\t\tERROR in ReclassModels() - {0}'.format(e))
                pass
        __Log('\tAll models reclassified')
        # Return the list of paths to reclassified rasters
        return sppReclassed
    except:
        print("Couldn't import arcpy")

# Function to create a crosswalk table of species included in the richness
# calculation
def __WriteSppTable(models):
    outTable = os.path.join(models.root, models.groupName + '.csv')
    tables.WriteSppTable(outTable, models.sppIncluded)
    __Log('\tCrosswalk table written to {0}'.format(outTable))
    return outTable



if __name__ == '__main__':
    __main()
    done = raw_input('\nDone.')