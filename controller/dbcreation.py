""" Create Database """
# avec DBOFF1.sql
# optionnel ?
# indications dans le readme
# commande : SOURCE <adresse du fichier>\DBOFF1.sql

import argparse
from dbconnection import DBconnect

class DBcreation:
    """Create database from .sql file."""
    
    def __init__(self, sql_file):
        """Add parameter for output verbosity."""
        parser = argparse.ArgumentParser(description="Create database from .sql file.")
        parser.add_argument("-v", "--verbose", action="store_true", help="add output verbosity")
        self.args = parser.parse_args()
        if self.args.verbose:
            print("Running '{}'".format(__file__))
        self._create_db(sql_file)


    def _create_db(self, sql_file):
        """Create database from .sql file."""
        # Open and read file named by user.
        with open(sql_file, 'r') as read_sql:
            sqlFile = read_sql.read()

        # Split the file to make requests list.
        SQLrequests = sqlFile.split(';')
        # Connexion to MySQL
        Log = DBconnect()
        cursor = Log.cnx.cursor()
        # Count for errors
        i = 0
        # Execute requests from the list.
        for request in SQLrequests:        
            try:
                cursor.execute(request)
            except:
                i+=1
                if self.args.verbose:
                    print('Skipped:',request)
                
        # Save information
        Log.cnx.commit()
        print('Database created from',sql_file)
        # Print counter if asked
        if self.args.verbose: 
            print(i,'line(s) skipped.')

TESTcreate = DBcreation('DBOFF1.sql')