"""
This module supports GAP habitat map production and management.
"""
from gapproduction import database, dictionaries, taxonomy

def ModelEVTs(modelCode : str, db : str, EVT_format : str = 'names') -> list:
    '''
    Returns two lists, the first of which contains the names of ecological
    systems that have been selected as primary habitat for the model, and
    the second of which contains those ecological systems selected as
    auxiliary habitat.

    Parameters
    ----------
    modelCode -- The 9-character GAP model code.
    EVT_format -- Specifies whether to return EVT names, codes, or both.
    db -- The name of the GAP database to query.

    Returns
    -------
    prim -- A list of primary ecological systems.
    aux -- A list of auxiliary ecological systems.
    '''
    try:
        # Connect to the desired model database
        cursor, WHRConnection = database.ConnectDB(db)

        if EVT_format == 'codes':
            # Query the primary map units
            sql = f"""SELECT t.intEVT_Code
                    FROM dbo.tblMapUnitDesc AS t 
                    INNER JOIN dbo.tblSppMapUnitPres AS s 
                    ON t.intEVT_Code = s.intEVT_Code
                    WHERE s.ysnPres='True' 
                    AND s.strSpeciesModelCode = '{modelCode}'"""
            prim = cursor.execute(sql).fetchall()

            # Query the auxiliary map units
            sql = f"""SELECT t.intEVT_Code
                    FROM dbo.tblMapUnitDesc AS t
                    INNER JOIN dbo.tblSppMapUnitPres AS s
                    ON t.intEVT_Code = s.intEVT_Code
                    WHERE s.ysnPresAuxiliary='True'
                    AND s.strSpeciesModelCode = '{modelCode}'"""
            aux = cursor.execute(sql).fetchall()

            # Process the lists to get the first item from each tuple
            prim = [i[0] for i in prim]
            aux = [i[0] for i in aux]

        elif EVT_format == 'names':
            # Query the primary map units
            sql = f"""SELECT t.strEVT_Name
                    FROM dbo.tblMapUnitDesc AS t 
                    INNER JOIN dbo.tblSppMapUnitPres AS s 
                    ON t.intEVT_Code = s.intEVT_Code
                    WHERE s.ysnPres='True' 
                    AND s.strSpeciesModelCode = '{modelCode}'"""
            prim = cursor.execute(sql).fetchall()

            # Query the auxiliary map units
            sql = f"""SELECT t.strEVT_Name
                    FROM dbo.tblMapUnitDesc AS t
                    INNER JOIN dbo.tblSppMapUnitPres AS s
                    ON t.intEVT_Code = s.intEVT_Code
                    WHERE s.ysnPresAuxiliary='True'
                    AND s.strSpeciesModelCode = '{modelCode}'"""
            aux = cursor.execute(sql).fetchall()

            # Process the lists to get the first item from each tuple,to remove
            # trailing/leading spaces, and to sort alphabetically
            prim = [str(i[0].strip()) for i in prim]
            prim.sort()
            aux = [str(i[0].strip()) for i in aux]
            aux.sort()

        elif EVT_format == 'both':
            # Query the primary map units
            sql = f"""SELECT t.intEVT_Code, t.strEVT_Name
                    FROM dbo.tblMapUnitDesc AS t 
                    INNER JOIN dbo.tblSppMapUnitPres AS s 
                    ON t.intEVT_Code = s.intEVT_Code
                    WHERE s.ysnPres='True' 
                    AND s.strSpeciesModelCode = '{modelCode}'"""
            prim = cursor.execute(sql).fetchall()

            # Query the auxiliary map units
            sql = f"""SELECT t.intEVT_Code, t.strEVT_Name
                    FROM dbo.tblMapUnitDesc AS t
                    INNER JOIN dbo.tblSppMapUnitPres AS s
                    ON t.intEVT_Code = s.intEVT_Code
                    WHERE s.ysnPresAuxiliary='True'
                    AND s.strSpeciesModelCode = '{modelCode}'"""
            aux = cursor.execute(sql).fetchall()

        # Delete the WHRdb cursor and close the connection
        cursor.close()
        WHRConnection.close()

        # Return the lists of primary and auxiliary map units
        return prim, aux

    except Exception as e:
        print(e)
        return False, False


