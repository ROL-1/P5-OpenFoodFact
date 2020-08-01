"""Insert data in data base. From JSON."""

import os
import json

from model.db_connection import Db_connect
from controller.api_config import FIELDS
from controller.api_config import CATEGORIES

# IGNORE

class Db_insert:
    """Insert data in data base. From JSON."""

    def __init__ (self, Api_data, verbose):
        """ ... """               

    def insertion(table, column, string):
        """Insert datas to database."""
        Log = Db_connect()
        Log.execute("INSERT IGNORE INTO {} ({}) VALUES (%s)".format(table,column),[string])

    def insert_data(self, Api_data, verbose):
        """..."""
        if verbose:
            print('Inserting datas to database')
        # Connexion MySQL
        # Log = Db_connect() #TC 
        product_count = 0
        for product in Api_data:
            if product['injection'] == 'True':
                if verbose: #for debug
                    print('Product count:',product_count, '; Product code : ', product['code'])            
                   
                # Table Codes_products_OFF / Table Brands / Table Nutriscore_grades
                
                Table1 = ['Codes_products_OFF', 'code', product['code']]
                Table2 = ['Brands', 'brands', product['brands']]
                Table3 = ['Nutriscore_grades', 'nutriscore_grade', product['nutriscore_grade']]
                Db_insert.insertion(product, column, Table, field)

                # Table Db_categories
                # While = danger ?
                Db_Categories_List = Log.request("SELECT categories from Categories")
                search_category = True 
                while search_category:
                    for category in CATEGORIES:
                        if category in product['categories']:
                            search_category = False               
                            Product_category = category         
                            Log.execute("INSERT IGNORE INTO Categories (categories) VALUES (%s)",[category])  

                # Table Stores, multiple values in product['stores'] : use many-to-many relationship.
                Db_stores = Log.request("SELECT stores from Stores")

                # Fin new products_id.
                Last_Product_ID = Log.request("SELECT products_id FROM Products ORDER BY products_id DESC LIMIT 1")
                if not(Last_Product_ID):                
                    ProductID = 0
                else:
                    ProductID =  Last_Product_ID[0][0]+1   

                for store in product['stores'].split(','):
                    if store in Db_stores:
                        StoreID = Log.request("SELECT stores_id FROM Stores WHERE stores = (%s)",[store])[0][0]
                        Log.execute("INSERT IGNORE INTO Products_has_Stores VALUES (%s,%s)",[ProductID,StoreID]) 
                    else:
                        Log.execute("INSERT IGNORE INTO Stores (stores) VALUES (%s)",[store])
                        StoreID = Log.request("SELECT stores_id FROM Stores WHERE stores = (%s)",[store])[0][0]
                        Log.execute("INSERT IGNORE INTO Products_has_Stores VALUES (%s,%s)",(ProductID,StoreID))      

                # Table Products
                Codes_products_OFF_id = Log.request("SELECT Codes_products_OFF_id FROM Codes_products_OFF ORDER BY Codes_products_OFF_id DESC LIMIT 1")[0][0]
                BrandID = Log.request("SELECT brands_id FROM Brands WHERE brands = (%s)",[product['brands']])[0][0]
                Nutriscores_grades_ID = Log.request("SELECT nutriscore_grade_id FROM Nutriscore_grades WHERE nutriscore_grade = (%s)",[product['nutriscore_grade']])[0][0]
                Product_Db_category_ID = Log.request("SELECT categories_id FROM Categories WHERE categories = (%s)",[Product_category])[0][0]                         
                data_field = ("INSERT IGNORE INTO Products (Codes_products_OFF_Codes_products_OFF_id, product_name_fr, url, Brands_brands_id, Nutriscore_grade_nutriscore_grade_id, Categories_categories_id) VALUES (%s,%s,%s,%s,%s,%s)")                    
                data_string = (Codes_products_OFF_id, product['product_name_fr'],product['url'],BrandID,Nutriscores_grades_ID, Product_Db_category_ID)                
                Log.execute(data_field, data_string)
                Log.cnn.commit()
                product_count +=1  
        if verbose:
            print(f'Database filled with {product_count} products.')

        # Make sure data is committed to the database
        Log.cnn.commit() #Enregistre l'information

        Log.close_connection #TC
