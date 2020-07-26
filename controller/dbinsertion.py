"""Insert data in data base. From JSON."""

import json

from controller.dbconnection import DBconnect
from controller.api_config import FIELDS



class DBinsert:
    """Insert data in data base. From JSON."""

    # Ouvre le json : dans le __init__ ?
    def __init__ (self, Api_data, verbose):
        """ ... """
               

    def insert_data(self, Api_data, verbose):
        """..."""
        if verbose:
            print('Inserting data to database')
        # Connexion MySQL
        Log = DBconnect() #TC   
        cursor = Log.cnx.cursor()#TC 

        # fonction insertion des données
        for product in Api_data:
            # Table Products
            data_field = ("INSERT INTO Products (Codes_products_OFF, product_name_fr,url,Grades,grades_id,Brands,brands_id) VALUES (%s)")
            data_string = (product['product_name_fr'],)                     
            cursor.execute(data_field, data_string)




            for field, string in product.items():
                if field != 'injection':
                    if count <1:
                        print(("INSERT INTO {} ({}) VALUES (%s)").format(field,field))
                        print(string)
                        data_field = (("INSERT INTO {} ({}) VALUES (%s)").format(field,field))
                        data_string = (string,)                     
                        cursor.execute(data_field, data_string)

        
        

        # Make sure data is committed to the database
        Log.cnx.commit() #Enregistre l'information

        DBconnect.close_connection #TC
        # self.connect = DBconnect() #TC 

# A = DBinsert() #TC
#https://pynative.com/python-cursor-fetchall-fetchmany-fetchone-to-read-rows-from-table/
#products = cursor.fetchall()

# cursor.fetchall() fetches all the rows of a query result.
#  It returns all the rows as a list of tuples. An empty list is returned if there is no record to fetch.

# cursor.fetchmany(size) returns the number of rows specified by size argument.
#  When called repeatedly this method fetches the next set of rows of a query result and returns a list of tuples.
#  If no more rows are available, it returns an empty list.

# cursor.fetchone() method returns a single record or None if no more rows are available.

#for product in products :
    #...

#fetchone, fetchall, fetchmany #To Clean
 
# infos = (cursor.lastrowid, 'nutella','orangina') #cursor.lastrowid récupère le dernier id 

# request = 'SELECT * FROM DBOFF1' 