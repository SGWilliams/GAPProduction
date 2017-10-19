'''
Module for tasks related to GAP deductive habitat modeling.
'''
import gapdb, dictionaries


### Dictionary of data layers used in 2001
layers_2001 = {'ysnHydroWV': "https://doi.org/10.5066/F7JM28J1",
             'strForIntBuffer': "https://doi.org/10.5066/F7XW4HPN",
             'intIntoBuffOW': "https://doi.org/10.5066/F7JM28J1",
             'intElevMax' : "https://doi.org/10.5066/F72N515B",
             'PrimEcoSys': "https://doi.org/10.5066/F7959GF5",
             'AuxEcoSys': "https://doi.org/10.5066/F7959GF5",
             'intIntoBuffWV': "https://doi.org/10.5066/F7JM28J1",
             'intFromBuffFW': "https://doi.org/10.5066/F7JM28J1",
             'intElevMin': "https://doi.org/10.5066/F72N515B",
             'ysnHydroOW': "https://doi.org/10.5066/F7JM28J1",
             'ysnUrbanInclude': "https://doi.org/10.5066/F7PC318R",
             'strUseForInt': "https://doi.org/10.5066/F7XW4HPN",
             'intEdgeEcoWidth': {"Forest/Open Ecotone Only": "https://doi.org/10.5066/F7XW4HPN", 
                             "F/O + Shrubland/Woodland": "https://doi.org/10.5066/F7T43RZ7"},
             'intFromBuffWV': "https://doi.org/10.5066/F7JM28J1",
             'strStreamVel': "https://doi.org/10.5066/F7JM28J1",
             'strSalinity': "https://doi.org/10.5066/F7JM28J1",
             'strEdgeType': {"Forest/Open Ecotone Only": "https://doi.org/10.5066/F7XW4HPN", 
                             "F/O + Shrubland/Woodland": "https://doi.org/10.5066/F7T43RZ7"},
             'ysnHydroFW': "https://doi.org/10.5066/F7JM28J1",
             'ysnUrbanExclude': "https://doi.org/10.5066/F7PC318R",
             'strAvoid': "https://doi.org/10.5066/F7PC318R",
             'intFromBuffOW': "https://doi.org/10.5066/F7JM28J1",
             'Region': "https://doi.org/10.5066/F77H1HGT",
             
             'intSlopeMin': "https://doi.org/10.5066/F75D8QQF",
             'intSlopeMax': "https://doi.org/10.5066/F75D8QQF",
             'hucs': "https://doi.org/10.5066/F7DZ0754",
             'intPercentCanopy': "https://doi.org/10.5066/F7DZ0754"}


def getHabitatDescription(strUC):
    '''
    (string) -> string
    
    Returns the habitat description text for a species.
    
    Arguments:
    strUC -- Gap species code
    '''
    WHRCursor, WHRConnection = gapdb.ConnectWHR()
    desc = WHRCursor.execute("""SELECT hab.memSppHabDesc
                         FROM dbo.tblTaxa as hab
                         WHERE hab.strUC = '{0}'""".format(strUC)).fetchall()
    desc = desc[0][0]
    return desc


def getModelComments(strUC):
    '''
    (string) -> string
    
    Returns the modeling comments text for a species.
    
    Arguments:
    strUC -- Gap species code
    '''
    WHRCursor, WHRConnection = gapdb.ConnectWHR()
    desc = WHRCursor.execute("""SELECT hab.memSppComments
                         FROM dbo.tblTaxa as hab
                         WHERE hab.strUC = '{0}'""".format(strUC)).fetchall()
    desc = desc[0][0]
    return desc


def ExcludeModels():
    '''
    (None) -> tuple

    Retrieves tuple of models that are designated for exclusion in 
    tblAllSpecies.ysnInclude in the WHRDb.
    '''

    # Get a cursor and connection to WHR database
    whrCursor, whrCon = gapdb.ConnectWHR()
    # Execute the query to select model codes that match the passed species code
    models = whrCursor.execute("""SELECT a.strSpeciesModelCode
                            FROM dbo.tblAllSpecies as a
                            WHERE a.ysnInclude = 'False'""").fetchall()

    # Delete the cursor
    del whrCursor
    # Close the database connection
    whrCon.close()

    # Create a list of all the matching models
    hm = [str(item[0]) for item in models]

    # Return the list of matching model codes
    return tuple(hm)


def SppHabText(spp):
    '''
    (list) -> pandas dataframe
    
    This function queries the WHRDb for a species' habitat
        description text and populates a table with the
        text for all species provided in the list.
        
    Arguments:
    spp -- Python list of unique species codes (strUC)
        
    Example: 
    >>>dfHab = SppHabText(spp=["mSEWEx", "bAMROx"])
    '''
    import pandas as pd
    # Connect to db
    cursor, con = gapdb.ConnectWHR()
    # Build empty dataframe
    dfHabitat = pd.DataFrame(index=spp, 
                             columns=["SciName", "SppHabDesc"])
    dfHabitat.index.name = "strUC"
    for sp in spp:
        print sp
        # Fetch habitat description
        qry = cursor.execute(""" SELECT t.strUC, t.memSppHabDesc
                           FROM dbo.tblTaxa as t
                           WHERE t.strUC = ?""", sp).fetchone()
        # Populate table
        try:
            dfHabitat.loc[sp, "SppHabDesc"] = qry[1]
        except:
            dfHabitat.loc[sp, "SppHabDesc"] = "Error"
        dfHabitat.loc[sp, "SciName"] = gapdb.NameSci(sp)
    return dfHabitat


