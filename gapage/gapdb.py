## This module facilitates common tasks for querying the GAP Species Database
## and WHRdb.
##
## Due to the scope of this module, and since the functions are automatically
## alphabetized in the full help document, I have inserted, for reference, a
## thematic arrangement of the public functions...
##
## CONNECTING TO THE DATABASES:
##    ConnectGAdb(uid='xxxx', pwd='xxxx')
##        Returns a cursor and a connection within the gap analysis database.
##
##    ConnectSppDB(uid='xxxx', pwd='xxxx')
##        Returns a cursor and connection within the GAP species database.
##
##    ConnectWHR(uid='xxxx', pwd='xxxx')
##        Returns a cursor and connection within the GAP WHRdb.
##
##
##
## SPECIES COMPLETION STATUS:
##
##    ListAllSpecies(completedModels=False)
##        Lists all species
##
##    RangeCompleted(spCode)
##        Checks whether the species has a published range
##
##    ModelCompleted(spCode)
##        Checks whether the species has a published model
##
##    SppModelCompleted(state=False)
##        Gets a list of all species with published models
##
##    SppRangeCompleted(state=False)
##        Gets a list of all species with published range
##
##
##
## STATE INFORMATION:
##    SppInState(state, breedingOnly=False)
##        Gets a list of all the species that occur in the given state. Requires
##            that the species have a published range in order to make the list.
##
##    States(spCode, abbr=False, migratory=False)
##        Returns a list of the states in which the species has range.
##
##    BreedingStates(spCode, abbr=False)
##        Returns a list of the states in which the species has breeding range.
##
##    States_SGCN(spCode, abbr=False)
##        Returns a list of the states in which the species is a SGCN
##
##
##
## SPECIES TAXONOMY/NAMES/CROSSWALKS:
##    Taxonomy(spCode)
##        Returns a tuple of 8 items: GAP species code, class, order, family,
##        genus, species, subspecies, full scientific name, and common name.
##
##    NameClass(spCode)
##        Returns the species' class
##
##    NameCommon(spCode)
##        Returns the species' common name
##
##    NameFamily(spCode)
##        Returns the species' family
##
##    NameGenus(spCode)
##        Returns the species' genus
##
##    NameOrder(spCode)
##        Returns the species' order
##
##    NameSci(spCode)
##        Returns the species' scientific name (Genus species [subspecies])
##
##    NameSpecies(spCode)
##        Returns the species' scientific species name
##
##    NameSubspecies(spCode)
##        Returns the subspecies name, if applicable; otherwise, returns
##        an empty string
##
##    NameDownload(spCode)
##        Gets the download filename
##
##    Crosswalk(spCode)
##        Returns a tuple of 4 items: GAP species code, ELCode, ITIS TSN, and
##            Global_SEQ_ID
##
##    SpInfoCombined(spCode)
##        Returns the full info for the the species, including taxonomy, crosswalk,
##            and range/model completion status.
##
##    Dict_SciNameToCode()
##        Returns a dictionary within which the keys are species scientific names and
##            the keys are GAP codes
##
##
## SPECIES INFO - MISCELLANEOUS:
##    ESA_Status(spCode)
##        Returns the species' ESA status
##
##    GapCase(spCode)
##        Returns an input string in the Gap Code capitalization
##
##    ProcessDate(spCode, x='Model', y='Edited')
##        Gets the date that the species' range or model was created
##        or last edited. Returns the date as a date data type.
##
##    Who(spCode, action="reviewed")
##        Returns the name of a person who worked on a species.
##
##    Related(code)
##        Gets a list of species/subspecies that share the code root (i.e.
##        the first 5 characters of the code). If your argument exceeds five
##        characters, the function will ignore all but the first five. If you submit
##        an argument with fewer than five characters, the function will return all
##        codes that begin with whatever argument you submitted.
##
##
## MAP UNITS:
##
##    AllMUs()
##        Get a list of all possible map units.
##
##    MUCodesToNames(muCodeList)
##        Translates a list of map unit codes into a list of ecological system names.
##            The passed codes can be either strings or integers.
##
##    MUName(muCode)
##        Returns the name of the ecological system that matches the passed map unit
##            code.
##
##    MUCode(muName)
##        Returns the map unit code of the ecological system that matches the passed
##            name.
##
##    MUNamesToCodes(muNameList)
##        Translates a list of ecological system names to map unit codes.
##
##    MuInRegion(mu, region)
##        Returns a boolean indicating whether the map unit occurs within the region.
##
##    MuRegions(mu)
##        Returns a list of the GAP modeling regions (by numeric code) in which the
##            map unit occurs.
##
##    UniqueMUs(inRegion, absentRegions=range(1,7))
##       Get a list of map units unique to the region of interest.
##
##    MUsWithKeyword(keyword)
##       Returns a list of map units (as integers) that contain the keyword
##      in their name or description.
##
##
##
## DUPLICATE RECORDS:   !!!REMOVED July 2016 because not sure what the utility
##     would be and it's dangerous. See older versions for the code.
##
##    RemoveDuplicateRecords(db, uid, pwd, table, ignoreFields=[])
##        Deletes duplicate records from the passed table in the passed database.
##            Returns the number of deleted records as well as the initial/total
##            number of records in the table.
##
##
##    RemoveDuplicateRecordsPreview(db, uid, pwd, table, ignoreFields=[])
##        Returns a list of the records that will be deleted if the RemoveDuplicateRecords()
##            function is called. Also returns the number of records to be deleted and
##            the initial/total number of records in the table.
##
## ADD SPECIES:
##      AddSpecies(inTable, username, pwd)
##          Code for adding a new species to the databases.
##


#######################################
##### Importing other modules and setting global variables

import pyodbc, gapageconfig, tables, sys
from dictionaries import stateDict_From_Abbr, stateDict_To_Abbr, taxaDict


#######################################################################
##########################################################
#############################################
## Database Connections

def ConnectToDB(connectionStr):
    '''
    (str) -> cursor, connection

    Provides a cursor within and a connection to the database

    Argument:
    connectionStr -- The SQL Server compatible connection string for connecting
        to a database

    Example:
    >>> conString = """DRIVER=SQL Server Native Client 11.0;
                   SERVER={0};
                   UID={1};
                   PWD={2};
                   DATABASE=WHRdB;"""
    >>> cursor, connection = ConnectToDB(conString)

    '''
    try:
        con = pyodbc.connect(connectionStr)
    except:
        connectionStr = connectionStr.replace('11.0', '10.0')
        con = pyodbc.connect(connectionStr)

    return con.cursor(), con


#######################################
##### Connect to the Species Database
def ConnectSppDB(uid=gapageconfig.uid, pwd=gapageconfig.password,
                 server=gapageconfig.server, trusted=gapageconfig.trusted):
    '''
    Returns a cursor and connection within the GAP species database.
    '''
    # Species database connection parameters
    sppConStr = """DRIVER=SQL Server Native Client 11.0;
            SERVER={0};
            UID={1};
            PWD={2};
            DATABASE=Species_Database;
            TRUSTED_CONNECTION={3};
            APP=gapage;
            """.format(server, uid, pwd, trusted)

    return ConnectToDB(sppConStr)


#######################################
##### Function to connect to the WHRDB
def ConnectWHR(uid=gapageconfig.uid, pwd=gapageconfig.password,
               server=gapageconfig.server, trusted=gapageconfig.trusted):
    '''
    Returns a cursor and connection within the GAP WHRdb.
    '''
    # WHRDB connection parameters:
    whrConStr = """DRIVER=SQL Server Native Client 11.0;
            SERVER={0};
            UID={1};
            PWD={2};
            DATABASE=WHRdb;
            TRUSTED_CONNECTION={3};
            APP=gapage;
            """.format(server, uid, pwd, trusted)

    return ConnectToDB(whrConStr)


