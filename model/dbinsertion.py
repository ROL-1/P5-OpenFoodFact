"""Insert data in data base. From JSON."""

import os
import json

from model.dbconnection import DBconnect
from controller.api_config import FIELDS
from controller.api_config import CATEGORIES

# IGNORE 

class DBinsert:
    """Insert data in data base. From JSON."""

    # Ouvre le json : dans le __init__ ?
    def __init__ (self, Api_data, verbose):
        """ ... """               

    def insert_data(self, Api_data, verbose):
        """..."""
        if verbose:
            print('Inserting datas to database')
        # Connexion MySQL
        Log = DBconnect() #TC   
        cursor = Log.cnn.cursor()#TC 
        product_count = 0
        for product in Api_data:
            if product['injection'] == 'True':
                if verbose: #for debug
                    print('Product count:',product_count, '; Product code : ', product['code'])
                # Table Codes_products_OFF
                cursor.execute("INSERT IGNORE INTO Codes_products_OFF (code) VALUES (%s)",[product['code']])
                Db_Codes_products_OFF = Log.request("SELECT * from Codes_products_OFF")

                # Table Brands
                Db_brands = Log.request("SELECT brands from Brands")
                if product['brands'] not in Db_brands:
                    cursor.execute("INSERT IGNORE INTO Brands (brands) VALUES (%s)",[product['brands']])                   

                # Table Nutriscore_grades
                Db_Nutriscore_grades =  Log.request("SELECT nutriscore_grade from Nutriscore_grades")
                if product['nutriscore_grade'] not in Db_Nutriscore_grades:
                    cursor.execute("INSERT IGNORE INTO Nutriscore_grades (nutriscore_grade) VALUES (%s)",[product['nutriscore_grade']])                    

                # Table Db_categories
                # While = danger ?
                Db_Categories_List = Log.request("SELECT Db_categories from db_categories")
                search_category = True 
                while search_category:
                    for category in CATEGORIES:
                        if category in product['Db_categories']:
                            search_category = False               
                            Product_category = category         
                            cursor.execute("INSERT IGNORE INTO Db_categories (db_categories) VALUES (%s)",[category])  

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
                        StoreID = Log.request("SELECT stores_id FROM Stores WHERE stores = (%s)",[store]) 
                        cursor.execute("INSERT IGNORE INTO Products_has_Stores VALUES (%s,%s)",[ProductID,StoreID]) 
                    else:
                        cursor.execute("INSERT IGNORE INTO Stores (stores) VALUES (%s)",[store])
                        cursor.execute("SELECT stores_id FROM Stores WHERE stores = (%s)",[store])
                        StoreID = cursor.fetchall()[0][0]
                        cursor.execute("INSERT IGNORE INTO Products_has_Stores VALUES (%s,%s)",[ProductID,StoreID])      

                # Table Products
                Codes_products_OFF_id = Log.request("SELECT Codes_products_OFF_id FROM Codes_products_OFF ORDER BY Codes_products_OFF_id DESC LIMIT 1")[0][0]
                cursor.execute("SELECT brands_id FROM Brands WHERE brands = (%s)",[product['brands']])
                BrandID = cursor.fetchall()[0][0]
                cursor.execute("SELECT nutriscore_grade_id FROM Nutriscore_grades WHERE nutriscore_grade = (%s)",[product['nutriscore_grade']])
                Nutriscores_grades_ID = cursor.fetchall()[0][0]
                cursor.execute("SELECT db_categories_id FROM Db_categories WHERE Db_categories = (%s)",[Product_category])
                Product_Db_category_ID = cursor.fetchall()[0][0]                            
                data_field = ("INSERT IGNORE INTO Products (Codes_products_OFF_Codes_products_OFF_id, product_name_fr, url, Brands_brands_id, Nutriscore_grade_nutriscore_grade_id, Db_categories_db_categories_id) VALUES (%s,%s,%s,%s,%s,%s)")                    
                data_string = (Codes_products_OFF_id, product['product_name_fr'],product['url'],BrandID,Nutriscores_grades_ID, Product_Db_category_ID)                     
                cursor.execute(data_field, data_string)
                Log.cnn.commit()
                product_count +=1  
        if verbose:
            print(f'Database filled with {product_count} products.')

        # Make sure data is committed to the database
        Log.cnn.commit() #Enregistre l'information

        DBconnect.close_connection #TC
        # self.connect = DBconnect() #TC 

 
#https://pynative.com/python-cursor-fetchall-fetchmany-fetchone-to-read-rows-from-table/
 
# infos = (cursor.lastrowid, 'nutella','orangina') #cursor.lastrowid récupère le dernier id 