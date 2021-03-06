#! /usr/bin/env python3
# coding: utf-8
"""File to manage connection to database."""

import mysql.connector as MC

from model.json import Json
from mysql.connector import errorcode


class Connection:
    """Manage connection to database and contains functions to get datas."""

    compteur = 0

    def __init__(self, host, user, password, database=None):
        """Load parameters and call connection()."""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection()

    def database_log(self):
        """Look for database name for connection."""
        DATABASE = Json.read_database_name()
        Log = Connection(self.host, self.user, self.password, DATABASE)
        return Log

    def connection(self):
        """Make connection to database."""
        try:
            self.cnn = MC.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
        except MC.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print(
                    "Une information est erronée parmi votre nom d'utilisateur"
                    " et votre mot de passe."
                )
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("La base de données n'existe pas.")
                print(
                    "Veuillez relancer le programme avec la commande : "
                    "--install_database. (option : -v)"
                )
            else:
                print(err)
            return exit()
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
        self.cnn.commit()

    def close_connection(self):
        """Close connection to database."""
        self.cnn.close()
