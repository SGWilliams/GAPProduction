## Module to create species-specific metadata for a range table or model raster.
##
## Public Function:
##
## SpeciesInputs() -- Gives a list of input data layers used by a species
##
## ScienceBaseCSV() -- Creates a csv file for use in uploading metadata to ScienceBase

def SpeciesInputs(strUC, season='all', publishedOnly=True, conusOnly=True,
                  migratory=False):
    '''
    (string) -> list
    
    Returns a list of input layers used by one of a species' regional-seasonal models.
        Developed for use with updating metadata on ScienceBase.
    
    Arguments:
    strUC -- A gap species code like "bAMROx".
    season -- The season for which you wish to return models. By default, all
        seasons will be assessed. You may enter: 's' or 'summer' for summer
        models; 'w' or 'winter' for winter models; 'y', 'year', 'yearround', or
        'year-round' for year-round models.
    publishedOnly -- Optional boolean parameter to include only published models.
        By default, it is set as False, which assesses models in all stages.
    conusOnly -- Optional boolean parameter to include only models within CONUS.
        By default, it is set as True, which assesses only CONUS models.
    migratory -- Optional boolean parameter to include migratory models.
        By default, it is set as False, which skips migratory models.
    
    Example:
    >>>inputs = SpeciesInputs("bAMREx")
    ['hydrology', 'elevation']
    '''
    import gapmodeling
    # Dictionary of model variables and associated input layers
    input_dict = {'intEdgeEcoWidth': "forest_edge", 'intElevMax': "elevation",
                  'intElevMin': "elevation", 'strAvoid': "forest_edge",
                  'strEdgeType': "forest/open + woodland/shrubland",
                  'strForIntBuffer': "forest_edge", 'strSalinity': "hydrology",
                  'strStreamVel': "hydrology", 'strUseForInt': "forest_edge",
                  'ysnHandModel': "undocumented", 'ysnHydroFW': "hydrology", 
                  'ysnHydroOW': "hydrology", 'ysnHydroWV': "hydrology", 
                  'ysnUrbanExclude': "human_impact_avoidance",
                  'ysnUrbanInclude': "human_impact_avoidance"}
                  
    # Build starter set/list.            
    sp_inputs = set(["natl_GAP_land_cover_ver1.0_(2001)"])
    # Get list of models for the species
    mods = gapmodeling.ModelCodes(strUC, season, publishedOnly, conusOnly, migratory)
    for mod in mods:
        # Get dictionary version of model
        mod_dict = gapmodeling.ModelAsDictionary(mod, ecolSystem="names")
        # Check if model is a handmodel, break out if so.
        if mod_dict["ysnHandModel"] == True:
            sp_inputs = [input_dict['ysnHandModel']]
            break
        # Starter list for model inputs
        mod_inputs = []
        # If a parameter isn't blank (or equivalent), then add to model input list
        for key in mod_dict.keys():
            if type(mod_dict[key]) == float and mod_dict[key] > 0. and key in input_dict:
                mod_inputs.append(input_dict[key])
            if type(mod_dict[key]) == int and mod_dict[key] >= 0 and key in input_dict:
                mod_inputs.append(input_dict[key])
            if type(mod_dict[key]) == bool and mod_dict[key] is True and key in input_dict:
                mod_inputs.append(input_dict[key])
            if type(mod_dict[key]) == list and len(mod_dict[key]) > 0 and key in input_dict:
                mod_inputs.append(input_dict[key])
        sp_inputs = set(mod_inputs) | sp_inputs
    # Return the list of inputs the species uses.
    return list(sp_inputs)


def ScienceBaseCSV(species, publicationDate, csvName):
    '''
    (list, integer, string) -> pandas DataFrame and saved CSV file.
    
    Creates a dataframe and csv file with rows for species in your list and columns for
        each of the pieces of information needed when updating metadata records on 
        ScienceBase for habitat maps.
    
    Notes:
    The "end_date" column pulls from tblUpdateDateTime, but it's unclear how this table
        is and was populated.  Many entries are blank, so this function uses 2013 if the
        model editing field is blank.
    
    Arguments:
    species -- Python list of GAP species codes to process
    publicationDate -- A year to use as the publication date
    csvName -- Path and name of where to save csv file
    
    Example:
    >>>DF = MakeScienceBaseCSV(["aAMBUx", "bCOHAx", "bAMROx", "bCOMEx"], 
                               publicationDate = 2017, csvName="T:/temp/SBTable.csv")    
    '''
    import pandas as pd, gapdb, sciencebase
    # Intialize a dataframe
    DF0 = pd.DataFrame()
    DF0.index.name = "GAP_code"
    
    abstract_text = """This dataset represents a species habitat distribution model for {0}.  These habitat maps are created by applying a <a href="https://www.sciencebase.gov/catalog/item/527d0a83e4b0850ea0518326">deductive habitat model</a> to remotely-sensed data layers within a species' range.""" 
    
    citation_text = """U.S. Geological Survey - Gap Analysis Program, {2}, {0} ({1}) Habitat Map, U.S. Geological Survey data release, https://doi.org/10.5066/{3}."""
    
    # Fill out desired columns
    for sp in species:
        print sp
        nameCom = gapdb.NameCommon(sp)
        nameSci = gapdb.NameSci(sp)
        DF0.loc[sp, "common_name"] = nameCom
        DF0.loc[sp, "scientific_name"] = nameSci
        DF0.loc[sp, "start_date"] = 2008
        try:
            DF0.loc[sp, "end_date"] = gapdb.ProcessDate(sp).year
        except:
            DF0.loc[sp, "end_date"] = 2013
        DF0.loc[sp, "publication_date"] = publicationDate
        DF0.loc[sp, "citation"] = citation_text.format(nameCom, nameSci, publicationDate,
                                                        sciencebase.GetHabMapDOI(sp))
        DF0.loc[sp, "place_keywords"] = "United States" 
        DF0.loc[sp, "theme_keywords"] = "{1}, {0}".format(nameCom, nameSci)
        DF0.loc[sp, "editor"] = gapdb.Who(sp, "edited")
        DF0.loc[sp, "reviewer"] = gapdb.Who(sp, "reviewed")
        DF0.loc[sp, "NatureServe_element_code"] = gapdb.Crosswalk(sp)[1]
        DF0.loc[sp, "TSN_code"] = gapdb.Crosswalk(sp)[2]
        DF0.loc[sp, "Global_SEQ_ID"] = gapdb.Crosswalk(sp)[3]
        DF0.loc[sp, "input_data"] = str(SpeciesInputs(sp))
        DF0.loc[sp, "IPDS"] = "IP-082267"
        DF0.loc[sp, "abstract"] = abstract_text.format(nameCom)
    
    DF0.to_csv(csvName)
    return DF0