#######################################################################
##########################################################
#############################################
## General


# Returns a list of all species (by GAP code) in the GAP species database
def ListAllSpecies(completedModels=False, CONUSOnly=False):
    '''
    [boolean] -> list

    Returns a list of all species from the species database, but note that the
    CONUSonly argument references the WHRDB.

    Argument:
    completedModels -- An optional, boolean parameter indicating whether you
        wish to return only species that have completed models. By default, it
        is set to False, meaning that all species will be returned.
    '''
    print("!!!completedModels Option doesn't work because the SppDB is not up to date!!!")
    sppCursor, sppCon = ConnectWHR()
    comp = sppCursor.execute("""SELECT DISTINCT strUC FROM dbo.tblAllSpecies""").fetchall()
    del sppCursor
    sppCon.close()

    # Since the SQL query returns a list of tuples, create a list of
    # the first item from each tuple:
    sppList = [str(item[0]) for item in comp]

    if completedModels:
        sppList = [sp for sp in sppList if ModelCompleted(sp)]

    if CONUSOnly:
        sppList = [i for i in sppList if SpInCONUS(i)]

    return sppList


# Returns a dictionary within which the keys are species scientific names and
# the keys are GAP codes
def Dict_SciNameToCode():
    '''
    () -> dict

    Returns a dictionary within which the keys are species scientific names and
      the keys are GAP codes
    '''
    d = {}
    l = ListAllSpecies()

    for i in l:
        try:
            sci = NameSci(i)
            if sci in d.iterkeys():
                print sci
                if i.endswith('x'):
                    d[sci] = i
                else:
                    pass
            else:
                d[sci] = i
        except:
            pass

    return d



#######################################################################
##########################################################
#############################################
## Completion Status

#######################################
##### Function to check if the range is complete
def RangeCompleted(spCode):
    '''
    (string) -> boolean

    Checks whether the species has a published range

    Argument:
    spCode -- the species' unique GAP ID

    Example:
    >>> RangeCompleted("aNRLFx")
    True
    '''
    sppCursor, sppCon = ConnectSppDB()
    comp = sppCursor.execute("""SELECT al.strRangeStatus
                         FROM dbo.tblAllSpecies as al
                         WHERE al.strUniqueID = ?""", spCode).fetchone()

    del sppCursor
    sppCon.close()

    if type(comp) == pyodbc.Row:
        if comp[0].strip() == "Complete":
            return True

    return False


#######################################
##### Function to check if the species' model is complete
def ModelCompleted(spCode):
    '''
    (string) -> boolean

    Checks whether the species has a published model based on the species database

    Argument:
    spCode -- the species' unique GAP ID

    Example:
    >>> ModelCompleted("aNRLFx")
    True
    '''
    sppCursor, sppCon = ConnectSppDB()
    comp = sppCursor.execute("""SELECT al.strModelStatus
                         FROM dbo.tblAllSpecies as al
                         WHERE al.strUniqueID = ?""", spCode).fetchone()

    del sppCursor
    sppCon.close()

    if type(comp) == pyodbc.Row:
        try:
            if comp[0].strip() == "Complete":
                return True
        except:
            pass

    return False


#######################################
##### Function to get a list of all species with completed ranges
def SppRangeCompleted(state=False):
    '''
    () -> list

    Gets a list of all species with published range

    Argument:
    state -- An optional parameter indicating the state of interest. The two-
        letter state postal abbreviation or the full state name are valid. If
        no state is entered, the function will simply return all completed
        models.
    '''
    sppCursor, sppCon = ConnectSppDB()
    comp = sppCursor.execute("""SELECT al.strUniqueID
                         FROM dbo.tblAllSpecies as al
                         WHERE al.strRangeStatus = 'Complete'""").fetchall()

    del sppCursor
    sppCon.close()

    # Since the SQL query returns a list of tuples, create a list of
    # the first item from each tuple:
    sppList = [str(item[0]) for item in comp]
    print sppList

    # If the user passed a valid state
    if state in stateDict_From_Abbr.iterkeys() or state in stateDict_To_Abbr.iterkeys():
        # Get a list of all species within that state
        stateSpp = SppInState(state)
        # And include only species found in both lists
        sppList = [i for i in sppList if i in stateSpp]

    # Sort the list alphabetically
    sppList.sort()

    return sppList


#######################################
##### Function to get a list of all species with completed ranges
def SppModelCompleted(state=False):
    '''
    ([state]) -> list

    Gets a list of all species with published models

    Argument:
    state -- An optional parameter indicating the state of interest. The two-
        letter state postal abbreviation or the full state name are valid. If
        no state is entered, the function will simply return all completed
        models.
    '''

    sppCursor, sppCon = ConnectSppDB()
    comp = sppCursor.execute("""SELECT al.strUniqueID
                         FROM dbo.tblAllSpecies as al
                         WHERE al.strModelStatus = 'Complete'""").fetchall()

    del sppCursor
    sppCon.close()

    # Since the SQL query returns a list of tuples, create a list of
    # the first item from each tuple:
    sppList =[str(item[0]) for item in comp]

    # If the user passed a valid state
    if state in stateDict_From_Abbr.iterkeys() or state in stateDict_To_Abbr.iterkeys():
        # Get the list of species in that state
        stateSpp = SppInState(state)
        # And only include species found in both lists
        sppList = [i for i in sppList if i in stateSpp]

    # Sort the list alphabetically
    sppList.sort()

    return sppList




#######################################################################
##########################################################
#############################################
## State Info

#######################################
##### Function to get a list of all species that occur in the given state
def SppInState(state, breedingOnly=False):
    '''
    !!!!!!!!!!!!!!!!!!!!!!  May not be working correctly.
    (string) -> list

    Gets a list of all the species that occur in the given state. Requires
        that the species have a published range in order to make the list.

    Note: The output omits species with only migratory range in the state as
        well as species that do not have a presence classification or 1, 2, or
        6.

    Arguments:
    state -- Can be either the state's two-character postal code or the full
        state name.
    breedingOnly -- An optional, boolean argument indicating whether you wish
        to return only species that breed within the state. The default is
        False, meaning that both breeding and non-breeding species will be
        included.

    Example:
    >>> SppInState('IN')
    [u'aETSAx', u'aFTSAx', u'aHELLa', u'aHELLx', u'aLESIx'...]
    >>> SppInState('Indiana', True)
    [u'aETSAx', u'aFTSAx', u'aHELLa', u'aHELLx', u'aLESIx'...]
    '''
    try:
        # If the user submitted a valid state abbreviation...
        if len(state) == 2 and state in stateDict_From_Abbr.iterkeys():
            # ...get the state name
            state = stateDict_From_Abbr[state]
        # If the state name is not valid...
        if state not in stateDict_To_Abbr.iterkeys():
            # ...raise an exception.
            raise Exception('The state name passed to SppInState function is not valid')

        # Create empty species list.
        sppList = []

        compRanges = SppRangeCompleted()
        sppCursor, sppCon = ConnectSppDB()

        # For each completed species...
        for sp in compRanges:
            # Get the taxon name (for use in the SQL query)
            taxa = taxaDict[sp[0][0]]

            if breedingOnly is False:
                qry = """SELECT DISTINCT rt.strUC
                        FROM dbo.tblBoundaryCrosswalk AS bc
                        INNER JOIN dbo.tblRanges_""" + taxa + """ AS rt
                        ON bc.strHUC12RNG = rt.strHUC12RNG
                        WHERE (rt.strUC=?)
                        AND (bc.strStateName=?)
                        AND (rt.intGapSeas<>2)
                        AND (rt.intGapRepro=1 OR rt.intGapRepro=3 OR rt.intGapRepro=2)
                        AND (rt.intGapPres=1 OR rt.intGapPres=2 OR rt.intGapPres=6);"""
            else:
                qry = """SELECT DISTINCT rt.strUC
                        FROM dbo.tblBoundaryCrosswalk AS bc
                        INNER JOIN dbo.tblRanges_""" + taxa + """ AS rt
                        ON bc.strHUC12RNG = rt.strHUC12RNG
                        WHERE (rt.strUC=?)
                        AND (bc.strStateName=?)
                        AND (rt.intGapSeas<>2)
                        AND (rt.intGapRepro=1 OR rt.intGapRepro=3)
                        AND (rt.intGapPres=1 OR rt.intGapPres=2 OR rt.intGapPres=6);"""

            inState = sppCursor.execute(qry, sp, state).fetchone()
            print("Wait a few minutes for it......")
            # If the species is in the state, add its code to the species list.
            if inState:
                sppList.append(inState[0])

        del sppCursor
        sppCon.close()

        return sppList

    except Exception as e:
        print e.message
        return []


