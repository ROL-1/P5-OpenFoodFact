"""Insert data in data base. From JSON."""

import json

from dbconnection import DBconnect
from api_config import FIELDS



class DBinsert:
    """Insert data in data base. From JSON."""

    # Ouvre le json : dans le __init__ ?
    def __init__ (self):
        """ ... """
        with open("scraped_file.json", "r") as read_file:
            data = json.load(read_file)
            print(data['products'][1]['code'])            

        # Connexion MySQL
        Log = DBconnect() #TC   
        cursor = Log.cnx.cursor()#TC 

        # Créer une fonction par type d'ajout // filtrages ?     

        # fonction insertion des données
        add_brand = ("INSERT INTO brands (brands_name) VALUES (%s)")
        data_brand = (data['products'][2]['brands'],) #requette pour ajouter une marque test

        # action insérer une nouvelle marque
        cursor.execute(add_brand,data_brand)
        

        # Make sure data is committed to the database
        Log.cnx.commit() #Enregistre l'information

        DBconnect.close_connection #TC
        # self.connect = DBconnect() #TC 

A = DBinsert() #TC
#https://pynative.com/python-cursor-fetchall-fetchmany-fetchone-to-read-rows-from-table/
#products = cursor.fetchall()

# cursor.fetchall() fetches all the rows of a query result. It returns all the rows as a list of tuples. An empty list is returned if there is no record to fetch.

# cursor.fetchmany(size) returns the number of rows specified by size argument. When called repeatedly this method fetches the next set of rows of a query result and returns a list of tuples. If no more rows are available, it returns an empty list.

# cursor.fetchone() method returns a single record or None if no more rows are available.

#for product in products :
    #...

#fetchone, fetchall, fetchmany #To Clean
 
# infos = (cursor.lastrowid, 'nutella','orangina') #cursor.lastrowid récupère le dernier id 

# request = 'SELECT * FROM DBOFF1' 