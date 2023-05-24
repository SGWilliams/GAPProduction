"""
This module supports GAP range map production and management.
"""
import pandas as pd

def V2FortblRanges(v2_database : str) -> pd.DataFrame:
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

    # Add a column for strUC
    gap_id = conn.execute("SELECT species_id FROM compilation_info;").fetchone()[0]
    df2["strUC"] = gap_id

    # Add a column for strCompSrc
    who = conn.execute("SELECT who_ran FROM compilation_info;").fetchone()[0]
    initials = "".join([x[0] for x in who.split()])
    df2["strCompSrc"] = f"USGAP ({initials})"

    # Close the database connection
    conn.close()

    return df2[["strUC", "strHUC12RNG", "intGAPPres", "intGAPSeas", 
                "strCompSrc"]] 


def V2FortblRangeEdit(db : str) -> pd.DataFrame:
    """
    Reads the compilation info table from a range output database and 
    creates a dataframe that can be used to document the origin of changes
    to the 2016 range database (tblRangeEdit).

    Parameters
    ----------
    db : A string containing the name of the database to query.

    Returns
    -------
    df : A dataframe with columns "strUC", "strEditor", "dtmEditDate", 
        "memEditSource", "memEditComments"

    N. Tarr 5/24/2023
    """
    import sqlite3
    import pandas as pd
    from datetime import datetime

    # Connect to the database
    conn = sqlite3.connect(db)

    # Read in the compilation info table as a dataframe
    sql = """SELECT * FROM compilation_info;"""
    df = pd.read_sql(sql, conn)

    # Pull out only the columns we want
    df = df[["species_id", "notes", "who_ran"]]

    # Reformat the dataframe to match GAP database naming conventions
    df.rename(columns={"species_id": "strUC", 
                       "notes": "memEditComments", 
                       "who_ran": "strEditor", 
                       }, inplace=True)

    # Add a column with the database name
    df["memEditSource"] = db

    # Add a date column
    df["dtmEditDate"] = datetime.now().strftime("%Y-%m-%d")

    # Return the dataframe
    return df[["strUC", "strEditor", "dtmEditDate", "memEditSource",
               "memEditComments"]]


# -----------------------------------------------------------------------------
def __main():
    pass

if __name__ == '__main__':
    __main()