#######################################
##### Function to get a list of states in which the species occurs:
def States(spCode, abbr=False, migratory=False):
    '''
    (string) -> list

    Returns a list of the states in which the species has range.

    Arguments:
    spCode -- the species' unique GAP ID
    abbr -- boolean indicating whether you wish to return postal code abbreviations
        of the states. By default, this is set to False, which means that full
        state names will be returned.

    Example:
    >>> States("aNRLFx")
    [u'Oregon', u'California', u'Washington']
    '''
    if RangeCompleted(spCode) != True:
        return False

    sppCursor, sppCon = ConnectSppDB()
    taxa = taxaDict[spCode[0]]

    qry = """SELECT DISTINCT bc.strStateName
            FROM dbo.tblBoundaryCrosswalk AS bc
            INNER JOIN dbo.tblRanges_""" + taxa + """ AS rt
            ON bc.strHUC12RNG = rt.strHUC12RNG
            WHERE (rt.strUC=?)
            AND (rt.intGapPres<>0)
            AND (rt.intGapSeas<>2);"""

    if migratory:
        qry = qry.replace('AND (rt.intGapSeas<>2)', '')

    states = sppCursor.execute(qry, spCode).fetchall()

    del sppCursor
    sppCon.close()

    if type(states) <> list:
        return []

    # Since the cursor returns a list of tuples, extract the first item
    # in each tuple and insert that into a new list.
    stList = [item[0] for item in states if item[0] in stateDict_To_Abbr]

    if abbr == True:
        stList = [stateDict_To_Abbr[item] for item in stList]

    stList.sort()

    return stList


#######################################
##### Function to get a list of states in which the species is an SGCN:
def States_SGCN(spCode, abbr = False):
    '''
    (string) -> list

    Returns a list of the states in which the species is a SGCN

    Arguments:
    spCode -- the species' unique GAP ID
    abbr -- boolean indicating whether you wish to return postal code abbreviations
        of the states (default: False)

    Example:
    >>> States_SGCN("aFFSAx")
    [u'Oregon', u'California', u'Washington']
    '''

    sppCursor, sppCon = ConnectSppDB()

    states = sppCursor.execute("""SELECT DISTINCT cs.strSGCN_state
                            FROM dbo.tblConservationStatus AS cs
                            WHERE cs.strUniqueID=?;""", spCode).fetchall()

    del sppCursor
    sppCon.close()

    if type(states) <> list:
        return False

    # Since the cursor returns a list of tuples, extract the first item
    # in each tuple and insert that into a new list.
    stList = [str(item[0].strip()) for item in states]

    if abbr == False:
        stList = [stateDict_From_Abbr[item] for item in stList]

    stList.sort()

    return stList


#######################################
##### Function to get a list of states in which species breeds:
def BreedingStates(spCode, abbr = False):
    '''
    (string) -> list

    Returns a list of the states in which the species has breeding range.

    Arguments:
    spCode -- the species' unique GAP ID
    abbr -- boolean indicating whether you wish to return postal code
        abbreviations of the states (default: False)

    Example:
    >>> BreedingStates("bGOEAx", True)
    ['OK', 'WY', 'AZ', 'OR', 'SD', 'CA', 'WA', 'ND', 'ID', 'NE', 'CO', 'TX',
    'MT', 'UT', 'NV', 'KS', 'NM']
    '''

    sppCursor, sppCon = ConnectSppDB()
    if RangeCompleted(spCode) != True:
        return []

    taxa = taxaDict[spCode[0]]

    states = sppCursor.execute("""SELECT DISTINCT bc.strStateName
                            FROM dbo.tblBoundaryCrosswalk AS bc
                            INNER JOIN dbo.tblRanges_""" + taxa + """ AS rt
                            ON bc.strHUC12RNG = rt.strHUC12RNG
                            WHERE (rt.strUC=?)
                            AND (rt.intGapPres<>0)
                            AND (rt.intGapSeas<>2)
                            AND (rt.intGapRepro=1 OR rt.intGapRepro=3);""", spCode).fetchall()

    del sppCursor
    sppCon.close()

    if type(states) <> list:
        return []

    # Since the cursor returns a list of tuples, extract the first item
    # in each tuple and insert that into a new list.
    # Also, check that the state is in the stateDict_To_Abbr...some HUCs in the
    # table have a null entry in the state field
    stList = [item[0] for item in states if item[0] in stateDict_To_Abbr]

    # If the user wishes to return state abbreviations
    if abbr == True:
        # Alter the list so that it contains abbreviations
        stList = [stateDict_To_Abbr[item] for item in stList]

    stList.sort()

    return stList




#######################################################################
##########################################################
#############################################
## Species Taxonomy/Names/Crosswalks

#######################################
##### Function to get the species' full taxonomy
def Taxonomy(spCode):
    '''
    (string) -> tuple

    Returns a tuple of 8 items: GAP species code, class, order, family,
    genus, species, subspecies, full scientific name, and common name.

    Argument:
    spCode -- the species' unique GAP ID.

    Example:
    >>> Taxonomy("abafrc")
    (u'aBAFRc', u'Amphibia', u'Anura', u'Craugastoridae', u'Craugastor',
    u'augusti', u'cactorum', u'Craugastor augusti cactorum', u'Western Barking Frog')
    '''
    try:
        sppCursor, sppCon = ConnectSppDB()
        # Query the species databsae to return a tuple of taxonomic info
        qry = sppCursor.execute("""SELECT al.strUniqueID, al.strClass, al.strOrder, al.strFamily,
                            al.strGenus, al.strSpecies, al.strSubspecies, al.strFullSciName, al.strCommonName
                            FROM dbo.tblAllSpecies AS al
                            WHERE al.strUniqueID = ?""", spCode).fetchone()

        del sppCursor
        sppCon.close()

        # If the result is not of type pyodbc.row, return None
        if type(qry) <> pyodbc.Row:
            return None

        # If the result if of type pyodbc.row, then...

        # Create an empty list
        tL = []
        # For each item in the query result
        for i in qry:
            # If it = None,
            if i is None:
                # Then append an empty string
                tL.append('')
            # If the item is not None, then append the stripped item
            else:
                tL.append(i.strip())

        # Then create a tuple of the list
        taxTup = tuple(tL)

        return taxTup

    except Exception, e:
        print 'Exception in function Taxonomy().'
        print e.message


#######################################
##### Functions to get just a single name from Taxonomy
def NameCommon(spCode):
    '''
    (string) -> string

    Returns the species' common name

    Argument:
    spCode -- the species' unique GAP ID.
    '''
    x = Taxonomy(spCode)
    if type(x) == tuple and len(x) >= 9:
        return x[8]
    else:
        return None

def NameSci(spCode):
    '''
    (string) -> string

    Returns the species' scientific name (Genus species [subspecies])

    Argument:
    spCode -- the species' unique GAP ID.
    '''
    x = Taxonomy(spCode)
    if type(x) == tuple and len(x) >= 9:
        return x[7]
    else:
        return None

