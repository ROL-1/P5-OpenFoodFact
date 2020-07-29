"""Class to filter(really?) api informations and transmit it to the database."""
"""pip install mysql-connector-python"""

import mysql.connector as MC
from mysql.connector import errorcode

from model.db_config import HOST,USER,PASSWORD
from model.db_name import DATABASE

class Db_connect: 
    """Récupère les informations pour la connexion et créé la connexion."""

    def __init__(self):
        """Load parameters and call connection()."""
        self.host = HOST
        self.user = USER
        self.password = PASSWORD
        self.database = DATABASE
        self._connection()


    def _connection(self):
        """Make connection to database."""        
        try:
            self.cnn = MC.connect(
                host = self.host,                
                user = self.user,
                database = self.database,
                password = self.password
                )
        except MC.Error as err :
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR: # .errno = return last error code
                print("Une information est erronée parmi votre nom d'utilisateur et votre mot de passe.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("La base de données n'existe pas.")
            else:
                print(err)
        return self.cnn

    def request(self, request):
        """Return request after open and close the cursor."""
        cursor = self.cnn.cursor()
        cursor.execute(request)
        result = cursor.fetchall()
        cursor.close()
        return result

    def commit(self):
        """Commit to the database."""
        commit = self.connection.commit()

    def close_connection(self):
        """Close connection to database."""
        #cursor.close() #TC
        self.connection.close()