def SpReferences(sp):
    '''
    (string) -> pandas dataframe
    
    Builds and returns a dataframe containing citations/references for the 
        species that you gave.  It combines references associated with any of
        the species models' published, conus, and non-migratory models.
    
    Argument:
    sp -- A species code (strUC).
    
    Example:
    >>>df = SpReferences("bAMROx")
    >>>df.to_csv("R:/RobinRefs.csv")
    '''
    import pandas as pd
    # Connect to db
    cursor, con = gapdb.ConnectWHR()
    # Define empty objects to store results
    refCodes = set([])
    references = {}
    # Get a list of models for the species
    mods = ModelCodes(sp, publishedOnly=True, 
                               conusOnly=True, migratory=False)
    # Retrieve the reference codes for each model, collect new ones in the set
    for mod in mods:
        qry = cursor.execute("""SELECT j.strRefCode
                             FROM dbo.tblSppCitations as j 
                             WHERE j.strSpeciesModelCode = ?""",mod).fetchall()
        sprefCodes = set([x[0] for x in qry])
        refCodes = sprefCodes | refCodes
    # Retrieve the text for each code and add to a dictionary
    for code in refCodes:
        qry2 = cursor.execute("""SELECT r.memCitation
                              FROM dbo.tblCitations as r
                              WHERE r.strRefCode = ?""",code).fetchall()
        try:
            references[code] = str(qry2[0][0])
        except:
            references[code] = "ERROR"
    # Build a dataframe with strUC, SciName, and Reference text
    dfReferences = pd.DataFrame(index=references.keys(), 
                                columns=["memCitation"])
    dfReferences.index.name = "strRefCode"
    dfReferences["strUC"] = sp
    dfReferences["SciName"] = gapdb.NameSci(sp)
    for i in dfReferences.index:
        dfReferences.loc[i, "memCitation"] = references[i]
    # Return the resulting DataFrame
    return dfReferences


#### Function to get a dictionaries of map units used by species.
try:
    def LoadSpeciesMUs(UC, Range=True):
        '''
        (string, boolean) -> dictionary

        Returns a dictionary with python sets containing map units that are selected
            as primary (prim) in any of the species' models, auxiliary (aux) in any of the
            species' models, map units within the species' range (inRangeMU), map units
            not in the species' range (outRangeMU), and prim and aux converted to names
            instead of codes (primNames and auxNames).  A set of all map unit codes is
            returned as well (allMU).

        Arguments:
        UC -- a strUC code (e.g, mSEWEn)
        Range -- Defaults to True. Setting to True will run processes that extract a
        list of map units that occur within a species' range.

        Example:
        speciesMUs = loadSpeciesMapUnits("mSEWEn", Range=False)
        '''

        import gaprange
        if Range:
            allNames = gapdb.AllMUs()
            print("Getting map units within the species' range")
            rngMUNames = gaprange.EcoSysInRange(UC)
            inRngMU = set(gapdb.MUNamesToCodes(rngMUNames))
            allMU = set(gapdb.MUNamesToCodes(allNames))
            outRngMU = allMU - inRngMU
            primNames, auxNames = SpEcoSystems(UC, contiguousOnly=True)
            prim = set(gapdb.MUNamesToCodes(primNames))
            aux = set(gapdb.MUNamesToCodes(auxNames))
            UCSets = {"prim": prim, "aux": aux, "primNames": primNames,
                    "allMU": allMU, "inRangeMU": inRngMU, "outRangeMU": outRngMU,
                    "auxNames": auxNames}
            UCSets["keys"] = UCSets.keys()
            return UCSets
            return 'The sets are named "prim", "aux", "primNames", "auxNames", "inRangeMU", "outRangeMU", and "allMU"'

        else:
            print("Not using range")
            allNames = gapdb.AllMUs()
            allMU = set(gapdb.MUNamesToCodes(allNames))
            primNames, auxNames = SpEcoSystems(UC, contiguousOnly=True)
            prim = set(gapdb.MUNamesToCodes(primNames))
            aux = set(gapdb.MUNamesToCodes(auxNames))
            UCSets = {"prim": prim, "aux": aux, "primNames": primNames,
                    "allMU": allMU, "inRangeMU": [], "outRangeMU": [],
                    "auxNames": auxNames}
            UCSets["keys"] = UCSets.keys()
            return UCSets
            return 'The sets are named "prim", "aux", "primNames", "auxNames", "inRangeMU", "outRangeMU", and "allMU"'

except:
    def LoadSpeciesMUs(UC):
        '''
        (string, boolean) -> dictionary

        Returns a dictionary with python sets containing map units that are selected
            as primary (prim) in any of the species' models, auxiliary (aux) in any of the
            species' models, and prim and aux converted to names instead of codes
            (primNames and auxNames).  A set of all map unit codes is returned as
            well (allMU).

        Arguments:
        UC -- a strUC code (e.g, mSEWEn)

        Example:
        speciesMUs = loadSpeciesMapUnits("mSEWEn")
        '''
        print("Not using range")
        allNames = gapdb.AllMUs()
        allMU = set(gapdb.MUNamesToCodes(allNames))
        primNames, auxNames = SpEcoSystems(UC,contiguousOnly=True)
        prim = set(gapdb.MUNamesToCodes(primNames))
        aux = set(gapdb.MUNamesToCodes(auxNames))
        UCSets = {"prim": prim, "aux": aux, "primNames": primNames,
                "allMU": allMU, "auxNames": auxNames}
        UCSets["keys"] = UCSets.keys()
        return UCSets
        return 'The sets are named "prim", "aux", "primNames", "auxNames", and "allMU"'


def RemoveAlienMUs(models):
    '''
    (list) -> None

    Goes through each model in a list and unselects primary and auxiliary map units
        which are not found within the model's region.

    Arguments:
    Models -- A list of model codes (e.g., ["mRESQx-y5", "mRESQx-y4"])
    '''
    for model in models:
        prim, aux = ModelEcoSystems(model)

        alienPMU = [x for x in prim if gapdb.MuInRegion(x, model[-1:]) == False]
        SetMUs(model, alienPMU, select=False)

        alienAMU = [x for x in aux if gapdb.MuInRegion(x, model[-1:]) == False]
        SetMUs(model, alienAMU, primary=False, select=False)


