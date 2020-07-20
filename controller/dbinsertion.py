"""Insert data in data base. From JSON."""

import json
from dbconnection import DBconnect

class DBinsert:
    """Insert data in data base. From JSON."""

    # Ouvre le json : dans le __init__ ?
    def __init__ (self):
        """ ... """
        with open("scraped_file.json", "r") as read_file:
            data = json.load(read_file)
            print(data['products'][1]['code'])            

        #connexion
        B = DBconnect() #TC   
        cursor = B.connection.cursor()#TC      

        # fonction insertion des données
        add_brand = ("INSERT INTO brands (brands_id,brands_name) VALUES (%s,%s)") #requette pour ajouter une marque      
        data_brand = (444,data['products'][1]['brands']) #marque test

        # action insérer une nouvelle marque
        cursor.execute(add_brand,data_brand)

        # Make sure data is committed to the database
        B.connection.commit() #Enregistre l'information

        DBconnect._close_connection #TC
        self.connect = DBconnect() #TC

A = DBinsert() #TC

# infos = (cursor.lastrowid, 'nutella','orangina') #cursor.lastrowid récupère le dernier id 

# request = 'SELECT * FROM DBOFF1' 