"""Class to create database."""

from controller.dbconnection import DBconnect
from controller.dbname import DATABASE

class DBcreate:
    """..."""

    def __init__(self, sql_readed, verbose):        
        """..."""

    def create_db(self, sql_readed, verbose):
        """Create database (drop if exists)."""       
        # Split the file to make requests list.
        SQLrequests = sql_readed.split(';')
        # Connexion to MySQL
        Log = DBconnect()
        cursor = Log.cnn.cursor()

        # Drop database if exist
        ("DROP DATABASE IF EXISTS {}".format(DATABASE))    
        Log.cnn.commit()
        # Count for strings skipped.
        i = 0
        # Execute requests from the list.
        if verbose:
            print('Executing requests to database.') 
        for request in SQLrequests:                   
            try:
                cursor.execute(request)
            except:
                i+=1
                if verbose:
                    print("String skipped:'",request,"'")                
        # Save information
        Log.cnn.commit()
        # Disconnect from MySQL Server.
        Log.close_connection         
        # Print counter if asked
        if verbose: 
            print(i,'string(s) skipped.')