def EcoSystemModels(ecologicalSystem, season='all', contiguousOnly=False):
    '''
    (int) -> list, list

    Returns two lists, the first of which contains the names of species
        that have a primary association with the ecological system, and
        the second of which contains a list of species with a secondary
        association with the ecological system. Only includes models
        for which ysnInclude is True; omits models with region code 0

    Arguments:
    ecologicalSystem -- The 4-digit land cover map unit code.
    season -- The season for which you wish to return ecological systems. By
        default, all seasons will be retrieved. You may enter: 's' or 'summer'
        for summer models; 'w' or 'winter' for winter models; 'y', 'year',
        'yearround', or 'year-round' for year-round models.
    contiguousOnly -- An optional, boolean parameter, indicating whether you
        wish to return codes only for models within the contiguous U.S. By
        default, it is set to False, which means that all model codes will be
        returned, regardless of their region.
    '''

    try:
        # Get WHRdb cursor and connection
        whrCursor, whrCon = gapdb.ConnectWHR()
        # Query the primary map units
        prim = whrCursor.execute("""SELECT strSpeciesModelCode
                                FROM dbo.tblSppMapUnitPres
                                WHERE ysnPres='True' AND intLSGapMapCode = ?""", ecologicalSystem).fetchall()
        # Query the auxiliary map units
        aux = whrCursor.execute("""SELECT strSpeciesModelCode
                                FROM dbo.tblSppMapUnitPres
                                WHERE ysnPresAuxiliary='True' AND intLSGapMapCode = ?""", ecologicalSystem).fetchall()

        # Delete the WHRdb cursor and close the connection
        del whrCursor
        whrCon.close()

        # Process the lists to get the first item from each tuple,to remove
        # trailing/leading spaces, and to sort alphabetically
        prim = [str(i[0].strip()) for i in prim]
        prim.sort()
        aux = [str(i[0].strip()) for i in aux]
        aux.sort()

        # If the user only wishes to return models from the contiguous U.S....
        if contiguousOnly:
            # Select only those models with region codes less than 7
            prim = [i for i in prim if int(i[-1]) < 7]
            aux = [i for i in aux if int(i[-1]) < 7]

        # Filter by the passed season
        season = season.lower()
        if season != 'all':
            if season == 's' or season == 'summer':
                prim = [i for i in prim if i[-2] == 's']
                aux = [i for i in aux if i[-2] == 's']
            elif season == 'w' or season == 'winter':
                prim = [i for i in prim if i[-2] == 'w']
                aux = [i for i in aux if i[-2] == 'w']
            elif season == 'y' or season == 'year-round' or season == 'yearround' or season == 'year':
                prim = [i for i in prim if i[-2] == 'y']
                aux = [i for i in aux if i[-2] == 'y']

        # Return the lists of primary and auxiliary map units
        return prim, aux

    except:
        return False, False


def EcoSystemSpecies(ecologicalSystem, season='all', contiguousOnly=False):
    '''
    (int) -> list, list

    Returns two lists, the first of which contains the names of species
        that have a model with a primary association with the ecological system, and
        the second of which contains a list of species with a model
        with secondary association with the ecological system. Only includes species
        witha model for which ysnInclude is True; omits models with region code 0.

    Argument:
    ecologicalSystem -- The 4-digit land cover map unit code.
    season -- The season for which you wish to return ecological systems. By
        default, all seasons will be retrieved. You may enter: 's' or 'summer'
        for summer models; 'w' or 'winter' for winter models; 'y', 'year',
        'yearround', or 'year-round' for year-round models.
    contiguousOnly -- An optional, boolean parameter, indicating whether you
        wish to return codes only for models within the contiguous U.S. By
        default, it is set to False, which means that all model codes will be
        returned, regardless of their region.
    '''
#   CAN SOME OF THIs Be replace by the function above? needs argument filterss
    try:
        prim, aux = EcoSystemModels(ecologicalSystem, season=season, contiguousOnly=False)
        prim = set([i[:6] for i in prim])
        aux = set([i[:6] for i in aux])

        # Return the lists of primary and auxiliary map units
        return list(prim), list(aux)

    except:
        return False, False

def ModelExists(modelCode):
    '''
    (string) -> boolean

    Checks a model code to verify that it is in the database. ...mostly used
        internally, but could have some validity as public function.

    Argument:
    modelCode -- Any string, but the purpose of the function is to verify that
        this is a valid, nine-character, GAP model code.

    Examples:
    >>> ModelExists('mbishx-y4')
    True
    >>> ModelExists('flurbington')
    False
    >>> ModelExists('mBISHx-y9')
    False
    '''
    # Connect to the WHRdb
    cur, conn = gapdb.ConnectWHR()

    # The base query
    qry = """SELECT t.strSpeciesModelCode
        FROM dbo.tblAllSpecies as t
        WHERE t.strSpeciesModelCode = ?"""

    # Execute the query with the model code
    res = cur.execute(qry, str(modelCode)).fetchone()

    # If the query returned a valid entry, set the variable res to True
    if res: res = True
    # Otherwise, set res to False
    else: res = False

    # Close the cursor/connection
    del cur, conn

    return res




def ModelCodes(spCode, season='all', publishedOnly=False, conusOnly=True,
               migratory=False):
    '''
    (string, string, [boolean], [boolean], [boolean]) -> tuple
    
    Retrieves list of models for the given species. Only includes models
    for which ysnInclude is True; omits models with region code 0
    
    Notes:
    This is pulling from two different tables in WHRdb.  The code could probably be 
        a little more succinct if a join were specified in the sql query passed.
    
    Arguments:
    spCode -- The species' unique GAP ID
    season -- The season for which you wish to return models. By default, all
        seasons will be retrieved. You may enter: 's' or 'summer' for summer
        models; 'w' or 'winter' for winter models; 'y', 'year', 'yearround', or
        'year-round' for year-round models.
    publishedOnly -- Optional boolean parameter to include only published models.
        By default, it is set as False, which returns all models.
    conusOnly -- Optional boolean parameter to include only models within CONUS.
        By default, it is set as True, which returns only CONUS models.
    migratory -- Optional boolean parameter to include migratory models.
        By default, it is set as False, which excludes migratory models.
    
    Example:
    >>> ModelCodes('rGLSNx')
    (u'rGLSNx-y5', u'rGLSNx-y6', u'rGLSNx-y4')
    >>> gp.gapdb.ModelCodes('bbaeax', 's', True)
    ['bBAEAx-s1', 'bBAEAx-s2', 'bBAEAx-s3', 'bBAEAx-s4', 'bBAEAx-s5', 'bBAEAx-s6']
    >>> gp.gapdb.ModelCodes('bbaeax', 'winter')
    ['bBAEAx-w1', 'bBAEAx-w2', 'bBAEAx-w3', 'bBAEAx-w4', 'bBAEAx-w5', 'bBAEAx-w6']
    '''
    
    # Get a cursor and connection to WHR database
    whrCursor, whrCon = gapdb.ConnectWHR()
    
    # Execute a query to select model codes that match the passed species code
    # from tblAllSpecies
    models = whrCursor.execute("""SELECT strSpeciesModelCode
                            FROM dbo.tblAllSpecies
                            WHERE strUC LIKE ?
                            AND ysnInclude = 'True'
                            AND strSpeciesModelCode NOT LIKE '%0'
                            """, spCode + '%').fetchall()
    
    # Pull model codes out of return tuple
    mcsAllSpec = [str(item[0]) for item in models]
    
    # If the user only wishes to return models from the contiguous U.S....
    if conusOnly:
        # Select only those models with region codes less than 7
        mcsAllSpec = [i for i in mcsAllSpec if int(i[-1]) < 7]
        
    # Filter by the passed season
    season = season.lower()
    if season != 'all':
        if season == 's' or season == 'summer':
            mcsAllSpec = [i for i in mcsAllSpec if i[-2] == 's']
        elif season == 'w' or season == 'winter':
            mcsAllSpec = [i for i in mcsAllSpec if i[-2] == 'w']
        elif season == 'y' or season == 'year-round' or season == 'yearround' or season == 'year':
            mcsAllSpec = [i for i in mcsAllSpec if i[-2] == 'y']
    
    # Migratory filtering
    # Get list of migratory models
    migs = [x for x in mcsAllSpec if x[-2] == "m"]
    # Filter out migratory models
    mcsAllSpec = [x for x in mcsAllSpec if x[-2] != "m"]
    # If the user wishes to include migratory models.
    if migratory:
        mcsAllSpec = mcsAllSpec + migs
    
    if publishedOnly:
    # Execute a query to select model codes that match the passed species code
    # from tblModelStatus
        qry = """SELECT strSpeciesModelCode
                FROM dbo.tblModelStatus
                WHERE strSpeciesModelCode LIKE '{0}%'""".format(spCode)
        qry = qry + '\nAND strModelStatusAll = \'Publishing Completed\''
        models_status = whrCursor.execute(qry).fetchall()
        mcsModelStatus = set([item[0] for item in models_status])
        # Filter out models not in tblAllSpecies, to remove non-"publishing completed"
        mcs = tuple(set(mcsAllSpec) & mcsModelStatus)
    else:
        mcs = tuple(mcsAllSpec)
        
    # Delete the cursor
    del whrCursor
    # Close the database connection
    whrCon.close()    
    
    # Return the list of matching model codes
    return mcs


