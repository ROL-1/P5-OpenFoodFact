""" class to filter(really?) api informations and transmit it to the database."""
"""pip install mysql-connector-python"""


    #products = cursor.fetchall()

    #for product in products :
        #...

    #fetchone, fetchall, fetchmany #To Clean

# except MC.Error as err :
    # if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    #     print("Something is wrong with your user name or password")
    # elif err.errno == errorcode.ER_BAD_DB_ERROR:
    #     print("Database does not exist")
    # else:
    #     print(err)

import mysql.connector as MC

from dbconfig import HOST,DATABASE,USER,PASSWORD

# class de connexion
class DBconnect : 
    """Récupère les informations pour la connexion et créé la connexion """

    def __init__(self):
        """Load parameters and call _connection()."""
        self.host = HOST
        self.database = DATABASE
        self.user = USER
        self.password = PASSWORD
        self._connection()

    def _connection(self):
        """Créé la connexion."""
        self.connection = MC.connect(host = self.host, database = self.database, user = self.user, password = self.password) # Gestion du password ???
        return self.connection

    def _close_connection(self):
        #cursor.close()
        self.connection.close()
