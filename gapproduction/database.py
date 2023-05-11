"""
This module facilitates common tasks for querying the GAP Species Database.
"""
from gapconfig import server, driver

# Connection Function ---------------------------------------------------------
def ConnectDB_pyodbc(db : str, 
              driver : str = driver, 
              server : str = server) -> tuple:
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
    connection : Connection object for the database
    '''
    try:
        import pyodbc
        con = pyodbc.connect(driver=driver, server=server, 
                             trusted_connection='yes', database=db)
        return con.cursor(), con
    except Exception as e:
        print(e)


# ConnectDB function, but using SQLAlchemy instead of pyodbc ------------------
def ConnectDB(db : str, driver : str = driver, server : str = server) -> tuple:
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
    connection : Connection object for the database
    '''
    try:
        from sqlalchemy import create_engine
        engine = create_engine('mssql+pyodbc://' + server + '/' + db + '?driver=' + driver)
        con = engine.connect()
        cursor = con.connection.cursor()
        return cursor, con
    except Exception as e:
        print(e)


# -----------------------------------------------------------------------------
def __main():
    pass

if __name__ == '__main__':
    __main()