def ModelAsDictionary(model : str, db : str) -> dict:
    '''
    Returns a dictionary that includes a key for each of a regional model's 
    variables.

    Parameters
    ----------
    model : A region-season model code.
    db : The name of the GAP database to query (e.g., "GAPVert_48_2016").

    Returns
    -------
    modelDict : A dictionary with keys for each of the model's variables. Keys
        are:
    Dictionary keys -- ['intIntoBuffFW', 'ScientificName', 'ysnHydroWV', 'intAuxBuff',
                        'strForIntBuffer', 'ysnHandModel', 'intIntoBuffOW', 'Season',
                        'intElevMax', 'PrimEVTs', 'AuxEVTs', 'SpeciesCode',
                        'intIntoBuffWV', 'cbxContPatch', 'ysnUrbanExclude', 'intFromBuffFW',
                        'intElevMin', 'ysnHydroOW', 'Region', 'CommonName',
                        'ysnUrbanInclude', 'strUseForInt', 'intEdgeEcoWidth',
                        'intFromBuffWV', 'strStreamVel', 'strSalinity', 'strEdgeType',
                        'ysnHydroFW', 'intContPatchSize', 'strAvoid', 'intFromBuffOW',
                        'memHMNotes']

    Example:
    modelDictionary = ModelAsDictionary(model="mSEWEx-y1", EVT_format="both")

    N. Tarr 3/20/2025
    '''
    # SETUP -------------------------------------------------------------------
    # Connect to the desired model database
    cursor, connection = database.ConnectDB(db)

    # Create a function to retrieve the desired ancillary variables
    def __getVariable(model, variable):
        sql = f"""SELECT anc.{variable}
                FROM dbo.tblModelAncillary as anc
                WHERE anc.strSpeciesModelCode = '{model}'"""
        var = cursor.execute(sql).fetchall()
        var = var[0][0]
        return var

    # BUILD DICTIONARY --------------------------------------------------------
    # Initialize dictionary
    modelDict = {}

    # Region and season
    region = dictionaries.regionsDict_Num_To_Name[int(model[8])]
    modelDict["Region"] = region

    season = model[7]
    modelDict["Season"] = season
                                                    
    # Species names
    species_code = model[:6]
    modelDict["SpeciesCode"] = species_code
    taxon_info = taxonomy.GetTaxonInfo(db=db, species_code=species_code)
    modelDict["CommonName"] = taxon_info["common_name"]
    modelDict["ScientificName"] = taxon_info["scientific_name"]
    if len(str.split(taxon_info["scientific_name"], " ")) == 3:
        modelDict["SubspeciesName"] = str.split(taxon_info["scientific_name"], 
                                                " ")[2]
    else:
        modelDict["SubspeciesName"] = None

    # # Who worked on the model
    # modelDict["Modeler"] = gapdb.Who(SpeciesCode, action="edited_model")
    # modelDict["Reviewer"] = gapdb.Who(SpeciesCode, action="reviewed_model")

    # Land Cover Associations
    PrimEVTs, AuxEVTs = ModelEVTs(modelCode=model, db=db,
                                EVT_format="both")
    modelDict["PrimEVTs"] =[PrimEVTs][0]
    modelDict["AuxEVTs"] =[AuxEVTs][0]

    # Hand Model
    ysnHandModel = __getVariable(model, "ysnHandModel")
    modelDict["ysnHandModel"] = ysnHandModel

    # Hand Model Comments
    #memHandModelNotes = __getVariable(model, "memHMNotes")
    #modelDict["memHandModelNotes"] = memHandModelNotes

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