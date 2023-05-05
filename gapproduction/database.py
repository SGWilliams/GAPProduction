"""
This module facilitates common tasks for querying the GAP Species Database.
"""
import pyodbc, gapconfig


# Connection Function ---------------------------------------------------------
def ConnectDB(db : str, driver : str, server : str) -> tuple:
    '''
    Returns a cursor and connection within the specified database.
    For troubleshooting db = 'GapVert_48_2016'

    Parameters
    ----------
    db : Database to connect to (on CHUCK)
    driver : ODBC driver to use
    server : Server to connect to

    Returns
    -------
    cursor : Cursor object for the database
    con : Connection object for the database
    '''
    try:
        import pyodbc

        con = pyodbc.connect(driver=driver, server=server, 
                             trusted_connection='yes', database=db)
        
        print("-- Connected to " + db)

        return con.cursor(), con
    except Exception as e:
        print(e)


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


def __main():
    pass


if __name__ == '__main__':
    __main()