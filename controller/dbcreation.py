"""Create Database."""

import argparse
from controller.dbconnection import DBconnect

# AJOUTER CONTROLER SUR ERREURS
# Extraire le nom de la database ?

class DBcreation:
    """Create database from .sql file."""
    
    def __init__(self, sql_file, verbose):
        """Launch create_db() and response for verbose."""
        if verbose:
            print("Running 'dbcreation.py'")
        self._create_db(sql_file,verbose)

    def _create_db(self, sql_file, verbose):
        """Create database from .sql file."""
        # Open and read file named by user.
        if verbose:
            print("Reading '{}'".format(sql_file))
        with open(sql_file, 'r') as read_sql:
            sqlFile = read_sql.read()
        # Split the file to make requests list.
        SQLrequests = sqlFile.split(';')
        # Connexion to MySQL
        Log = DBconnect()
        cursor = Log.cnx.cursor()
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
        Log.cnx.commit()
        # Disconnect from MySQL Server.
        Log.close_connection 
        print("Database created from '{}'".format(sql_file))
        # Print counter if asked
        if verbose:  
            print(i,'string(s) skipped.')
