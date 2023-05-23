"""
This module facilitates management and addition of citations to the GAP
databases.
"""
from gapproduction import database
import pandas as pd
pd.options.display.max_colwidth = 1000
import re

# Function to check if a reference already exists -----------------------------
def CitationExists(citation : str, db : str) -> (bool, pd.DataFrame):
    '''
    Looks for a citation in the database.  Matches would unlikely be exact, so
    the function uses wildcards to match the citation to the database and 
    prints protential matches.

    Parameters
    ----------
    citation : A string containing the reference information.
    db : A string containing the name of the database to query.

    Returns
    -------
    exists : A boolean indicating whether the citation already exists.
    matches : A dataframe of potential matches.
    '''
    # Connect to database
    cursor, connection = database.ConnectDB(db)

    print("Your reference: \n" + citation + "\n")
    # Use regex to find the year in the reference
    full_year = re.findall(r'\d{4}', citation)[0]
    YY = full_year[-2:]

    # Get the first 3 characters of the reference
    auth = citation[:3]

    # Build a wildcard string to find potential matches knowning that similar
    # citations would start with auth and contain YY followed by a period.
    wc = auth + '%' + full_year + '.' + '%'

    # Query the database for similar citations
    sql = """SELECT * FROM dbo.tblCitations WHERE memCitation LIKE ?;"""
    matches = pd.read_sql(sql, connection, params=[wc])

    # If there are no matches, the citation is new
    if matches.empty:
        exists = False
        print("The citation probably doesn't exist in the database")
        return exists, matches
    else:
        exists = True
        print("The reference provided may already be in the database.  The following matched:")
        print(matches)
        return exists, matches
    
# Function to check if a reference code is available --------------------------
def Availability(reference_code : str, db : str) -> bool:
    '''
    Check if a reference code is available for use.

    Parameters
    ----------
    reference_code : A string containing the reference code.
    database : A string containing the name of the database to query.

    Returns
    -------
    free : A boolean indicating whether the reference code is available.

    '''
    # Does a code already exist that starts with the unique core of the code?
    # Connect to database
    cursor, connection = database.ConnectDB(db)

    # Get the unique core of the code
    code_core = reference_code[:8]

    # Query the database for any codes that start with the code_core
    sql = """SELECT * FROM dbo.tblCitations WHERE strRefCode LIKE ?;"""
    matches = pd.read_sql(sql, connection, params=[code_core + '%'])

    # If there are no matches, the code is free
    if matches.empty:
        free = True
        return free
    else:
        free = False
        print("The reference code provided is already in use: " + reference_code)
        print(matches)
        return free

# Function to make a reference code -------------------------------------------
def BuildStrRefCode(reference : str, reference_type : str,
                     db : str) -> str:
    '''
    Build a reference code (strRefCode) from a reference string.

    The reference code format is 
    X YY ZZZ ## USGP

    X - Reference Type
        A = journal article (primary literature)
        B = book/monograph (primary literature)
        N = non-refereed article (thesis, note)
        O = official document
        P = personal communication
        R = report
        U = unknown
        W = Website

    YY - Year

    ZZZ - First 3 characters of primary author's last name.

    ## - Sequential number of publication for that author in that year.

    USGP - Source of reference (new ones are always USGP).

    Parameters
    ----------
    reference_type : A string containing the reference information.
    type : A string (letter) indicating the type of reference. See above.
    db : A string containing the name of the database to query.

    Returns
    -------
    reference_code : A string containing the reference code.

    '''
    # Local function to increment the sequence number into a new code
    def __seq(reference_code):
        '''
        Changes a reference code by incrementing the sequence number.
        '''
        # Get the current sequence number
        seq = reference_code[6:8]

        # Increment the sequence number
        seq = str(int(seq) + 1)

        # Pad the sequence number with a leading zero if needed
        if len(seq) == 1:
            seq = '0' + seq

        # Replace the sequence number in the reference code
        reference_code = reference_code[:6] + seq + reference_code[8:]
        return reference_code  

    seq = '01'
    source = 'USGP'

    # Get the author characters
    ZZZ = reference.split()[0][:3].upper()

    # Use regex to find the year in the reference
    YY = re.findall(r'\d{4}', reference)[0][-2:]

    # Identify what a new code would be
    reference_code = reference_type + YY + ZZZ + seq + source

    # See if the code is available
    free = Availability(reference_code, db)

    # If free, return code
    if free:
        return reference_code

    if not free:
        # Use a while statement to increment the sequence number until a free
        #   code is found
        i = 0
        while not free:
            # Increment the sequence number
            reference_code = __seq(reference_code)

            # Check if the code is free
            free = Availability(reference_code, db)

            # Break if too many iterations
            i += 1
            if i > 10:
                print("Too many iterations")
                break

    # Return the free code
    print("Reference code was taken, changed to " + reference_code)
    return reference_code

# Function to add a reference to the database ---------------------------------
def AddReference(reference : str, reference_code : str, db : str) -> None:
    '''
    Add a reference to the database if the reference code doesn't exit.

    Parameters
    ----------
    reference : A string containing the reference information.
    reference_code : A string containing the reference code.
    db : A string containing the name of the database to query.

    Returns
    -------
    None
    '''
    # Connect to database
    cursor, connection = database.ConnectDB(db)

    # SQL to add if not exists
    sql = """INSERT INTO dbo.tblCitations (strRefCode, memCitation)
             SELECT ?, ? WHERE NOT EXISTS 
                    (SELECT * FROM dbo.tblCitations WHERE strRefCode = ?);"""

    # Execute the query
    connection.execute(sql, reference_code, reference, reference_code)

    # Commit the changes
    #connection.commit()

    # Print a message
    print(f"{reference_code} added to database: \n" + reference)

    return None 


# -----------------------------------------------------------------------------
def __main():
    pass

if __name__ == '__main__':
    __main()