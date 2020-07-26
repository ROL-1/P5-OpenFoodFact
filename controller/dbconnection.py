"""Class to filter(really?) api informations and transmit it to the database."""
"""pip install mysql-connector-python"""

import mysql.connector as MC

from controller.dbconfig import HOST,DATABASE,USER,PASSWORD

class DBconnect: 
    """Récupère les informations pour la connexion et créé la connexion."""

    def __init__(self):
        """Load parameters and call _connection()."""
        self.host = HOST
        self.database = DATABASE
        self.user = USER
        self.password = PASSWORD
        self._connection()

    def _connection(self):
        """Make connection to database."""
        try:
            self.cnx = MC.connect(host = self.host, database = self.database, user = self.user, password = self.password) # Gestion du password ??? ## database = self.database##
        except MC.Error as err :
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR: # .errno = return last error code
                print("Une information est erronée parmi votre nom d'utilisateur et votre mot de passe.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("La base de données n'existe pas.")
            else:
                print(err)
        return self.cnx

    def close_connection(self):
        """Close connection to database."""
        #cursor.close() #TC
        self.connection.close()