'''
Functions related to GAP Land Cover tasks and data.
NOTE: This content was originally in gapdb, and old versions still exist there.
They will need to be deleted and deprecated.
'''

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