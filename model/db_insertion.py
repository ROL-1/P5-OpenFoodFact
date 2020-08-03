"""Insert data in data base. From JSON."""

from model.db_connection import Db_connect
from controller.api_config import FIELDS
from controller.api_config import CATEGORIES
from model.rom import Rom

class Db_insert:
    """Insert data in data base."""

    def __init__ (self, Api_data, verbose):
        """ ... """

    def insert_data(self, Api_data, verbose):
        """..."""
        if verbose:
            print('Inserting datas to database')
        # Connexion MySQL
        with open('model/db_config.py','r') as file :
           for line in file:
               if 'DATABASE' in line:
                   DATABASE = line.split('= ')[1].replace("'","")  
        Log = Db_connect(DATABASE)

        product_count = 0
        for product in Api_data:
            if verbose: #for debug
                print('Product count:',product_count, '; Product code : ', product['code'])
                    
            # Defines list for insertion in Tables :                
            Codes_products_OFF = ['Codes_products_OFF', 'code', product['code']]
            Brands = ['Brands', 'brands', product['brands']]
            Nutriscore_grades = ['Nutriscore_grades', 'nutriscore_grade', product['nutriscore_grade']]
            Categories = ['Categories', 'categories', product['categories']]         
            insert_lists = [Codes_products_OFF, Brands, Nutriscore_grades, Categories]
            # Defines list for insertion in Table 'Stores' :
            for store in product['stores'].split(','):
                Stores = ['Stores', 'stores', store]
                insert_lists.append(Stores)
            # Insert datas in Tables.
            Rom.simple_insertion(Log, insert_lists)

            # Table Products
            # Get id for fields
            Codes_products_OFF_id =  ['Codes_products_OFF_id', 'Codes_products_OFF', 'code', product['code']]
            BrandID = ['brands_id', 'Brands', 'brands', product['brands']]
            Nutriscores_grades_ID = ['nutriscore_grade_id', 'Nutriscore_grades', 'nutriscore_grade', product['nutriscore_grade']]
            Product_category_ID = ['categories_id', 'Categories', 'categories', product['categories']]            
            request_lists = [Codes_products_OFF_id, BrandID, Nutriscores_grades_ID, Product_category_ID]
            result_list = Rom.simple_request(Log, request_lists)
            # Define id 
            Codes_products_OFF_id = result_list[0]
            BrandID = result_list[1]            
            Nutriscores_grades_ID = result_list[2]
            Product_category_ID = result_list[3]
            # Make request
            Products = ['Products',
            'Codes_products_OFF_Codes_products_OFF_id, product_name_fr, url, Brands_brands_id, Nutriscore_grade_nutriscore_grade_id, Categories_categories_id',
            (Codes_products_OFF_id, product['product_name_fr'], product['url'] ,BrandID, Nutriscores_grades_ID, Product_category_ID)
            ]
            insert_lists = [Products,]
            Rom.multiple_insertion(Log,insert_lists)

            # Table products_has_Stores : (many-to-many relationship).
            # Get Product_ID
            ProductID = ['products_id', 'Products', 'product_name_fr', product['product_name_fr']]
            request_lists = [ProductID,]
            result_list = Rom.simple_request(Log, request_lists)
            ProductID = result_list[0]
            # Get Store_ID and inject.
            for store in product['stores'].split(','):                
                StoreID = ['stores_id', 'Stores', 'stores', store]
                insert_lists = [StoreID,]
                Rom.simple_request(Log, insert_lists)
                StoreID = result_list[0]
                Products_has_Stores = ['Products_has_Stores',(ProductID,StoreID)]
                insert_lists = [Products_has_Stores,]
                Rom.two_values_insertion(Log,insert_lists)
            
            # Commit changes to database.
            Log.cnn.commit()
            product_count +=1 
             
        if verbose:
            print(f'Database filled with {product_count} products.')

        # Make sure data is committed to the database
        Log.cnn.commit() #Enregistre l'information

        Log.close_connection #TC