def HandModels():
    '''
    (None) -> tuple

    Retrieves list of models that require hand modeling. Only includes models
    for which ysnInclude is True; omits models with region code 0
    '''

    # Get a cursor and connection to WHR database
    whrCursor, whrCon = gapdb.ConnectWHR()
    # Execute the query to select model codes that match the passed species code
    models = whrCursor.execute("""SELECT a.strSpeciesModelCode
                            FROM dbo.tblAllSpecies as a INNER JOIN dbo.tblModelingAncillary as m
                            ON a.strSpeciesModelCode = m.strSpeciesModelCode
                            WHERE a.ysnInclude = 'True'
                            AND m.ysnHandModel = 'True'
                            AND a.strSpeciesModelCode NOT LIKE '%0'
                            """).fetchall()

    # Delete the cursor
    del whrCursor
    # Close the database connection
    whrCon.close()

    # Create a list of all the matching models
    hm = [str(item[0]) for item in models]

    # Return the list of matching model codes
    return tuple(hm)


def ModelEcoSystems(modelCode):
    '''
    (str) -> list, list

    Returns two lists, the first of which contains the names of ecological
        systems that have been selected as primary habitat for the model, and
        the second of which contains those ecological systems selected as
        auxiliary habitat.

    Argument:
    modelCode -- The 9-character GAP model code.
    '''
    try:
        # Get WHRdb cursor and connection
        whrCursor, whrCon = gapdb.ConnectWHR()
        # Query the primary map units
        prim = whrCursor.execute("""SELECT t.strLSGapName
                                FROM dbo.tblMapUnitDesc AS t INNER JOIN dbo.tblSppMapUnitPres AS s ON t.intLSGapMapCode = s.intLSGapMapCode
                                WHERE s.ysnPres='True' AND s.strSpeciesModelCode = ?""", modelCode).fetchall()
        # Query the auxiliary map units
        aux = whrCursor.execute("""SELECT t.strLSGapName
                                FROM dbo.tblMapUnitDesc AS t INNER JOIN dbo.tblSppMapUnitPres AS s ON t.intLSGapMapCode = s.intLSGapMapCode
                                WHERE s.ysnPresAuxiliary='True' AND s.strSpeciesModelCode = ?""", modelCode).fetchall()

        # Delete the WHRdb cursor and close the connection
        del whrCursor
        whrCon.close()

        # Process the lists to get the first item from each tuple,to remove
        # trailing/leading spaces, and to sort alphabetically
        prim = [str(i[0].strip()) for i in prim]
        prim.sort()
        aux = [str(i[0].strip()) for i in aux]
        aux.sort()

        # Return the lists of primary and auxiliary map units
        return prim, aux

    except:
        return False, False


def SpEcoSystems(spCode, season='all', contiguousOnly=True, 
                 publishedOnly=False, migratory=False):
    '''
    (string) -> list, list

    Returns two lists, the first of which contains the names of ecological
        systems that have been selected as primary habitat in any or all of the
        passed species' models, and the second of which contains those
        ecological systems selected as auxiliary habitat.
    
    Arguments:
    spCode -- The species' GAP code; you can opt to pass either the 6-character
        code or to retrieve systems selected by any or all subspecies/species by
        submitting a shorter code. E.g.: SpEcoSystems('mwtde') would retrieve
        systems from the mwtdex, mwtdel, mwtden, and mwtdec models, grouping all
        systems into the two lists.
    season -- The season for which you wish to return ecological systems. By
        default, all seasons will be retrieved. You may enter: 's' or 'summer'
        for summer models; 'w' or 'winter' for winter models; 'y', 'year',
        'yearround', or 'year-round' for year-round models.
    contiguousOnly -- An optional, boolean parameter, indicating whether you
        wish to return codes only for models within the contiguous U.S. By
        default, it is set to False, which means that all model codes will be
        returned, regardless of their region.
    publishedOnly -- Optional boolean parameter to include only published models.
        By default, it is set as False, which returns all models.
    migratory -- Optional boolean parameter to include migratory models.
        By default, it is set as False, which excludes migratory models.
    
    '''
    print("!!!! NOTE -- the publishedOnly option may not be up to date. The appropriate tables need to be checked.")
    try:
        # Get the model codes that match the passed species code
        models = ModelCodes(spCode=spCode, season=season, 
                            publishedOnly=publishedOnly, 
                            conusOnly=contiguousOnly, migratory=migratory)
        # Initialize empty lists to store the primary and auxiliary map units
        essP = []
        essA = []
        # For each model
        for m in models:
            # Get the model's map units
            p, a = ModelEcoSystems(m)
            # For each primary unit
            for i in p:
                # If it's not in the primary MU list, add it
                if i not in essP:
                    essP.append(i)
            # For each auxiliary unit
            for i in a:
                # If it's not in the auxiliary MU list, add it
                if i not in essA:
                    essA.append(i)

        # Return the lists of primary and auxiliary map units
        return essP, essA

    except:
        return False, False


