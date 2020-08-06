"""Insert data in data base. From JSON."""

import os
from model.db_connection import Db_connect
from controller.api_config import FIELDS
from controller.api_config import CATEGORIES
from model.rom import Rom

class Db_insert:
    """Insert data in data base."""

    def __init__ (self, Log, Api_data, verbose):
        """Retrive connection to server sql."""
        self.Log = Log

    def tables_list(self, product):
        """Define list for insertion in Tables."""
        Codes_products_OFF = ['Codes_products_OFF', 'code', product['code']]
        Brands = ['Brands', 'brands', product['brands']]
        Nutriscore_grades = ['Nutriscore_grades', 'nutriscore_grade', product['nutriscore_grade']]
        Categories = ['Categories', 'categories', product['categories']]
        insert_lists = [Codes_products_OFF, Brands, Nutriscore_grades, Categories]
        # Defines list for insertion in Table 'Stores' :
        for store in product['stores'].split(','):                
            Stores = ['Stores', 'stores', store]
            insert_lists.append(Stores)
        return insert_lists
    
    def get_id_list(self, product):
        """Table Products : create request for fields' id."""
        Codes_products_OFF_id =  ['Codes_products_OFF_id', 'Codes_products_OFF', 'code', product['code']]
        BrandID = ['brands_id', 'Brands', 'brands', product['brands']]
        Nutriscores_grades_ID = ['nutriscore_grade_id', 'Nutriscore_grades', 'nutriscore_grade', product['nutriscore_grade']]
        Product_category_ID = ['categories_id', 'Categories', 'categories', product['categories']]            
        id_list = [Codes_products_OFF_id, BrandID, Nutriscores_grades_ID, Product_category_ID]
        return id_list

    def products_list(self, product, Codes_products_OFF_id, BrandID, Nutriscores_grades_ID, Product_category_ID):
        """Table Products : create request."""
        Products = ['Products',
            'Codes_products_OFF_Codes_products_OFF_id, product_name_fr, generic_name_fr, url, Brands_brands_id, Nutriscore_grades_nutriscore_grade_id, Categories_categories_id',
            (Codes_products_OFF_id, product['product_name_fr'], product['generic_name_fr'], product['url'] ,BrandID, Nutriscores_grades_ID, Product_category_ID)
            ]
        insert_lists = [Products,]    
        return insert_lists
    
    def phs_id(self, product):
        """Get Product_ID."""
        ProductID = ['products_id', 'Products', 'product_name_fr', product['product_name_fr']]
        request_lists = [ProductID,]
        return request_lists

    def store_id(self, store):
        """Get store_ID."""
        StoreID = ['stores_id', 'Stores', 'stores', store]
        request_lists = [StoreID,]
        return request_lists        

    def insert_data(self, Api_data, verbose):
        """..."""
        if verbose:
            print('Inserting datas to database')

        product_count = 0
        for product in Api_data:
            if verbose: #for debug
                print('Product count:',product_count, '; Product code : ', product['code'])                    
            # Tables : defines listes for insertion.
            insert_lists = self.tables_list(product)
            # Tables : datas insertion.
            Rom.simple_insertion(self.Log, insert_lists)

            # Table Products : get id for fields. 
            request_lists = self.get_id_list(product)            
            id_list = Rom.simple_request(self.Log, request_lists)
            # Table Products : define id.
            Codes_products_OFF_id = id_list[0]
            BrandID = id_list[1]            
            Nutriscores_grades_ID = id_list[2]
            Product_category_ID = id_list[3]
            # Table Products : insertion.
            insert_lists = self.products_list(product, Codes_products_OFF_id, BrandID, Nutriscores_grades_ID, Product_category_ID)
            Rom.multiple_insertion(self.Log, insert_lists)

            # Table products_has_Stores : (many-to-many relationship).
            request_lists = self.phs_id(product)
            result_list = Rom.simple_request(self.Log, request_lists)
            # Table products_has_Stores : define ProductID.
            ProductID = result_list[0]
            # Table Stores : Get Store_ID and insertion in products_has_Stores.
            for store in product['stores'].split(','):
                request_lists = store_id(store)
                result_list = Rom.simple_request(self.Log, request_lists)
                # Table Stores : define id.
                StoreID = result_list[0] 
                Products_has_Stores = ['Products_has_Stores',(ProductID,StoreID)]
                insert_lists = [Products_has_Stores,]
                # Table Products_has_Stores : insertion.
                Rom.two_values_insertion(self.Log,insert_lists)
            # Commit changes to database.
            self.Log.cnn.commit()
            product_count +=1
                                     
        if verbose:
            print(f'Database filled with {product_count} products.')
        # Make sure data is committed to the database
        self.Log.cnn.commit() #TC
        self.Log.close_connection #TC
