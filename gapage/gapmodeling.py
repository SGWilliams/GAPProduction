## Module to query/manipulate model parameters within the WHRdb.
##
## Public Functions:
##
## ModelExists() -- Returns a boolean, indicating whether the passed string is
##      a valid, existing GAP model code.
##
## ModelCodes() -- Get a tuple of included model codes for the species.
##
## ModelEcoSystems() -- Returns lists of the selected primary and auxiliary
##      map units for the model.
##
## SpEcoSystems() -- Returns lists of primary and auxiliary map units that are
##      selected within any models for the given species.
##
## SpMuDiscrepancies() -- Returns a list of ecological systems that are selected
##      inconsistently among models (for regions within which each given system
##      occurs).
##
## ModelMuDiscrepancies() -- Identifies specific inconsistencies in the map unit
##      selection between the two input models.
##
## ResolveMuDiscrepancies() -- Resolves inconsistencies in the map unit
##      selection between the two input models by setting the change model to
##      match the selections of the template model. Note: This function is not
##      only intended to address regional differences for a given taxon, but
##      could also be used to address differences within a region between
##      subspecies or between other similar models.
##
## SetMUs() -- Selects the passed map units for the given model.
##
## HandModels() -- Returns a list of model codes for models that must be
##      modeled by hand.
##
## EcoSystemModels() -- Returns a list of models with primary assocation with the
##      ecological system and also a list of models with a secondary association.
##
## EcoSystemSpecies() -- Returns a list of species with a primary association with
##      the ecological system and another list of species with secondary assocations
##
## RemoveAlienMUs() -- Goes through each model in a list and unselects primary
##     and auxiliary map units which are not found within the model's region.
##
## ExcludeModels() -- Returns a list of models that exist in the WHRDb but are designated
##      for exclusion in the ysnInclude field.

import gapdb

#######################################
##### Function to get a tuple of "exclude models".
def ExcludeModels():
    '''
    (None) -> tuple

    Retrieves tuple of models that are designated for exclusion in tblAllSpecies.ysnInclude in the 
    WHRDb.
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


try:
    import arcpy
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
        prim, aux = gapdb.ModelEcoSystems(model)

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



#######################################
##### Function to get a list of all included, valid region models for a species
def ModelCodes(spCode, season='all', contiguousOnly=False):
    '''
    (string, string, [boolean]) -> tuple

    Retrieves list of models for the given species. Only includes models
    for which ysnInclude is True; omits models with region code 0

    Arguments:
    spCode -- The species' unique GAP ID
    season -- The season for which you wish to return models. By default, all
        seasons will be retrieved. You may enter: 's' or 'summer' for summer
        models; 'w' or 'winter' for winter models; 'y', 'year', 'yearround', or
        'year-round' for year-round models.
    contiguousOnly -- An optional, boolean parameter, indicating whether you
        wish to return codes only for models within the contiguous U.S. By
        default, it is set to False, which means that all model codes will be
        returned, regardless of their region.

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
    # Execute the query to select model codes that match the passed species code
    models = whrCursor.execute("""SELECT strSpeciesModelCode
                            FROM dbo.tblAllSpecies
                            WHERE strUC LIKE ?
                            AND ysnInclude = 'True'
                            AND strSpeciesModelCode NOT LIKE '%0'
                            """, spCode + '%').fetchall()

    # Delete the cursor
    del whrCursor
    # Close the database connection
    whrCon.close()

    # Create a list of all the matching models
    mcs = [str(item[0]) for item in models]

    # If the user only wishes to return models from the contiguous U.S....
    if contiguousOnly:
        # Select only those models with region codes less than 7
        mcs = [i for i in mcs if int(i[-1]) < 7]

    # Filter by the passed season
    season = season.lower()
    if season != 'all':
        if season == 's' or season == 'summer':
            mcs = [i for i in mcs if i[-2] == 's']
        elif season == 'w' or season == 'winter':
            mcs = [i for i in mcs if i[-2] == 'w']
        elif season == 'y' or season == 'year-round' or season == 'yearround' or season == 'year':
            mcs = [i for i in mcs if i[-2] == 'y']

    # Return the list of matching model codes
    return mcs


#######################################
##### Function to get a list of all included, valid region models for a species
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


#######################################
##### Get a list of the ecological systems that are selected in the WHRdb for
##### the passed model code
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


#######################################
##### Get a list of the ecological systems that are selected in the WHRdb for
##### any models that match the passed species code
def SpEcoSystems(spCode, season='all', contiguousOnly=False):
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
    '''
    try:
        # Get the model codes that match the passed species code
        models = ModelCodes(spCode, season, contiguousOnly)
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


## List the map units with inconsistent selection among models
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