def ModelAsDictionary(model, ecolSystem="codes"):
    '''
    (string, boolean) -> dictionary

    Returns a dictionary that includes a key for each of a regional model's variables.
        NOTE: Only works for conus models.

    Arguments:
    model -- a model code (e.g., "bcoyex-s6")
    ecolSystem -- specifies whether to return ecological system names, codes, or both.
        Defaults codes, which returns codes and takes a little longer to run.  Choosing
        "both" will return a list of tuples (code, name).

    Dictionary keys -- ['intIntoBuffFW', 'ScientificName', 'ysnHydroWV', 'intAuxBuff',
                        'strForIntBuffer', 'ysnHandModel', 'intIntoBuffOW', 'Season',
                        'intElevMax', 'PrimEcoSys', 'AuxEcoSys', 'SpeciesCode',
                        'intIntoBuffWV', 'cbxContPatch', 'ysnUrbanExclude', 'intFromBuffFW',
                        'intElevMin', 'ysnHydroOW', 'Region', 'CommonName',
                        'ysnUrbanInclude', 'strUseForInt', 'intEdgeEcoWidth',
                        'intFromBuffWV', 'strStreamVel', 'strSalinity', 'strEdgeType',
                        'ysnHydroFW', 'intContPatchSize', 'strAvoid', 'intFromBuffOW',
                        'memHMNotes']

    Example:
    modelDictionary = ModelAsDictionary(model="mSEWEx-y1", ecolSystem="both")
    '''
    #import dictionaries
    ################### Create a function to retrieve the desired ancillary variable
    ################################################################################
    def __getVariable(model, variable):
        WHRCursor, WHRConnection = gapdb.ConnectWHR()
        var = WHRCursor.execute("""SELECT anc.{0}
                             FROM dbo.tblModelingAncillary as anc
                             WHERE anc.strSpeciesModelCode = '{1}'""".format(variable, model)).fetchall()
        var = var[0][0]
        return var

    ################################################  Add parameters to a dictionary
    ################################################################################
    # Initialize dictionary
    modelDict = {}

    # Regiona and season
    region = dictionaries.regionsDict_Num_To_Name[int(model[8])]
    modelDict["Region"] = region

    season = model[7]
    modelDict["Season"] = season
                                                    
    # Species names
    SpeciesCode = model[:6]
    modelDict["SpeciesCode"] = SpeciesCode

    Common = gapdb.NameCommon(SpeciesCode)
    modelDict["CommonName"] = Common

    Scientific = gapdb.NameSci(SpeciesCode)
    modelDict["ScientificName"] = Scientific
    
    Sub = gapdb.NameSubspecies(SpeciesCode)
    modelDict["SubspeciesName"] = Sub
    
    # Who worked on the model
    modelDict["Modeler"] = gapdb.Who(SpeciesCode, action="edited")
    modelDict["Reviewer"] = gapdb.Who(SpeciesCode, action="reviewed")
    
    # Land Cover Map Units
    if ecolSystem == "codes":
        cursor, conn = gapdb.ConnectWHR()
        PrimEcoSys = cursor.execute("""SELECT j.intLSGapMapCode
                                  FROM dbo.tblSppMapUnitPres as j 
                                  WHERE j.strSpeciesModelCode = ? 
                                  """, model).fetchall()
        modelDict["PrimEcoSys"] =[x[0] for x in PrimEcoSys]
        AuxEcoSys = cursor.execute("""SELECT j.intLSGapMapCode
                                  FROM dbo.tblSppMapUnitPres as j 
                                  WHERE j.strSpeciesModelCode = ? 
                                  """, model).fetchall()
        modelDict["AuxEcoSys"] =[x[0] for x in AuxEcoSys]
    elif ecolSystem == "names":
        primary, auxiliary = ModelEcoSystems(model)
        modelDict["PrimEcoSys"] = primary
        modelDict["AuxEcoSys"] = auxiliary
    elif ecolSystem == "both":
        cursor, conn = gapdb.ConnectWHR()
        qry1 = cursor.execute("""SELECT j.intLSGapMapCode, 
                                                           d.strLSGapName
                                  FROM dbo.tblSppMapUnitPres as j 
                                  INNER JOIN dbo.tblMapUnitDesc as d 
                                  ON d.intLSGapMapCode = j.intLSGapMapCode
                                  WHERE (j.strSpeciesModelCode = ?) 
                                  AND (j.ysnPres = 1)""", model).fetchall()
        modelDict["PrimEcoSys"] = [(x[0], x[1].strip()) for x in qry1]


        qry2 =  cursor.execute("""SELECT j.intLSGapMapCode, 
                                                          d.strLSGapName
                                 FROM dbo.tblSppMapUnitPres as j
                                 INNER JOIN dbo.tblMapUnitDesc as d 
                                 ON d.intLSGapMapCode = j.intLSGapMapCode
                                 WHERE (j.strSpeciesModelCode = ?) 
                                 AND (j.ysnPresAuxiliary = 1)""", model).fetchall()
        modelDict["AuxEcoSys"] = [(x[0], x[1].strip()) for x in qry2]
       
    # Hand Model
    ysnHandModel = __getVariable(model, "ysnHandModel")
    modelDict["ysnHandModel"] = ysnHandModel
    
    # Hand Model Comments
    memHandModelNotes = __getVariable(model, "memHMNotes")
    modelDict["memHandModelNotes"] = memHandModelNotes

    # Hydrography variables
    ysnHydroFW = __getVariable(model, "ysnHydroFW")
    modelDict["ysnHydroFW"] = ysnHydroFW

    intFromBuffFW = __getVariable(model, "intFromBuffFW")
    modelDict["intFromBuffFW"] = intFromBuffFW

    intIntoBuffFW = __getVariable(model, "intIntoBuffFW")
    modelDict["intIntoBuffFW"] = intIntoBuffFW

    ysnHydroOW = __getVariable(model, "ysnHydroOW")
    modelDict["ysnHydroOW"] = ysnHydroOW

    intFromBuffOW = __getVariable(model, "intFromBuffOW")
    modelDict["intFromBuffOW"] = intFromBuffOW

    intIntoBuffOW = __getVariable(model, "intIntoBuffOW")
    modelDict["intIntoBuffOW"] = intIntoBuffOW

    ysnHydroWV = __getVariable(model, "ysnHydroWV")
    modelDict["ysnHydroWV"] = ysnHydroWV

    intFromBuffWV = __getVariable(model, "intFromBuffWV")
    modelDict["intFromBuffWV"] = intFromBuffWV

    intIntoBuffWV = __getVariable(model, "intIntoBuffWV")
    modelDict["intIntoBuffWV"] = intIntoBuffWV

    strSalinity = __getVariable(model, "strSalinity")
    modelDict["strSalinity"] = strSalinity

    strStreamVel = __getVariable(model, "strStreamVel")
    modelDict["strStreamVel"] = strStreamVel

    # Edge variables
    strEdgeType = __getVariable(model, "strEdgeType")
    modelDict["strEdgeType"] = strEdgeType

    intEdgeEcoWidth = __getVariable(model, "intEdgeEcoWidth")
    modelDict["intEdgeEcoWidth"] = intEdgeEcoWidth

    # Forest interior variables
    strUseForInt = __getVariable(model, "strUseForInt")
    modelDict["strUseForInt"] = strUseForInt

    strForIntBuffer = __getVariable(model, "strForIntBuffer")
    modelDict["strForIntBuffer"] = strForIntBuffer

    # Patch size
    cbxContPatch = __getVariable(model, "cbxContPatch")
    modelDict["cbxContPatch"] = cbxContPatch

    intContPatchSize = __getVariable(model, "intContPatchSize")
    modelDict["intContPatchSize"] = intContPatchSize

    # Auxiliary LC Map Unit Buffer Distance
    intAuxBuff = __getVariable(model, "intAuxBuff")
    modelDict["intAuxBuff"] = intAuxBuff

    # Urban avoid layer
    strAvoid = __getVariable(model, "strAvoid")
    modelDict["strAvoid"] = strAvoid

    ysnUrbanExclude = __getVariable(model, "ysnUrbanExclude")
    modelDict["ysnUrbanExclude"] = ysnUrbanExclude

    ysnUrbanInclude = __getVariable(model, "ysnUrbanInclude")
    modelDict["ysnUrbanInclude"] = ysnUrbanInclude

    # Elevation variables
    intElevMin = __getVariable(model, "intElevMin")
    modelDict["intElevMin"] = intElevMin

    intElevMax = __getVariable(model, "intElevMax")
    modelDict["intElevMax"] = intElevMax
    
    # Slope variables
    intSlopeMin = __getVariable(model, "intSlopeMin")
    modelDict["intSlopeMin"] = intSlopeMin

    intSlopeMax = __getVariable(model, "intSlopeMax")
    modelDict["intSlopeMax"] = intSlopeMax
    
    # Slope variables
    intPercentCanopy = __getVariable(model, "intPercentCanopy")
    modelDict["intPercentCanopy"] = intPercentCanopy

    return modelDict


