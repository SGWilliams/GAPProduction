"""
This module facilitates common tasks for querying the GAP Species Database.
"""
from gapconfig import server, driver
print("SERVER:  ",server)
print("DRIVER:  ",driver)

# Connection Function ---------------------------------------------------------
def ConnectDB(db : str, 
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
        print("-- Connected to " + db)
        return con.cursor(), con
    except Exception as e:
        print(e)


def __main():
    pass

if __name__ == '__main__':
    __main()