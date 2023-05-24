"""
This module supports GAP range map production and management.
"""
import pandas as pd

def V2As2016(v2_database : str) -> pd.DataFrame:
    '''
    Reads the simple results table from a range output database and creates a
    GAP database style range table with columns "intGAPPres" and "intGAPSeas" that
    has a 1 in intGAPPres where presence_2015v2 is 1.  intGAPSeas gets value of 1, 3, 
    or 4 where 1 = year_round, 3 = winter, and 4 = summer.  All other values are
    NULL, but NULLs are converted to 7 ('UNKNOWN') where intGAPPres is 1.

    Additional steps are needed to insert the output dataframe into the 2016 
    database: this function does not write to the GAP databases.

    Parameters
    ----------
    v2_database : A string containing the name of the database to query.

    Returns
    -------
    df2 : A dataframe with columns "strHUC12RNG", "intGAPPres", and "intGAPSeas".

    N. Tarr 5/24/2023
    '''
    import sqlite3
    import pandas as pd

    year = "2015"

    # Connect to the database
    conn = sqlite3.connect(v2_database)

    # Read in simple results as a dataframe, strHUC12RNG as a string
    sql = """SELECT * FROM simplified_results;"""
    df = pd.read_sql(sql, conn).astype({"strHUC12RNG": "object"})

    # Set the df index to strHU12RNG
    df.set_index("strHUC12RNG", inplace=True)

    # Create a new dataframe with the same index as df and columns for 
    # intGAPPres and intGAPSeas
    df2 = pd.DataFrame(index=df.index, columns=["intGAPPres", "intGAPSeas"])

    # Set intGAPPres to 1 where presence_2015 is 1
    df2.loc[df["presence_2015v2"] == 1, "intGAPPres"] = 1

    # Find which seasons are represented in the simplified results table
    seasons = [col for col in df.columns if "presence" not in col]
    seasons = [col for col in seasons if "strHUC12RNG" not in col]
    seasons = tuple(set([x[:-7] for x in seasons]))

    # If year_round is represented, set intGAPSeas to 1 where year_round is 1
    if "year_round" in seasons:
        df2.loc[df["year_round_2015v2"] == 1, "intGAPSeas"] = 1

    # If a strHUC12RNG value has a 1 in both summer and winter, set intGAPSeas to 1
    if "summer" in seasons and "winter" in seasons:
        df2.loc[(df["summer_2015v2"] == 1) & (df["winter_2015v2"] == 1), 
                "intGAPSeas"] = 1
        
    # If a strHUC12RNG value has a 1 in summer but not winter, set intGAPSeas to 4
    if "summer" in seasons and "winter" in seasons:
        df2.loc[(df["summer_2015v2"] == 1) & (df["winter_2015v2"] != 1), 
                "intGAPSeas"] = 4
        
    # If a strHUC12RNG value has a 1 in winter but not summer, set intGAPSeas to 3
    if "summer" in seasons and "winter" in seasons:
        df2.loc[(df["summer_2015v2"] != 1) & (df["winter_2015v2"] == 1), 
                "intGAPSeas"] = 3

    # Set intGAPSeas to 7 where intGAPPres is 1 and intGAPSeas is NULL
    df2.loc[(df2["intGAPPres"] == 1) & (df2["intGAPSeas"].isnull()),
            "intGAPSeas"] = 7
    
    # Drop rows where everything is NULL
    df2.dropna(how="all", inplace=True)

    # Reset the index so that strHUC12RNG is a column
    df2.reset_index(inplace=True)

    # Close the database connection
    conn.close()

    return df2


# -----------------------------------------------------------------------------
def __main():
    pass

if __name__ == '__main__':
    __main()