def SetMUs(modelCode, mapUnits, primary=True, select=True):
    '''
    (str, list/tuple, [boolean]) -> boolean

    For the given model, selects the passed map units.

    Arguments:
    modelCode -- The 9-character, GAP model code to which you wish to apply the
        map unit selections.
    mapUnits -- The names/codes of the map units you wish to select for the
        model.
    primary -- An optional parameter, indicating whether you wish to apply the
        map units as primary or auxiliary. By default, this parameter is set to
        True, meaning that the map units are selected as primary. If False,
        the map units will be selected as auxiliary.
    select -- An optional parameter, indicating whether the map units should be
        selected or unselected. By default, select is set to True, meaning that
        the passed map units will be selected for the given model. select=False
        would remove the passed map units from the given model.

    Example:
    >>> SetMU('mNAROx-y4', ['Developed, Low Intensity', 1201, 1203, 'Open Water (Fresh)'])
    True
    '''
    try:
        # Get the cursor and connection to the WHRDB
        cur, conn = gapdb.ConnectWHR("SpeciesManager", "G@pp3r")

        # Convert the passed map units to the map unit codes...if they are not
        # codes already.
        mapUnits = gapdb.MUNamesToCodes(mapUnits)

        # If setting as primary
        if primary:
            # Query framework
            qry = """UPDATE dbo.tblSppMapUnitPres
                SET ysnPres=?
                WHERE strSpeciesModelCode=?
                AND intLSGapMapCode=?"""
        # If setting as auxiliary
        else:
            # Query framework
            qry = """UPDATE dbo.tblSppMapUnitPres
                SET ysnPresAuxiliary=?
                WHERE strSpeciesModelCode=?
                AND intLSGapMapCode=?"""

        # If the user opted to select the map units
        if select:
            # Set the selectionType variable to be the string 'True'
            selectionType = 'True'
        # If the user did not opt to select the map units
        else:
            # Set the selectionType variable to be the string 'False'
            selectionType = 'False'

        # For each mu...
        for i in mapUnits:
            # Execute the update query
            count = cur.execute(qry, selectionType, modelCode, i).rowcount

        # Commit the changes to the database
        conn.commit()

        # Close the cursor and the database connection
        del cur, conn

        # Return True is the function processed properly
        return True

    except Exception as e:
        print e
        return False