def NameGenus(spCode):
    '''
    (string) -> string

    Returns the species' genus

    Argument:
    spCode -- the species' unique GAP ID.
    '''
    x = Taxonomy(spCode)
    if type(x) == tuple and len(x) >= 9:
        return x[4]
    else:
        return None

def NameClass(spCode):
    '''
    (string) -> string

    Returns the species' class

    Argument:
    spCode -- the species' unique GAP ID.
    '''
    x = Taxonomy(spCode)
    if type(x) == tuple and len(x) >= 9:
        return x[1]
    else:
        return None

def NameOrder(spCode):
    '''
    (string) -> string

    Returns the species' order

    Argument:
    spCode -- the species' unique GAP ID.
    '''
    x = Taxonomy(spCode)
    if type(x) == tuple and len(x) >= 9:
        return x[2]
    else:
        return None

def NameFamily(spCode):
    '''
    (string) -> string

    Returns the species' family

    Argument:
    spCode -- the species' unique GAP ID.
    '''
    x = Taxonomy(spCode)
    if type(x) == tuple and len(x) >= 9:
        return x[3]
    else:
        return None

def NameSpecies(spCode):
    '''
    (string) -> string

    Returns the species' scientific species name

    Argument:
    spCode -- the species' unique GAP ID.
    '''
    x = Taxonomy(spCode)
    if type(x) == tuple and len(x) >= 9:
        return x[5]
    else:
        return None

def NameSubspecies(spCode):
    '''
    (string) -> string

    Returns the subspecies name, if applicable; otherwise, returns
    an empty string

    Argument:
    spCode -- the species' unique GAP ID.
    '''
    x = Taxonomy(spCode)
    if type(x) == tuple and len(x) >= 9:
        return x[6]
    else:
        return None


#######################################
##### Function to get the species' download file name
def NameDownload(spCode):
    '''
    (string) -> string

    Gets the download filename

    Argument:
    spCode -- the species' unique GAP ID

    Example:
    >>> NameDownload('mNAROx')
    Lon_can_NAROx
    '''

    sppCursor, sppCon = ConnectSppDB()
    dlfn = sppCursor.execute("""SELECT al.strDownloadFileName
                    FROM dbo.tblAllSpecies AS al
                    WHERE al.strUniqueID = ?""", spCode).fetchone()

    del sppCursor
    sppCon.close()

    dlfn = dlfn[0]

    return dlfn


#######################################
##### Function to get the codes to crosswalk the GAP code to ELCode, etc.
def Crosswalk(spCode):
    '''
    (string) -> tuple

    Returns a tuple of 4 items: GAP species code, ELCode, ITIS TSN, and
        Global_SEQ_ID

    Argument:
    spCode -- the species' unique GAP ID

    Example:
    >>> Crosswalk('mNAROx')
    (u'mNAROx', u'AMAJF10010', u'180549', 102243)
    '''

    try:
        whrCursor, whrCon = ConnectWHR()
        qry = whrCursor.execute("""SELECT t.strUC, t.strSort, t.strITIScode, t.intELEMENT_GLOBAL_SEQ_UID
                                FROM dbo.tblTaxa as t
                                WHERE t.strUC = ?""", spCode).fetchone()

        del whrCursor
        whrCon.close()

        xWalkTemp = tuple(qry)

        # Create an empty new list
        xWalk = []
        # For each item resulting from the query
        for item in xWalkTemp:
            # If the item is of type None or is False
            if item == 'None' or item == None:
                # Add an empty string to the list
                xWalk.append('')
            # Otherwise, add a string of the item
            else:
                xWalk.append(str(item))

        # Convert the list to a tuple and return it
        return tuple(xWalk)

    # An exception in this function would indicate that the species is not in
    # the taxa table. Therefore, just return the submitted species code with
    # the remaining fields represented by empty strings.
    except:
        return (spCode,'','','')


##### Function to return the combined info for a species, including taxonomy,
##### crosswalk, and range/model completion status.
def SpInfoCombined(spCode, completionStatus = True):
    '''
    (string, [boolean]) -> tuple

    Returns the full info for the the species, including taxonomy, crosswalk,
        and range/model completion status.

    Refer to SpInfoCombinedHeaders() to get a list of the appropriate field
        headings

    Argument:
    spCode -- the species' unique GAP ID
    completionStatus -- an optional, boolean argument, indicating whether to
        include the range/model completion status in the output. By default, it
        is set to true, meaning that the status fields will be included.

    Example:
    >>> SpInfoCombined('abotox')
    ('aBOTOx', 'Amphibia', 'Anura', 'Bufonidae', 'Anaxyrus', 'boreas', '',
    'Anaxyrus boreas', 'Western Toad', 'AAABB01030', '773513', '102714', 'True', 'True')
    '''
    try:
        tax = Taxonomy(spCode)

        xWalk = Crosswalk(spCode)[1:]

        comb = list(tax + xWalk)

        if completionStatus:
            rComp = str(RangeCompleted(spCode))
            mComp = str(ModelCompleted(spCode))

            comb.append(rComp)
            comb.append(mComp)

        comb = tuple([str(i) for i in comb])

        return comb

    except Exception as e:
        return False


def SpInfoCombinedHeaders(completionStatus = True):
    '''
    Returns a list of the fields names from the SpInfoCombined() function,
        in the proper order.
    '''
    heads = ['Species_GAP_Code', 'Class', 'Order', 'Family', 'Genus', \
             'Species', 'Subspecies', 'Full_Scientific_Name', 'Common_Name', \
             'ElCode', 'ITIS_TSN', 'Global_Seq_ID']

    if completionStatus:
        heads.extend(['GAP_Range_Completed', 'GAP_Model_Completed'])

    return heads



#######################################################################
##########################################################
#############################################
## Species Info - misc.


#######################################
##### Function to get a list of models for the species
def ModelCodes(code, publishedOnly=False, conusOnly=False, migratory=True):
    '''
    (string, [boolean], [boolean], [boolean]) -> list

    Gets a list of the species' regional model codes from tblModelStatus in WHRDb.

    Arguments:
    code -- the species' unique GAP ID or the beginning of the GAP ID
    publishedOnly -- Optional boolean parameter to include only published models.
        By default, it is set as False, which returns all models.
    conusOnly -- Optional boolean parameter to include only models within CONUS.
        By default, it is set as False, which returns all models.
    migratory -- Optional boolean parameter to include migratory models.
        By default, it is set as True, which includes migratory models.

    Examples:
    >>> ModelCodes("aHOTOx")
    [u'aHOTOx-y0', u'aHOTOx-y5', u'aHOTOx-y6']
    >>> ModelCodes("aHOTOx", True)
    [u'aHOTOx-y0', u'aHOTOx-y5', u'aHOTOx-y6']
    >>> ModelCodes("aHOTOx", True, True)
    [u'aHOTOx-y5', u'aHOTOx-y6']

    '''
    sppCursor, sppCon = ConnectWHR()
    qry = """SELECT strSpeciesModelCode
            FROM dbo.tblModelStatus
            WHERE strSpeciesModelCode LIKE '{0}%'""".format(code)

    if publishedOnly:
        qry = qry + '\nAND strModelStatusAll = \'Publishing Completed\''

    qryResult = sppCursor.execute(qry).fetchall()

    del sppCursor
    sppCon.close()

    spCodes = [item[0] for item in qryResult]

    # Get list of migratory models
    migs = [x for x in spCodes if x[-2] == "m"]

    # Filter out migratory models
    spCodes = [x for x in spCodes if x[-2] != "m"]

    # If the user wishes to view only models for CONUS
    if conusOnly:
        # Copy the spCodes list
        codes = spCodes
        spCodes = [x for x in codes if x[-1] in [str(y) for y in range(1,7)]]
        '''# !!!!! This old code leaves in migratory but not winter models ->
        # Initialize an empty list
        spCodes = list()
        # For each number from 1-6 (i.e., CONUS region codes)
        for i in range(1,7):
            # For each model code
            for code in codes:
                # If the conus region code is in the model name
                if str(i) in code:
                    # Add the code to the list
                    spCodes.append(code)
                    break'''

     # If the user wishes to include migratory models.
    if migratory:
        spCodes=spCodes + migs

    return spCodes


