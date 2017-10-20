'''
Functions to use for connecting to and interacting with ScienceBase
'''

import gapconfig
import gapdb

# The top level ScienceBase Item ID for the GAP habitat maps
habMapCollectionItem = "527d0a83e4b0850ea0518326"


def ConnectToSB(username=gapconfig.sbUserName, password=gapconfig.sbWord):
    """
    (string) -> connection to ScienceBase
    
    Creats a connection to ScienceBase. You will have to enter your password.
    
    Arguments:
    username -- your ScienceBase user name.
    
    Example:
    >> connection = ConnectToSB(username="ntarr@usgs.gov")
    """
    import pysb
    sb = pysb.SbSession()
    sb.login(username, password)
    return sb


def ListHabitatMapIDs():
    """
    () -> list
    
    Returns a list of habitat map IDs by listing child items of the top
    level ScienceBase item for the GAP habitat maps.
    
    Example:
    >> mapIDs = HabitatMapIDs()
    """
    sb = ConnectToSB()
    global habMapCollectionItem
    habitatMapIDs = sb.get_child_ids(habMapCollectionItem)
    return habitatMapIDs


def GetHabMapDOI(strUC):
    """
    (string) -> string
    
    Returns the ScienceBase DOI for the habitat map of the passed
    species/strUC.
    
    Arguments:
    strUC -- A gap species code ("mSEWEx")
    
    Example:
    >> id = GetHabMapDOI("bAMROx")
    """
    cursor, connect = gapdb.ConnectAnalyticDB()
    sql = """SELECT tblTaxa.strDoiHM
             FROM tblTaxa
             WHERE tblTaxa.strUC = ?"""
    doi = cursor.execute(sql, strUC).fetchone()[0]  
    del cursor
    connect.close()
    return str(doi)


def GetHabMapURL(strUC):
    """
    (string) -> string
    
    Returns the ScienceBase URL for the habitat map of the passed
    species/strUC.
    
    Arguments:
    strUC -- A gap species code ("mSEWEx")
    
    Example:
    >> url = GetHabMapURL("bAMROx")
    """
    cursor, connect = gapdb.ConnectAnalyticDB()
    sql = """SELECT tblTaxa.strSbUrlHM
             FROM tblTaxa
             WHERE tblTaxa.strUC = ?"""
    url = cursor.execute(sql, strUC).fetchone()[0]  
    del cursor
    connect.close()
    return str(url)


def GetHabMapID(strUC):
    """
    (string) -> string
    
    Returns the ScienceBase Item ID for the habitat map of the passed
    species/strUC.
    
    Arguments:
    strUC -- A gap species code ("mSEWEx")
    
    Example:
    >> id = GetHabMapID("bAMROx")
    """
    return GetHabMapURL(strUC)[-24:]

    
def HabMapItemCSV(species, publicationDate, csvName):
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
    >>>DF = HabMapItemCSV(["aAMBUx", "bCOHAx", "bAMROx", "bCOMEx"], 
                               publicationDate = 2017, csvName="T:/temp/SBTable.csv")    
    '''
    import pandas as pd, gapdb, gapmodeling
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
        DF0.loc[sp, "citation"] = citation_text.format(nameCom, 
                                                       nameSci, 
                                                       publicationDate, 
                                                       GetHabMapDOI(sp))
        DF0.loc[sp, "place_keywords"] = "United States" 
        DF0.loc[sp, "theme_keywords"] = "{1}, {0}".format(nameCom, nameSci)
        DF0.loc[sp, "editor"] = gapdb.Who(sp, "edited")
        DF0.loc[sp, "reviewer"] = gapdb.Who(sp, "reviewed")
        DF0.loc[sp, "NatureServe_element_code"] = gapdb.Crosswalk(sp)[1]
        DF0.loc[sp, "TSN_code"] = gapdb.Crosswalk(sp)[2]
        DF0.loc[sp, "Global_SEQ_ID"] = gapdb.Crosswalk(sp)[3]
        DF0.loc[sp, "input_data"] = str(gapmodeling.SpeciesInputs(sp))
        DF0.loc[sp, "IPDS"] = "IP-082267"
        DF0.loc[sp, "abstract"] = abstract_text.format(nameCom)
        DF0.loc[sp, "doi"] = GetHabMapDOI(sp)
        DF0.loc[sp, "ScienceBase_url"] = GetHabMapURL(sp)
    
    DF0.to_csv(csvName)
    return DF0