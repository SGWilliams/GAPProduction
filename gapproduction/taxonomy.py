'''
Functions related to querying and editing the GAP species concepts/taxonomy.
'''

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
    import gapdb, pyodbc
    try:
        sppCursor, sppCon = gapdb.ConnectSppDB()
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
    import gapdb
    try:
        whrCursor, whrCon = gapdb.ConnectWHR()
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
    import gapdb
    try:
        tax = Taxonomy(spCode)

        xWalk = Crosswalk(spCode)[1:]

        comb = list(tax + xWalk)

        if completionStatus:
            rComp = str(gapdb.RangeCompleted(spCode))
            mComp = str(gapdb.ModelCompleted(spCode))

            comb.append(rComp)
            comb.append(mComp)

        comb = tuple([str(i) for i in comb])

        return comb

    except Exception as e:
        print(e)
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
    import gapdb
    code = code[0:5]
    sppCursor, sppCon = gapdb.ConnectSppDB()
    qryResult = sppCursor.execute("""SELECT strUniqueID
                                FROM dbo.tblAllSpecies
                                WHERE strUniqueID LIKE '""" + code + """%'
                                """).fetchall()

    del sppCursor
    sppCon.close()

    spCodes =[item[0] for item in qryResult]

    return spCodes