def SpInCONUS(code, publishedOnly=False):
    '''
    !!! This may not give the desired result!!!

    (sp, [bool]) -> bool

    Determine whether the species has a model in CONUS. Results are derived from
    entries in tblModelStatus within the WHRDb.

    Arguments:
    code - The species' 6-character GAP ID code
    publishedOnly - An optional, boolean parameter indicating whether you wish
      to test whether the species' CONUS models have already been published. By
      default, it is set to False, meaning that all models, regardless of
      publishing status, will be considered.
    '''
    models = ModelCodes(code, publishedOnly, True)
    modelsLower = [x for x in models if x[-1] != "A" and x[-1] != "T" and x[-1] != "H"]
    if len(modelsLower) > 0:
        return True
    else:
        return False


#######################################
##### Function to get a list of related taxa; for example, if
##### you'd like to know what subspecies exist for a species
def Related(code):
    '''
    (string) -> list

    Gets a list of species/subspecies that share the code root (i.e.
    the first 5 characters of the code). If your argument exceeds five
    characters, the function will ignore all but the first five. If you submit
    an argument with fewer than five characters, the function will return all
    GAP codes that begin with whatever argument you submitted.

    Argument:
    code -- the species' unique GAP ID or the beginning of the GAP ID

    Examples:
    >>> Related("aBAFR")
    [u'aBAFRc', u'aBAFRl', u'aBAFRx']
    >>> Related("aBAFRc")
    [u'aBAFRc', u'aBAFRl', u'aBAFRx']
    >>> Related("aBA")
    [u'aBAFRc', u'aBAFRl', u'aBAFRx', u'aBATRx']
    '''
    code = code[0:5]
    sppCursor, sppCon = ConnectSppDB()
    qryResult = sppCursor.execute("""SELECT strUniqueID
                                FROM dbo.tblAllSpecies
                                WHERE strUniqueID LIKE '""" + code + """%'
                                """).fetchall()

    del sppCursor
    sppCon.close()

    spCodes =[item[0] for item in qryResult]

    return spCodes


#######################################
##### Function to return the species' ESA status
def ESA_Status(spCode):
    '''
    (string) -> string

    Returns the species' ESA status

    Argument:
    spCode -- the species' unique GAP ID

    Example:
    >>> ESA_Status('mNAROx')

    >>> ESA_Status('aABSAx')
    Candidate
    '''

    sppCursor, sppCon = ConnectSppDB()
    stat = sppCursor.execute("""SELECT cs.strESATandEStatus
                    FROM dbo.tblConservationStatus AS cs
                    WHERE cs.strUniqueID = ?""", spCode).fetchone()

    del sppCursor
    sppCon.close()

    if type(stat) <> pyodbc.Row:
        return False

    stat = stat[0]
    if type(stat) is unicode and len(stat) > 0:
        return stat.split(':')[1].strip()
    else:
        return False



def ConservationConcern(spCode):
    '''
    (string) -> string/boolean

    Returns the species' conservation concern description, if it exists;
        otherwise, returns False

    Argument:
    spCode -- the species' unique GAP ID

    Example:
    >>> ConservationConcern('mNAROx')
    False
    >>> ConservationConcern('bBAEAx')
    'Long-term planning and responsibility, high percent of global population in single biome'
    '''
    whrCursor, whrCon = ConnectWHR()
    concernStatus = whrCursor.execute("""SELECT cc.memConservationConcern
                    FROM dbo.tblConservationConcern AS cc
                    WHERE cc.strUC = ?""", spCode).fetchone()

    del whrCursor
    whrCon.close()

    if type(concernStatus) <> pyodbc.Row:
        return False

    stat = concernStatus[0]
    if type(stat) is unicode and len(stat) > 0:
        return stat.strip()
    else:
        return False



#######################################
##### Function to return the processing date for the species' range or model
def ProcessDate(spCode, x = 'Model', y = 'Edited', seconds=False):
    '''
    (string, string, string, [boolean]) -> datetime object / float

    Gets the date that the species' range or model was created
    or last edited. Returns the date as a date data type.

    Arguments:
    spCode -- the species' unique GAP ID
    x -- indicates whether you wish to return the process date for the species'
        'model' or its 'range'; the default is 'model';
    y -- indicates whether you wish to return the date that the data was
        'edited' or 'created'; the default is 'edited';
    seconds -- an optional parameter indicating whether you wish the date to
        be returned as seconds since the epoch. By default, it is set to false.

    Example:
    >>> print ProcessDate("bBAEAx")
    2013-04-01 00:00:00
    '''
    import datetime, time

    x = x.title()
    y = y.title()

    field = 'dtm' + x + y
    qry = """SELECT """ + field + """
            FROM dbo.tblUpdateDateTime
            WHERE strUniqueID = ?"""

    sppCursor, sppCon = ConnectSppDB()
    result = sppCursor.execute(qry, spCode).fetchone()

    if result:
        d = result[0]
    else:
        return None

    if y == 'Edited':
        editDate = d
        field = 'dtm' + x + 'Created'
        qry = """SELECT """ + field + """
            FROM dbo.tblUpdateDateTime
            WHERE strUniqueID = ?"""
        createDate = sppCursor.execute(qry, spCode).fetchone()[0]

        if editDate is None and createDate is not None:
            d = createDate

    del sppCursor
    sppCon.close()

    if seconds and d is not None:
        d = time.mktime(d.timetuple())

    return d

#######################################
##### Function to return the name of a person who worked on a species.
def Who(spCode, action="reviewed"):
    '''
    (string, action) -> string
    
    Gets the name of the staff member who completed an action of interest.
    
    Notes:
    This function queries the WHRdb tblModelStatus table, which has rows for each region-
        season model, not strUC.  It grabs (I believe) the first record of the query
        result.  It would ideally query the species database, but the table there is not 
        up to date.
    
    Arguments:
    spCode -- the species' unique GAP ID
    action -- The action of interest.  Choose from "edited", "mosaiced", "reviewed", 
        "published".
    
    Example:
    >>> print WhoReviewed("bBAEAx", action="reviewed")
    "Jeff Lonneker"
    '''
    print("See Notes!!!")
    
    # Dictionaries
    actions = {"reviewed": "whoInternalReviewComplete", "edited": "whoEditingComplete",
              "mosaiced": "whoMosaicingComplete", "published": "whoPublishingComplete"}
    staff = {"mjr": "Matthew Rubino", "nmt": "Nathan Tarr", "jjl": "Jeff Lonneker",
                 "tl": "Thomas Laxon", "rta": "Robert Adair", "mjb": "Matthew Rubino",
                 "mbr": "Matthew Rubino"}
    # Build a query             
    field = actions[action]
    qry = """SELECT """ + field + """
            FROM dbo.tblModelStatus
            WHERE strUC = ?"""
    # Connect to database
    sppCursor, sppCon = ConnectWHR()
    result = sppCursor.execute(qry, spCode).fetchone()
    
    # Format result of query
    if result and result[0] != None:
        if result[0].lower() in staff.keys():
            name = staff[result[0].lower()]
        else:
            name="Unknown"
    else:
        name = "Unknown"
    
    # Delete cursor
    del sppCursor
    sppCon.close()
    
    return name

