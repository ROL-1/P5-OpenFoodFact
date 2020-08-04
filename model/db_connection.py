"""Class to filter(really?) api informations and transmit it to the database."""
"""pip install mysql-connector-python"""

import mysql.connector as MC
from mysql.connector import errorcode

from model.db_config import HOST,USER,PASSWORD

class Db_connect: 
    """Récupère les informations pour la connexion et créé la connexion."""

    compteur = 0
    def __init__(self, database = None):
        """Load parameters and call connection()."""
        host = HOST
        user = USER
        password = PASSWORD  
        self._connection(host, user, password, database)

    def database_log(self):
        """Look for database name for connection."""
        with open('model/db_config.py','r') as file:
           for line in file:
               if 'DATABASE' in line:
                   DATABASE = line.split('= ')[1].replace("'","")  
        Log = Db_connect(DATABASE)
        return Log

    def _connection(self, host, user, password, database):
        """Make connection to database."""               
        try:                     
            self.cnn = MC.connect(
                host = host,                
                user = user,
                password = password,
                database = database,
                )
        except MC.Error as err :
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Une information est erronée parmi votre nom d'utilisateur et votre mot de passe.")
                return 1 #TC               
            elif err.errno == errorcode.ER_BAD_DB_ERROR:                 
                print("La base de données n'existe pas.")
                return 2 #TC              
            else:
                print(err)                
                return 3 #TC
        return self.cnn

    def execute(self, request, value=None):
        """Execute request (open and close the cursor, no return)."""
        cursor = self.cnn.cursor()
        cursor.execute(request, value)
        cursor.close()

    def request(self, request, value=None):
        """Return request after open and close the cursor."""
        cursor = self.cnn.cursor()
        cursor.execute(request, value)
        result = cursor.fetchall()
        cursor.close()
        return result

    def commit(self):
        """Commit to the database."""
        commit = self.cnn.commit()

    def close_connection(self):
        """Close connection to database."""
        #cursor.close() #TC
        self.connection.close()