def SpMuDiscrepancies(spCode, season='all', contiguousOnly=True):
    '''
    (string, [string], [boolean]) -> list

    Returns a list of map units that are selected for at least one model but
        that are not selected for at least one other model, the region of
        which the map unit occurs within.

    Arguments:
    spCode -- The species' GAP code; you can opt to pass either the 6-character
        code or to retrieve systems selected by any or all subspecies/species by
        submitting a shorter code. E.g.: SpEcoSystems('mwtde') would retrieve
        systems from the mwtdex, mwtdel, mwtden, and mwtdec models, grouping all
        systems into the two lists.
    season -- The season for which you wish to examine ecological systems. By
        default, all seasons will be retrieved. You may enter: 's' or 'summer'
        for summer models; 'w' or 'winter' for winter models; 'y', 'year',
        'yearround', or 'year-round' for year-round models.
    contiguousOnly -- An optional, boolean parameter, indicating whether you
        wish to examine only models within the contiguous U.S. By default, it is
        set to True, which means that only models within the conterminous U.S.
        will be examined.
    '''
    # Get a list of the species' model codes
    models = ModelCodes(spCode, season, contiguousOnly)
    # Get a list of ecological systems selected for the species
    prim, aux = SpEcoSystems(spCode, season, contiguousOnly)

    # Initialize an empty list to track the discrepancies
    discrepancies = []

    # For each model
    for m in models:
        # Get the model's selected map units
        mPrim, mAux = ModelEcoSystems(m)
        # Get the model's region code
        reg = m[-1]
        # Search the primary map units across all models for the species
        for mu in prim:
            #  if the map unit is in the region
            if gapdb.MuInRegion(mu, reg):
                # if the map unit is not selected for this model
                if mu not in mPrim:
                    # if the map unit has not already been noted
                    if mu not in discrepancies:
                        # add it to the list of discrepancies
                        discrepancies.append(mu)
        # ...do the same for the auxiliary map units
        for mu in aux:
            if gapdb.MuInRegion(mu, reg):
                if mu not in mAux:
                    if mu not in discrepancies:
                        discrepancies.append(mu)

    return discrepancies



def ModelMuDiscrepancies(templateModel, compareModel):
    '''
    (string, string) -> list, list, list, list

    Identifies specific inconsistencies in the map unit selection between the
        two input models. This function is used internally by the
        ResolveMuDiscrepancies() function, but it can also be used to preview
        the changes that that function will make to the database.

        Returns four lists, which contain:
            1) The primary map units that occur in both regions and are
                selected for the template model but not selected for the compare
                model.
            2) The primary map units that occur in both regions and are not
                selected for the template model but are selected for the compare
                model.
            3) The auxiliary map units that occur in both regions and are
                selected for the template model but not selected for the compare
                model.
            4) The auxiliary map units that occur in both regions and are not
                selected for the template model but are selected for the compare
                model.

    Arguments:
    templateModel -- The nine-character GAP model code for the model you wish to
        treat as the template (or the correct model)
    compareModel -- The nine-character GAP model code for the model you wish to
        compare to the template model.

    Example:
    >>> ModelMuDiscrepancies('mbishx-y1', 'mbishx-y4')
    (['Barren Land', 'California Montane Woodland and Chaparral', 'California Xeric Serpentine Chaparral', 'Central California Coast Ranges Cliff and Canyon'],
    ['California Central Valley and Southern Coastal Grassland', 'Mediterranean California Subalpine-Montane Fen'],
    ['California Lower Montane Blue Oak-Foothill Pine Woodland and Savanna', 'California Montane Jeffrey Pine-(Ponderosa Pine) Woodland'],
    ['California Central Valley and Southern Coastal Grassland', 'Mediterranean California Subalpine-Montane Fen'])
    '''
    # Verify that valid model codes were passed.
    if not ModelExists(templateModel) or not ModelExists(compareModel):
        print 'One of the models passed to ModelMuDiscrepancies(), either\n%s or %s, does not exist.' % (templateModel, compareModel)
        return False

    # Get the selected map units for each input model
    prim, aux = ModelEcoSystems(templateModel)
    cPrim, cAux = ModelEcoSystems(compareModel)

    # Get the region code for each input model
    tempReg = templateModel[-1]
    compReg = compareModel[-1]

    # Initialize an empty list to store the names of ecological systems that
    # occur in the template model but not within the compare model.
    primMissing = []
    # For each primary system in the template model
    for i in prim:
        # if the mu occurs in the compare model region
        if gapdb.MuInRegion(i, compReg):
            # if the mu is not selected for the compare model
            if i not in cPrim:
                # store the mu name
                primMissing.append(i)

    # Initialize an empty list to store the names of ecological systems that
    # occur in the compare model but not within the template model.
    primExtra = []
    # For each primary system in the compare model
    for i in cPrim:
        # if the mu occurs in the template model region
        if gapdb.MuInRegion(i, tempReg):
            # if the mu is not selected for the template model
            if i not in prim:
                # store the mu name
                primExtra.append(i)

    # Initialize an empty list to store the names of aux ecological systems that
    # occur in the template model but not within the compare model.
    auxMissing = []
    # For each auxiliary system in the template model
    for i in aux:
        # If the mu occurs in the compare model region
        if gapdb.MuInRegion(i, compReg):
            # if the mu is not selected for the compare model
            if i not in cAux:
                # store mu name
                auxMissing.append(i)

    # Initialize an empty list to store the names of aux ecological systems that
    # occur in the compare model but not within the template model.
    auxExtra = []
    # For each auxiliary system in the compare model
    for i in cAux:
        # If the mu occurs in the template region
        if gapdb.MuInRegion(i, tempReg):
            # if the mu is not selected for the template model
            if i not in aux:
                # store the mu name
                auxExtra.append(i)

    # Return all four lists
    return primMissing, primExtra, auxMissing, auxExtra


def ResolveMuDiscrepancies(templateModel, changeModel, uid, pwd):
    '''
    (string, string, string, string) -> None

    Resolves inconsistencies in the map unit selection between the two input
        models by setting the change model to match the selections of the
        template model.

    Note: This function is not only intended to address regional differences for
        a given taxon, but could also be used to address differences within a
        region between subspecies or other similar models.

    Arguments:
    templateModel -- The nine-character GAP model code for the model you wish to
        treat as the template (or the correct model)
    changeModel -- The nine-character GAP model code for the model you wish to
        change to match the template model.
    uid -- A user id to connect to the WHRdb. The user must have editing
        priveleges; otherwise, the function will fail.
    pwd -- The password that matches uid.
    '''
    # Verify that valid model codes were passed.
    if not ModelExists(templateModel) or not ModelExists(changeModel):
        print 'One of the models passed to ResolveMuDiscrepancies(), either\n%s or %s, does not exist.' % (templateModel, changeModel)
        return False

    # Get the lists of the map unit discrepancies
    primMissing, primExtra, auxMissing, auxExtra = ModelMuDiscrepancies(templateModel, changeModel)

    # Create a cursor and a connection within the database
    cur, conn = gapdb.ConnectWHR(uid, pwd)

    # To address primary map units that are selected in the template model but
    # not in the change model:
    SetMUs(changeModel, primMissing)

    # To address primary map units that are selected in the change model but not
    # in the template model:
    SetMUs(changeModel, primExtra, select=False)

    # To address auxiliary map units that are selected in the template model but
    # not in the change model:
    SetMUs(changeModel, auxMissing, primary=False)

    # To address auxiliary map units that are selected in the change model but
    # not in the template model:
    SetMUs(changeModel, auxExtra, False, False)

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and the database connection
    del cur, conn

    return
    