#######################################
##### Function to return an input string with the capitalization
##### pattern of GAP species codes
def GapCase(spCode):
    '''
    (string) -> string

    Returns an input string in the Gap Code capitalization

    Argument:
    spCode -- the species' unique GAP ID

    Example:
    >>> GapCase('bbaeax')
    bBAEAx
    >>> GapCase('BbAEax')
    bBAEAx
    >>> GapCase('BBAEAX')
    bBAEAx
    '''

    spCode = spCode[0].lower() + spCode[1:5].upper() + spCode[5].lower()

    return spCode




#######################################################################
##########################################################
#############################################
## Map Units

#######################################
##### Get the map unit's ecological system name
def MUName(muCode):
    '''
    (int) -> str

    Returns the name of the ecological system that matches the passed map unit
        code.

    Argument:
    muCode -- The map unit's 4-digit code.

    Example:
    >>> MUName(2812)
    'Dry noncalcareous woodland'
    '''
    # Check if the user passed an integer
    try:
        # If the user passed a code, continue
        i = int(muCode)
        pass
    except:
        # If the passed value cannot be cast as an integer, then it must be a
        # map unit name already, so just return it
        return muCode

    try:
        muCode = int(muCode)

        # Get the WHRdb cursor and connection
        whrCursor, whrCon = ConnectWHR()

        # Query the database
        res = whrCursor.execute("""SELECT t.strLSGapName
                                FROM dbo.tblMapUnitDesc as t
                                WHERE t.intLSGapMapCode = ?""", muCode).fetchone()

        # Process the query results, to get the first field from the tuple
        # and to remove trailing and leading spaces.
        mu = str(res[0].strip())

        # Del the WHRdb cursor and close the connection
        del whrCursor
        whrCon.close()

        return mu

    except:
        pass


def MUCode(muName):
    '''
    (str) -> int

    Returns the map unit code that matches the passed ecological system name.

    Argument:
    muName -- The map unit's code, as found in tblMapUnitDesc.strLSGapName.

    Example:
    >>> MUCode('Dry noncalcareous woodland')
    2812
    '''
    # Check whether the passed argument can be cast as an integer
    try:
        # If it can be cast as an integer, just return the integer.
        i = int(muName)
        return i
    # If the casting to integer fails, it is assumed that the argument is a
    # valid ecological system name, so go on with the rest of the function.
    except:
        pass

    try:
        # Get the WHRdb cursor and connection
        whrCursor, whrCon = ConnectWHR()

        # Query the database
        res = whrCursor.execute("""SELECT t.intLSGapMapCode
                                FROM dbo.tblMapUnitDesc as t
                                WHERE t.strLSGapName = ?""", muName).fetchone()

        # Process the query results, to get the first field from the tuple
        # and to remove trailing and leading spaces.
        mu = int(res[0])

        # Del the WHRdb cursor and close the connection
        del whrCursor
        whrCon.close()

        return mu

    except:
        pass


#######################################
##### Translate a list of map unit codes to a list of the ecological system
##### names
def MUCodesToNames(muCodeList):
    '''
    (list) -> list

    Translates a list of map unit codes into a list of ecological system names.
        The passed codes can be either strings or integers.

    Argument:
    muCodeList -- A list of 4-digit map unit codes

    Example:
    >>> [2503, 2505, 2512]
    ['Bog Vegetation', 'Closed Hala Forest', 'Closed Kukui Forest']
    '''
    # Initialize an empty list to store the map units
    muNameList = []

    # For each MU code in the list
    for mu in muCodeList:
        # Get its name
        name = MUName(mu)
        # If its name is not already in the list, add it
        if name:
            muNameList.append(name)

    return muNameList


#######################################
##### Translate a list of map unit codes to a list of the ecological system
##### names
def MUNamesToCodes(muNameList):
    '''
    (list) -> list

    Translates a list of map unit names into a list of ecological system codes.

    Argument:
    muCodeList -- A list of map unit names

    Example:
    >>> ['Bog Vegetation', 'Closed Hala Forest', 'Closed Kukui Forest']
    [2503, 2505, 2512]
    '''
    # Initialize an empty list to store the map units
    muCodeList = []

    # For each MU name in the list
    for mu in muNameList:
        # Get its code
        code = MUCode(mu)
        # If its code is not already in the list, add it
        if code:
            muCodeList.append(code)

    # Ensure that all included codes are legitimate map unit codes
    allMUs = AllMUs(False)
    muCodeList = [i for i in muCodeList if i in allMUs]

    return muCodeList


## Determine whether the map unit occurs in the region
def MuInRegion(mu, region):
    '''
    (string/int, string/int) -> boolean

    Returns a boolean indicating whether the map unit occurs within the region.

    Arguments:
    mu -- The GAP map unit code (as either an int or a string) or the map unit
        name.

    region -- The GAP region code (as either an int or a string) of interest.
        The function will also accept the region's two character abbreviation or
        its full name, as long as it matches those in the region dictionaries
        found within the dictionaries module.

    Examples:
    >>> gp.gapdb.MuInRegion("1402", "4")
    True
    >>> gp.gapdb.MuInRegion(1402, "4")
    True
    >>> gp.gapdb.MuInRegion(1402, "sw")
    True
    >>> gp.gapdb.MuInRegion(1402, "SOUTHWEST")
    True
    >>> gp.gapdb.MuInRegion('Atlantic Coastal Plain Northern Sandy Beach', 1)
    False
    '''
    # If the function parameters are stringified integers, cast them as integers.
    try:
        mu = int(mu)
    except:
        pass
    try:
        region = int(region)
    except:
        pass

    # Ensure that the passed model region is valid
    # If the region is not an integer
    if not type(region) is int:
        # If it is two characters long
        if len(region) == 2:
            # Import the appropriate dictionary
            from dictionaries import regionsDict_Abbr_To_Num as regDict
            # And convert the region string to uppercase
            region = region.upper()
        # If the length of the string is not 2
        else:
            # Import the appropriate dictionary
            from dictionaries import regionsDict_Name_To_Num as regDict
            # Conver the region string to title case
            region = region.title()
        # If the region string is one of the dictionary keys
        if region in regDict.iterkeys():
            # Set the region to the corresponding value
            region = regDict[region]
        # If the region is not in the dictionary, the user passed some wacky
        # parameter, so return False
        else:
            return False

    # If the region code is greater than 6...
    if not region < 7:
        # Return False
        return False
    # Cast the region code as a string before constructing the SQL query
    else:
        region = str(region)

    # Get WHRdb cursor and connection
    whrCursor, whrCon = ConnectWHR()

    # If the map unit code has been passed
    if type(mu) is int:
        # Query based on the map unit code
        qry = """SELECT t.ysnRegion%s
            FROM dbo.tblMapUnitDesc AS t
            WHERE t.intLSGapMapCode=?""" % region
    # If the passed map unit is a string
    else:
        # Query based on the map unit name
        qry = """SELECT t.ysnRegion%s
            FROM dbo.tblMapUnitDesc AS t
            WHERE t.strLSGapName=?""" % region

    # Execute the query
    res = whrCursor.execute(qry, mu).fetchone()

    # Delete the WHRdb cursor and close the connection
    del whrCursor
    whrCon.close()

    return res[0]


## Get a list of the regions in which the map unit occurs
def MuRegions(mu):
    '''
    (string/int) -> list

    Returns a list of the GAP modeling regions (by numeric code) in which the
        map unit occurs.

    Argument:
    mu -- The GAP map unit code (as either an int or string) or the map unit
        name.

    Examples:
    >>> gp.gapdb.MuRegions('Open Water (Aquaculture)')
    ['6']
    >>> gp.gapdb.MuRegions(2103)
    ['1', '3', '4', '5', '6']
    >>> gp.gapdb.MuRegions("2103")
    ['1', '3', '4', '5', '6']
    '''
    # Initialize an empty list to store the regions
    muList = []

    try:
        # For numbers from 1 to 6
        for i in range(1,7):
            # If the map unit is in the region
            if MuInRegion(mu, i):
                # add it to the list
                muList.append(str(i))
            else:
                pass
    except:
        pass

    return muList


