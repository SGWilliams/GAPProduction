"""
This module facilitates common tasks for querying the GAP species taxonomies.
"""
from gapproduction import database

# Get a complete list of valid species codes.
def AllSpeciesList(db : str = "GAPVert_48_2016") -> list:
    '''
    Returns a list of valid species; ysnIncludeSpp = 0 are excluded.
    
    Parameters
    ----------
    db -- The database name.
    
    Returns
    -------
    species_list -- A list of species-region models.
    '''
    # Connect to the GAP database
    cursor, connection = database.ConnectDB(db)

    # Query the primary map units
    sql = f"""SELECT strUC FROM tblTaxa
              WHERE ysnIncludeSpp = 1;"""
    species_list = cursor.execute(sql).fetchall()

    # Convert tuple items into a list of dictionaries
    species_list = [x[0] for x in species_list]

    return species_list


# Get taxonomic information from the GAP database
def GetTaxonInfo(db : str, species_code : str = None, 
                 scientific_name : str = None, 
                 common_name : str = None) -> dict:
    '''
    Returns a dictionary of : GAP species code, full scientific name, 
    common name, and ITIS TSN.  The function will try to lookup the species
    by GAP species code, then scientific name, then common name.

    Parameters
    ----------
    db -- the name of the GAP database to query.
    species_code -- the species' unique GAP ID.
    scientific_name -- the species' full scientific name.
    common_name -- the species' common name.

    Returns
    -------
    taxon_dict -- a dictionary of the species' taxonomic information.

    Example:
    >>> Taxonomy("bHOFIx", "GapVert_48_2030")
    {'gap_code': 'bHOFIx', 'common_name': 'House Finch', 
    'scientific_name': 'Carpodacus mexicanus', 'ITIS_TSN': 179191}
    '''
    try:
        import pandas as pd
        from gapproduction import database, strings

        # Connect to GAP database
        cursor, connection = database.ConnectDB(db)
        
        # Try lookup with species code
        if species_code is not None:

            # Check that the species code is capitalized correctly
            species_code = strings.GapCase(species_code)

            # Query the species databsae to return dataframe of taxonomic info
            sql = """SELECT * FROM dbo.tblTaxa WHERE strUC = ?;"""
            df = pd.read_sql(sql, connection, params=[species_code])
            connection.close()

        # Or try to lookup with scientific name
        elif scientific_name is not None:
            # Query the species databsae to return dataframe of taxonomic info
            sql = """SELECT * FROM dbo.tblTaxa WHERE strSciName = ?;"""
            df = pd.read_sql(sql, connection, params=[scientific_name])
            connection.close()
        
        # Else try to lookup with common name
        elif common_name is not None:
            # Query the species databsae to return dataframe of taxonomic info
            sql = """SELECT * FROM dbo.tblTaxa WHERE strComName = ?;"""
            df = pd.read_sql(sql, connection, params=[common_name])
            connection.close()

        taxon_dict = {}
        taxon_dict['GAP_SppCode'] = df.loc[0,'strUC']
        taxon_dict['GAP_ComName'] = df.loc[0,'strComName']
        taxon_dict['GAP_SciName'] = df.loc[0,'strSciName']
        
        taxon_dict['ITIS_TSN'] = df.loc[0,'intITIScode']
        taxon_dict['ITIS_SciName'] = df.loc[0,'strITIS_SciName']
        taxon_dict['ITIS_ComName'] = df.loc[0,'strITIS_ComName']

        taxon_dict['GAP_ITIS_Match'] = df.loc[0,'strGapITISmatch']

        taxon_dict['NatureServe_GlobalID'] = df.loc[0,'intNSglobal']
        taxon_dict['NatureServe_SciName'] = df.loc[0,'strNS_SciName']
        taxon_dict['NatureServe_ComName'] = df.loc[0,'strNS_ComName']

        taxon_dict['GAP_NatureServe_Match'] = df.loc[0,'strGapNSmatch']

        taxon_dict['GBIF_Key'] = df.loc[0,'intGBIFkey']
        taxon_dict['GBIF_SciName'] = df.loc[0,'strGBIF_SciName']
        taxon_dict['GAP_GBIF_Match'] = df.loc[0,'strGapGBIFmatch']

        taxon_dict['database'] = db

        return taxon_dict

    except Exception as e:
        print(e)


# -----------------------------------------------------------------------------
def __main():
    pass

if __name__ == '__main__':
    __main()