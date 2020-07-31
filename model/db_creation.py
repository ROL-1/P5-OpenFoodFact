"""Class to create database."""

from model.db_connection import Db_connect

class Db_create:
    """..."""

    def create_db(sql_readed, verbose):
        """Create database (drop if exists)."""       
        # Split the file to make requests list.
        SQLrequests = sql_readed.split(';')
        # Connexion to MySQL
        Log = Db_connect()
        # Drop database if exist
        with open('model/db_config.py','r') as file :
           for line in file:
               if 'DATABASE' in line:
                   DATABASE = line.split('= ')[1].replace("'","")  
        Log.execute("DROP DATABASE IF EXISTS {}".format(DATABASE))    
        Log.commit()
        # Count for strings skipped.
        i = 0
        # Execute requests from the list.
        if verbose:
            print('Executing requests to database.') 
        for request in SQLrequests:                   
            try:
                Log.execute(request)
            except:
                i+=1
                if verbose:
                    print("String skipped:'",request,"'")                
        # Save information
        Log.commit()
        # Disconnect from MySQL Server.
        Log.close_connection         
        # Print counter if asked
        if verbose: 
            print(i,'string(s) skipped.')