## Get a list of all map units
def AllMUs(name=True, conus=True):
    '''
    ([boolean]) -> list

    Returns a list of all map units in the database.

    Arguments:
    name -- Optional boolean parameter indicating whether you wish to return
        a list of the ecological system names or of the map unit codes. By
        default, it is set to True, which means that the list will contain
        ecological system names. False will return map unit codes as integers.
    conus -- Optional boolean parameter indicating whether you wish to return
        only the map units that occur within CONUS or all map units.
    '''
    # Connect to the database
    cur, conn = ConnectWHR()

    # Define the field name depending on whether the user wishes to return
    # ecological system names or map unit codes:
    if name:
        field = 'strLSGapName'
    else:
        field = 'intLSGapMapCode'

    # The SQL query with the field parameter
    qry = """SELECT t.%s
          FROM dbo.tblMapUnitDesc as t""" % field

    # Execute the query
    res = cur.execute(qry).fetchall()

    # Delete the cursor and close the connection
    del cur
    conn.close()

    # If the user wants to return ES names,
    if name:
        # Create a list of ecological system names from the stripped first item
        # in each row object
        mus = [i[0].strip() for i in res]
    # Otherwise...
    else:
        # Create a list of map unit codes from the first item in each row object
        mus = [i[0] for i in res]

    # Sort the list
    mus.sort()

    # If the user opted to return only MUs within CONUS
    if conus is True:
        # Send the list to the Conus filtering function
        mus = __ConusMUs(mus)

    # Return the list of map units
    return mus


def __ConusMUs(mus):
    # Initialize an empty list to store map units to omit
    musRemove = []
    # For each map unit
    for mu in mus:
        # Get a list of its regions
        regions = MuRegions(mu)
        # If no regions are in the list...
        if len(regions) < 1:
            # Add the map unit to the list of MUs to be removed
            musRemove.append(mu)
    # For each map unit in the list of those to be removed
    for mu in musRemove:
        # Remove it from the original map units list
        mus.remove(mu)

    return mus


## Get a list of map units unique to the region of interest
def UniqueMUs(inRegion, absentRegions=range(1,7)):
    '''
    (string/integer, [list]) -> list

    Returns a list of ecological systems that occur within the region of
        interest but that do not occur in any of the indicated regions
        (i.e., those indicated in absentRegions).

    Arguments:
    inRegion -- Either a string or integer, indicating the numeric GAP modeling
        region code of the region of interest.
    absentRegions -- A list containing either strings or integers, indicating
        the numeric GAP modeling region code(s) of any region(s) from which
        the map unit must be absent to be included in the output. By default,
        the list includes all regions (though the inRegion is removed from the
        list), meaning that only map units that are unique to the inRegion will
        be returned.
    '''
    # If the inRegion is in the absent regions list...if the user takes the
    # default absentRegions, this could occur:
    if inRegion in absentRegions:
        # remove it from the absent regions list
        absentRegions.remove(int(inRegion))

    # Get a list of all possible map units
    amus = AllMUs()
    # Initialize an empty list to store map units
    mus = []

    # For each map unit...
    for amu in amus:
        # if the map unit occurs in the inRegion
        if MuInRegion(amu, inRegion):
            # add it to the list
            mus.append(amu)

    # Initialize an empty list to store the map units to be omitted
    musRemove = []

    # For each map unit that occurs within the inRegion
    for mu in mus:
        # Get a list of regions that the map unit occurs in
        muRegs = MuRegions(mu)
        # For each region in the absentRegions list...
        for absReg in absentRegions:
            # If the region is in the list of regions for the map unit...
            if str(absReg) in muRegs:
                # Add the region to the list of map units to be omitted
                musRemove.append(mu)
                # and skip to the next map unit
                break

    # Create a list that contains map units unique to the region
    outMus = list(set(mus) - set(musRemove))

    # Return the list
    return outMus



################################################################
####################################################
################ Search for map units with a keyword in name or description.
def MUsWithKeyword(keyword):
    '''
    (str) -> list

    Returns a list of map units (as integers) that contain the keyword in their
    name or description
    '''
    # Get a cursor and connection to WHR database
    whrCursor, whrCon = ConnectWHR()
    # Execute the query to select model codes that match the passed species code
    MUs = whrCursor.execute("""SELECT intLSGapMapCode
                            FROM dbo.tblMapUnitDesc
                            WHERE memDescription Like ?
                            OR strLSGapName LIKE ?
                            """, '%' + keyword + '%', '%' + keyword + '%').fetchall()

    # Delete the cursor
    del whrCursor
    # Close the database connection
    whrCon.close()

    # Create a list of all the matching mus
    m = [int(item[0]) for item in MUs if MuInRegion(int(item[0]), 1) == True or
         MuInRegion(int(item[0]), 2) == True or MuInRegion(int(item[0]), 3) == True or
         MuInRegion(int(item[0]), 4) == True or MuInRegion(int(item[0]), 5) == True or
         MuInRegion(int(item[0]), 6) == True]

    # Return the list of matching model codes
    return m


def __main():
    pass

if __name__ == "__main__":
    __main()



#########################################################################
########################################################
#################################
## Add a new species to the databases
# Class to store the species' taxonomic info, codes, etc.

class __Species():
    def __init__(self, row, curSp, curWHR, connSp, connWHR):
        self.gapID, self.nameCommon, self.nameClass, self.nameOrder, self.nameFamily, \
            self.nameGenus, self.nameSpecies, self.nameSubSpecies, self.elCode, \
            self.DownloadFileName, self.Sensitive = row

        self.gapID = gap.gapdb.GapCase(self.gapID)
        self.nameGenus = self.nameGenus.title()
        self.nameClass = self.nameClass.title()
        self.nameOrder = self.nameOrder.title()
        self.nameFamily = self.nameFamily.title()
        self.nameSpecies = self.nameSpecies.lower()
        self.nameSubSpecies = self.nameSubSpecies.lower()

        self.nameBinom = '{0} {1}'.format(self.nameGenus, self.nameSpecies)
        self.nameSci = '{0} {1}'.format(self.nameBinom, self.nameSubSpecies)

        self.modelCode = '{0}-y0'.format(self.gapID)
        self.fourCode = self.gapID[1:-1]

        self.ServiceCode = '{0}_{1}'.format(gap.match_and_filter.LegalChars(self.nameCommon), self.gapID)

        self.curSp = curSp
        self.curWHR = curWHR
        self.connSp = connSp
        self.connWHR = connWHR


# Public function for adding a species to the GAP databases
def AddSpecies(inTable, userName, pwd):
    '''
    (str, str, str) ->

    Adds a species to the GAP databases.

    Arguments:
    inTable -- The path of the table containing the relevant species information.
        a template table can be found at: ...\GAPage\data\SppToAdd_template\SppToAdd.csv.
        Please copy the table and fill in the appropriate fields as in the example
        species.
    userName -- A write-permission-granted user name for the Species Database
        and for the WHRDB.
    pwd -- The password matching the given user name.
    '''
    # Connect to the databases
    curSp, connSp = ConnectSppDB(userName, pwd)
    curWHR, connWHR = ConnectWHR(userName, pwd)

    # Read the species' info from the passed table
    rows = tables.ListFromTable(inTable)[1:]

    # Verify that none of the passed species codes are already in use
    __CheckSpp(inTable)

    # For each species from the table, process the species
    for row in rows:
        print 'Input data:', row
        # Create a Species object
        sp = __Species(row, curSp, curWHR, connSp, connWHR)
        try:
            # Send the species through the queries, getting back a list of exceptions
            exes = __ProcessSp(sp)
            # Parse the exceptions and determine whether the user wishes to proceed
            commit = __FilterExceptions(exes, sp)
            # Apply the updates to the databases
            if commit:
                sp.connSp.commit()
                sp.connWHR.commit()
                print 'Updates have been committed to the databases.'
            # Undo the updates to the databases
            else:
                sp.connSp.rollback()
                sp.connWHR.rollback()
        except Exception as e:
            print 'Exception. Rolling back changes.'
            sp.connSp.rollback()
            sp.connWHR.rollback()
            print e

