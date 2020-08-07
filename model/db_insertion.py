"""Insert data in data base. From JSON."""

from model.rom import Rom
from model.db_requests_lists import Db_requests_lists

class Db_insert:
    """Insert data in data base."""

    def __init__ (self, Log, Api_data=None, verbose=None):
        """Retrive connection to server sql."""
        self.Log = Log

    def insert_user(self, insert_lists):
        """Insert user account in database."""
        Rom.simple_insertion(self.Log, insert_lists)
        self.Log.commit()
        self.Log.close_connection() 

    def insert_data(self, Api_data, verbose):
        """..."""
        if verbose:
            print('Inserting datas to database')

        product_count = 0
        for product in Api_data:
            if verbose: #for debug
                print('Product count:',product_count, '; Product code : ', product['code'])                    
            # Tables : defines listes for insertion.
            insert_lists = Db_requests_lists().tables_list(product)
            # Tables : datas insertion.
            Rom.simple_insertion(self.Log, insert_lists)

            # Table Products : get id for fields. 
            request_lists = Db_requests_lists().get_id_list(product)            
            id_list = Rom.simple_request(self.Log, request_lists)
            # Table Products : define id.
            Codes_products_OFF_id = id_list[0]
            BrandID = id_list[1]            
            Nutriscores_grades_ID = id_list[2]
            Product_category_ID = id_list[3]
            # Table Products : insertion.
            insert_lists = Db_requests_lists().products_list(product, Codes_products_OFF_id, BrandID, Nutriscores_grades_ID, Product_category_ID)
            Rom.multiple_insertion(self.Log, insert_lists)

            # Table products_has_Stores : (many-to-many relationship).
            request_lists = Db_requests_lists().phs_id(product)
            result_list = Rom.simple_request(self.Log, request_lists)
            # Table products_has_Stores : define ProductID.
            ProductID = result_list[0]
            # Table Stores : Get Store_ID and insertion in products_has_Stores.
            for store in product['stores'].split(','):
                request_lists = Db_requests_lists().store_id(store)
                result_list = Rom.simple_request(self.Log, request_lists)
                # Table Stores : define id.
                StoreID = result_list[0] 
                Products_has_Stores = ['Products_has_Stores',(ProductID,StoreID)]
                insert_lists = [Products_has_Stores,]
                # Table Products_has_Stores : insertion.
                Rom.two_values_insertion(self.Log,insert_lists)
            # Commit changes to database.
            self.Log.commit()
            product_count +=1
                                     
        if verbose:
            print(f'Database filled with {product_count} products.')
        # Make sure data is committed to the database
        self.Log.commit() #TC
        self.Log.close_connection()  #TC

