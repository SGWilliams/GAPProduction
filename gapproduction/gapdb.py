"""
This module facilitates common tasks for querying the GAP Species Databases
and WHRdb.
"""
import pyodbc, gapconfig
from dictionaries import stateDict_To_Abbr, taxaDict


def ConnectToDB(connectionStr):
    '''
    (str) -> cursor, connection

    Provides a cursor within and a connection to the database

    Argument:
    connectionStr -- The SQL Server compatible connection string for connecting
        to a database

    Example:
    >>> conString = """DRIVER=SQL Server Native Client 11.0;
                   SERVER={0};
                   UID={1};
                   PWD={2};
                   DATABASE=WHRdB;"""
    >>> cursor, connection = ConnectToDB(conString)

    '''
    try:
        con = pyodbc.connect(connectionStr)        
    except:
        connectionStr = connectionStr.replace('11.0', '10.0')
        con = pyodbc.connect(connectionStr)

    return con.cursor(), con 


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