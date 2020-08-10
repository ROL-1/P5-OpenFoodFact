"""Class to create database."""

from model.connection import Connection

class Create:
    """Create database."""
    def __init__(self, Log, sql_readed):
        self.Log = Log
        # Split the file to make requests list.
        self.SQLrequests = sql_readed.split(';')

    def create_db(self, verbose):
        """Create database (drop if exists)."""       
        with open('model/config.py','r') as file :
           for line in file:
               if 'DATABASE' in line:
                   DATABASE = line.split('= ')[1].replace("'","")  
        # Drop database if exist
        self.Log.execute("DROP DATABASE IF EXISTS {}".format(DATABASE))    
        self.Log.commit()
        # Count for strings skipped.
        i = 0
        # Execute requests from the list.
        if verbose:
            print('Executing requests to database.') 
        for request in self.SQLrequests:                   
            try:
                self.Log.execute(request)
            except:
                i+=1
                if verbose:
                    print("String skipped:'",request,"'")                
        # Save information
        self.Log.commit()
        # Disconnect from MySQL Server.
        self.Log.close_connection         
        # Print counter if asked
        if verbose: 
            print(i,'string(s) skipped.')