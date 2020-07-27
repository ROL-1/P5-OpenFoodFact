"""Insert data in data base. From JSON."""

import os
import json

from controller.dbconnection import DBconnect
from controller.api_config import FIELDS
from controller.api_config import CATEGORIES

# RETIRER LES IGNORE 

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
        count = 0
        for product in Api_data:
            if product['injection'] == 'True':
                print('Product count:',count, '; Product code : ', product['code'])
                # Table Codes_products_OFF
                data_field = ("INSERT IGNORE INTO Codes_products_OFF (code) VALUES (%s)")                    
                data_string = (product['code'],) 
                cursor.execute(data_field, data_string)
                cursor.execute("SELECT * from Codes_products_OFF")
                Db_Codes_products_OFF = cursor.fetchall()

                # Table Brands
                cursor.execute("SELECT brands from Brands")
                Db_brands = cursor.fetchall()
                if product['brands'] not in Db_brands:
                    data_field = ("INSERT IGNORE INTO Brands (brands) VALUES (%s)")                    
                    data_string = (product['brands'],)                       
                    cursor.execute(data_field, data_string)

                # Table Nutriscore_grades
                cursor.execute("SELECT nutriscore_grade from Nutriscore_grades")
                Db_Nutriscore_grades = cursor.fetchall()
                if product['nutriscore_grade'] not in Db_Nutriscore_grades:
                    data_field = ("INSERT IGNORE INTO Nutriscore_grades (nutriscore_grade) VALUES (%s)")                    
                    data_string = (product['nutriscore_grade'],)                   
                    cursor.execute(data_field, data_string)

                # Table Db_categories
                # While = danger ?
                cursor.execute("SELECT Db_categories from db_categories")
                Db_Categories_List = cursor.fetchall()
                search_category = True                
                            
                while search_category:
                    for category in CATEGORIES:
                        if category in product['Db_categories']:                        
                            data_field = ("INSERT IGNORE INTO Db_categories (db_categories) VALUES (%s)")                    
                            data_string = (category,)
                            search_category = False               
                            Product_category = category         
                            cursor.execute(data_field, data_string)
                            # os.system('pause') #TC

                # Table Stores, multiple values in product['stores'] : use many-to-many relationship.
                cursor.execute("SELECT stores from Stores")
                Db_stores = cursor.fetchall()

                # Fin new products_id.
                cursor.execute("SELECT products_id FROM Products ORDER BY products_id DESC LIMIT 1")
                Last_Product_ID = cursor.fetchall()
                if not(Last_Product_ID):                
                    ProductID = 0
                else:
                    ProductID =  Last_Product_ID[0][0]+1   

                for store in product['stores'].split(','):
                    if store in Db_stores:
                        data_field = ("SELECT stores_id FROM Stores WHERE stores = (%s)")                                      
                        data_string = (store,)
                        cursor.execute = (data_field, data_string)
                        StoreID = cursor.fetchall()
                        data_field = ("INSERT IGNORE INTO Products_has_Stores VALUES (%s,%s)")                    
                        data_string = (ProductID,StoreID)
                        cursor.execute(data_field, data_string)
                    else:
                        data_field = ("INSERT IGNORE INTO Stores (stores) VALUES (%s)")                                      
                        data_string = (store,)
                        cursor.execute(data_field, data_string)
                        data_field = ("SELECT stores_id FROM Stores WHERE stores = (%s)")                                      
                        data_string = (store,)
                        cursor.execute(data_field, data_string)
                        StoreID = cursor.fetchall()[0][0]
                        data_field = ("INSERT IGNORE INTO Products_has_Stores VALUES (%s,%s)")                    
                        data_string = (ProductID,StoreID)
                        cursor.execute(data_field, data_string)        

                # Table Products
                cursor.execute("SELECT Codes_products_OFF_id FROM Codes_products_OFF ORDER BY Codes_products_OFF_id DESC LIMIT 1")
                Codes_products_OFF_id = cursor.fetchall()[0][0]
                cursor.execute("SELECT brands_id FROM Brands WHERE brands = (%s)",[product['brands']])
                BrandID = cursor.fetchall()[0][0]
                cursor.execute("SELECT nutriscore_grade_id FROM Nutriscore_grades WHERE nutriscore_grade = (%s)",[product['nutriscore_grade']])
                Nutriscores_grades_ID = cursor.fetchall()[0][0]
                cursor.execute("SELECT db_categories_id FROM Db_categories WHERE Db_categories = (%s)",[Product_category])
                Product_Db_category_ID = cursor.fetchall()[0][0]                           
                data_field = ("INSERT IGNORE INTO Products (Codes_products_OFF_Codes_products_OFF_id, product_name_fr, url, Brands_brands_id, Nutriscore_grade_nutriscore_grade_id, Db_categories_db_categories_id) VALUES (%s,%s,%s,%s,%s,%s)")                    
                data_string = (Codes_products_OFF_id, product['product_name_fr'],product['url'],BrandID,Nutriscores_grades_ID, Product_Db_category_ID)                     
                cursor.execute(data_field, data_string)
                Log.cnx.commit()
                count +=1
        
        

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