# Verify that the species codes are not already in use
def __CheckSpp(table):
    sppToAdd = tables.ListValues(table, 0)
    sppExisting = ListAllSpecies()
    for sp in sppToAdd[1:]:
        if sp in sppExisting:
            done = raw_input('\nThe species code {0} already exists in the database.\nAddress this issue and then try again.\n\nPress any key to close.'.format(sp))
            sys.exit()


# Parse the exceptions, taking note of all except the duplicate primary keys
def __FilterExceptions(exes, sp):
    exesDupe = list()
    exesOther = list()
    if len(exes) > 0:
        for ex in exes:
            if 'duplicate' in ex[-1]:
                exesDupe.append(ex)
            else:
                exesOther.append(ex)
    # Let the user see the duplicate primary key exceptions
    if len(exesDupe) > 0:
        print '\n\nNote that the {0} already occurs in one or more tables in the database. This may not be a problem; if you are attempting to un-drop a species, this is expected. See the following messages:'.format(sp.gapID)
        for ex in exesDupe:
            print '\n', ex

    # Warn the user about all other exceptions, giving them the option to rollback
    # changes
    if len(exesOther) > 0:
        print '\n\nThe following error(s) occurred while attempting to update the databases:'
        for ex in exesOther:
            print '\n', ex
        while True:
            commit = raw_input("\nGiven the above errors, please indicate whether you wish to save the changes to the database.\nEnter 'Y' to try saving the changes; enter 'N' to rollback the database updates:\n").lower()
            if commit == 'y':
                return True
            if commit == 'n':
                return False
    return True



# Base function for processing a species
def __ProcessSp(sp):
    exes = list()

    # Run the species through each of the queries
    for func in [__01_sp_tblAllSpecies, \
                 __02_sp_tblModelingInfo, \
                 __03_sp_tblModelStatus, \
                 __04_sp_tblUpdateDateTime, \
                 __05_whr_tblAllSpecies, \
                 __06_whr_tblModelStatus, \
                 __07_whr_tblModelingAncillary, \
                 __08_whr_tblSppMapUnitPres, \
                 __09_whr_tblHabNotes, \
                 __10_whr_tblModelText, \
                 __11_whr_tblTaxa, \
                 __12_whr_tblConservationConcern, \
                 __13_whr_tblSpeciesNotes]:
        try:
            func(sp)
        except Exception as e:
            #print e
            exes.append(e)

    return exes


# Create the query string
def __StartQuery(cur, count, tableName):
    colNames = list()
    for row in cur.columns(table=tableName):
        colNames.append(row.column_name)

    colNames = ', '.join(colNames[:count])

    qry = '''INSERT INTO {0} ({1})'''.format(tableName, colNames)
    return qry


# Execute the query
def __Insert(cur, tup, qry):
    if len(tup) == 1:
        qry = "{0} VALUES ('{1}')".format(qry, tup[0])
    else:
        qry = qry + ' VALUES {0}'.format(tup)

    cur.execute(qry)


# Query for the Species database's AllSpecies table
def __01_sp_tblAllSpecies(sp):
    tup = (sp.gapID, sp.nameBinom, sp.nameCommon, sp.gapID[0], sp.nameClass, \
           sp.nameOrder, sp.nameFamily, sp.nameGenus, sp.nameSpecies, \
           sp.nameSubSpecies, sp.nameSci, '', '', '', '', 'Not Started', \
           'Not Started', sp.DownloadFileName, sp.Sensitive, sp.ServiceCode)

    qry = '''INSERT INTO tblAllSpecies'''

    __Insert(sp.curSp, tup, qry)

def __02_sp_tblModelingInfo(sp):
    tup = (sp.gapID, sp.modelCode, sp.gapID[0].upper(), \
           sp.fourCode, sp.gapID[-1].upper(), 'Y', 0, \
           sp.modelCode[:-1], 1, 1, sp.nameBinom, sp.nameSubSpecies, \
           sp.nameCommon, sp.elCode)

    qry = __StartQuery(sp.curSp, len(tup), 'tblModelingInfo')

    __Insert(sp.curSp, tup, qry)

def __03_sp_tblModelStatus(sp):
    tup = [sp.modelCode]
    qry = '''INSERT INTO tblModelStatus (strSpeciesModelCode)'''
    __Insert(sp.curSp, tup, qry)

def __04_sp_tblUpdateDateTime(sp):
    tup = [sp.gapID]

    qry = '''INSERT INTO tblUpdateDateTime (strUniqueID)'''

    __Insert(sp.curSp, tup, qry)

def __05_whr_tblAllSpecies(sp):
    tup = (sp.modelCode, 'Y', 'Year-round', 0, sp.modelCode[:-1], sp.gapID, '', \
           1, sp.nameBinom, sp.nameSubSpecies, sp.nameCommon, 'US', \
           sp.gapID[0], sp.elCode, sp.fourCode)

    qry = __StartQuery(sp.curWHR, len(tup), 'tblAllSpecies')

    __Insert(sp.curWHR, tup, qry)

def __06_whr_tblModelStatus(sp):
    tup = (sp.modelCode, sp.gapID)
    qry = '''INSERT INTO tblModelStatus (strSpeciesModelCode, strUC)'''
    __Insert(sp.curWHR, tup, qry)

def __07_whr_tblModelingAncillary(sp):
    tup = [sp.modelCode]
    qry = '''INSERT INTO tblModelingAncillary (strSpeciesModelCode)'''
    __Insert(sp.curWHR, tup, qry)

def __08_whr_tblSppMapUnitPres(sp):
    mus = AllMUs(False, True)

    rows = list()
    for mu in mus:
        rows.append([sp.modelCode, mu, False, False])

    qry = '''INSERT INTO tblSppMapUnitPres
             VALUES (?, ?, ?, ?)'''

    sp.curWHR.executemany(qry, rows)

def __09_whr_tblHabNotes(sp):
    tup = [sp.modelCode]
    qry = '''INSERT INTO tblHabNotes (strSpeciesModelCode)'''
    __Insert(sp.curWHR, tup, qry)

def __10_whr_tblModelText(sp):
    tup = [sp.modelCode]
    qry = '''INSERT INTO tblModelText (strSpeciesModelCode)'''
    __Insert(sp.curWHR, tup, qry)

def __11_whr_tblTaxa(sp):
    tup = (sp.gapID, sp.nameBinom, sp.nameSubSpecies, sp.gapID[-1], sp.nameCommon, \
           sp.elCode, sp.gapID[0])
    qry = __StartQuery(sp.curWHR, len(tup), 'tblTaxa')
    __Insert(sp.curWHR, tup, qry)

def __12_whr_tblConservationConcern(sp):
    tup = [sp.gapID]
    qry = '''INSERT INTO tblConservationConcern (strUC)'''
    __Insert(sp.curWHR, tup, qry)

def __13_whr_tblSpeciesNotes(sp):
    tup = [sp.gapID]
    qry = '''INSERT INTO tblSpeciesNotes (strUC)'''
    __Insert(sp.curWHR, tup, qry)



if __name__ == '__main__':
    pass