#############################  MODELING WORKFLOW FUNCTIONS
##########################################################
    
def RunModel(modelCode, regionalDir, year=2011):
    '''
    (string, string, string?) -> raster object saved to outDir

    Runs the model for the passed regional-seasonal model code, using the
        input data for the year provided and saves output in regionalDir.  Also
        returns output as a raster object.

    Arguments:
    modelCode -- Species-region-season code.
    regionalDir -- Directory where to save output.
    year -- Year of input data that you wish to create.

    Example:
    >>> RunModel("mSEWEx-y4", "T:/Output/", 2011)
    
    '''
    # Use year to locate directories for data

    print("RunModel - No code yet")


def StartEdit_1(modelCode, initials):
    '''
    (string, string) -> changes to WHRdb

    Changes status of model to "editing started" in WHRdb.

    Arguments:
    modelCode -- Species-region-season code.
    initials -- Your initials.  

    Example:
    >>> StartEdit_1("mSEWEx-y4", "NMT")
    '''
    # Change the model status to "editing started"

    # Record initials in editor field

    # Email when done
    
    print("STEP 1 -- No code yet")


def EndEdit_2(modelCode, initials):
    '''
    (string, string) -> changes to WHRdb

    Changes status of model to "editing complete" in WHRdb.

    Arguments:
    modelCode -- Species-region-season code.
    initials -- Your initials.  

    Example:
    >>> EndEdit_2("mSEWEx-y4", "NMT")
    '''
    
    # Change the model status to "editing complete"

    # Record initials in editor field

    # Email when done

    
    print("Step 2 -- No code yet")


def Mosaic_3(rasters, initials, mosaicDir, overwrite=True):
    '''
    (list, string, string, [Boolean]) -> raster object, saved raster

    Changes status of model to "mosaicing started" in WHRdb.

    Arguments:
    modelCodes -- List of species-region-season codes to mosaic.
    initials -- Your initials.
    mosaicDir -- Where to save the mosaiced models.
    overwrite -- True/False whether to overwrite any existing mosaic.

    Example:
    >>> Mosaic_3(["T:/Output/mSEWEx-y4", "T:/Output/mSEWEx-y1"], "NMT",
                "T:/Output/Mosaics/")
    '''
    
    # Change the model status to "mosaicing started"

    # Record initials in mosaicker field
    
    # Verify that a map exists for each season-region-model

    # Sum seasonal outputs within regions

    # Mosaic - make sure environments (snap) are correctly handled.
        
    # Email when done
        
    print("Step 3 -- No code yet")


def VerifyMosaic_4(strUC, initials, mosaicDir, regionalDir, reviewerInitials, 
                   suitable=True):
    '''
    (string, string, [Boolean], string, string, string) -> changes to WHRdb, email 
                                                            sent to reviewer

    Changes status of model to "mosaicing complete" in WHRdb and notifies the
        reviwer that it is complete and ready for review.

    Arguments:
    strUC -- strUC for species that was mosaiced.
    initials -- Your initials.
    suitable -- True/False whether the mosaic is correct.
    mosaicDir -- Directory where the mosaic is saved.
    regionalDir -- Directory where the regional outputs are saved.
    reviewerInitials -- Used to send email to the reviwer about the species.

    Example:
    >>> VerifyMosaic_4("mSEWEx", "NMT", True, mosaicDir="P:/Proj3/Output/Mosaics/",
                       regionalDir="P:/Proj3/Output/Regional/", "MJR")
    '''
    # Change the model status to "mosaic complete"

    # Record initials in mosaicker field

    # If mosaic is bad, delete mosaic and regional models, revert to "editing started"

    # Email the reviewer to let them know that the species ready for review.
    
    # Email when done
    
    print("Step 4 -- No code yet")


def StartReview_5(strUC, initials):
    '''
    (string, string) -> changes to WHRdb

    Changes status of model to "review started" in WHRdb, records initials.

    Arguments:
    strUC -- strUC for species that was mosaiced.
    initials -- Your initials.
    
    Example:
    >>> StartReview_5("mSEWEx", "NMT")
    '''

    # Change the model status to "review started"

    # Email when done
    
    print("Step 5 -- No code yet")


def EndReview_6(strUC, initials, mosaicDir, regionalDir, modelerInitials, suitable=True, ):
    '''
    (string, string, [boolean], string, string, string) -> changes to WHRdb

    Changes status of model to "review complete" in WHRdb, records initials.

    Arguments:
    strUC -- strUC for species that was mosaiced.
    initials -- Your initials.
    suitable -- True/False whether the mosaic is correct.
    mosaicDir -- Directory where the mosaic is saved.
    regionalDir -- Directory where the regional outputs are saved.
    modelerInitial -- Initials of the person who edited the model
        
    Example:
    >>> EndReview_6("mSEWEx", "NMT", True, mosaicDir="P:/Proj3/Output/Mosaics/",
                    regionalDir="P:/Proj3/Output/Regional/", "MJR")
    '''

    # Change model status.

    # Record initials of reviewer.

    # If mosaic is bad, delete mosaic and regional models, revert to "editing started"

    # Email the reviewer to let them know that the species ready for review.
    
    # Email when done

    print("Step 6 -- No code yet")

def Publish_7(strUC, initials, regionalDir, mosaicDir, storageDir, outputDir):
    '''
    (string, string, string, string, string, string) -> multiple processes.

    Changes status of model to "publishing started" in WHRdb, records initials,
        and .......

    Arguments:
    strUC -- The path name of the file to publish.
    initials -- Your initials.
    regionalDir -- Directory with regional outputs.
    mosaicDir -- Directory where mosaiced output is saved.
    storageDir -- Directory for "deep storage".
    outputDir -- Directory of the "Null123" outputs.
    
    Example:
    >>> Publish_7("mSEWEx", "NMT", "T:/Output")
    '''

    # Change model status.

    # Record initials of reviewer.

    # Copy regional models to any long term storage if desired, then delete

    # Copy file to null123 directory

    # Create 0123 version

    # Create 01 season versions

    # Publish to ScienceBase with metadata.

    # Create web services?

    # Is reprojection required?

    # Update model version and archive model in a dictionary of model dictionaries

    # Update range map version and archive table.

    # Email when done

    print("Step 7 -- No code yet")
