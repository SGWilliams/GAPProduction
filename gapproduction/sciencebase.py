## Functions to use for connecting to and interacting with ScienceBase
##

import gapconfig
import gapdb

# The top level ScienceBase Item ID for the GAP habitat maps
habMapCollectionItem = "527d0a83e4b0850ea0518326"

#### Function to establish a connection to ScienceBase
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
    