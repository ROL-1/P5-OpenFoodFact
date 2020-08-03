"""Class to retrives informations from database."""

import os
from controller.api_config import FIELDS
from model.db_connection import Db_connect
from model.db_config import NBPRODUCTS

class Db_requests:
    """Requests for questioning database."""

    def __init__(self, category=None, choice=None, product_id=None):
        """..."""
        self.NBPRODUCTS = NBPRODUCTS

    def characters_max(self):
        """Retrieve the maximum number of characters for the fields."""
        Log = Db_connect().database_log()
        char_max = {}
        for field in FIELDS.split(','):
            fetch = Log.request("""SELECT column_name, character_maximum_length
                                FROM information_schema.columns WHERE column_name = '"""
                                +field
                                +"""'AND (DATA_TYPE = 'char' OR DATA_TYPE = 'varchar')""")         
            char_max.update(fetch)
        Log.close_connection
        return char_max
    
    def fetch_products(self, category):
        """Return 'NBPRODUCTS' products from a category."""
        request = f"""
            SELECT products_id as ID,
            product_name_fr as Produits, 
            Brands.brands as Marque, 
            Nutriscore_grades.nutriscore_grade as Nutriscore,
            Stores.stores as Magasins
            FROM Products 
            INNER JOIN Brands ON Brands.brands_id = Products.Brands_brands_id
            INNER JOIN Nutriscore_grades ON Nutriscore_grades.Nutriscore_grade_id = Products.Nutriscore_grades_Nutriscore_grade_id
            INNER JOIN Categories ON Categories.categories_id = Products.Categories_categories_id
            INNER JOIN Products_has_Stores ON Products.products_id = Products_has_Stores.Products_products_id
            INNER JOIN Stores ON Products_has_Stores.Stores_stores_id = Stores.stores_id
            WHERE Categories.categories = '{category}'
            AND Nutriscore_grades.nutriscore_grade > 'C'
            ORDER BY RAND ()            
            LIMIT {self.NBPRODUCTS}
            """
        Log = Db_connect().database_log()
        fetched_products = Log.request(request) 
        return fetched_products    
    
    def fetch_substitute(self, category):
        """Find substitute : product with better nutriscore from the same category."""
        request = f"""
            SELECT products_id as ID,
            product_name_fr as Produits, 
            Brands.brands as Marque, 
            Nutriscore_grades.nutriscore_grade as Nutriscore,
            Stores.stores as Magasins
            FROM Products 
            INNER JOIN Brands ON Brands.brands_id = Products.Brands_brands_id
            INNER JOIN Nutriscore_grades ON Nutriscore_grades.Nutriscore_grade_id = Products.Nutriscore_grades_Nutriscore_grade_id
            INNER JOIN Categories ON Categories.categories_id = Products.Categories_categories_id
            INNER JOIN Products_has_Stores ON Products.products_id = Products_has_Stores.Products_products_id
            INNER JOIN Stores ON Products_has_Stores.Stores_stores_id = Stores.stores_id
            WHERE Categories.categories = '{category}'
            AND Nutriscore_grades.nutriscore_grade <= 'C'
            ORDER BY RAND ()            
            LIMIT 1
            """
        Log = Db_connect().database_log()
        fetched_substitute = Log.request(request) 
        return fetched_substitute
    
    def fetch_product(self, product_id):
        """Find substitute : product with better nutriscore from the same category."""
        request = f"""
            SELECT products_id as ID,
            product_name_fr as Produits, 
            Brands.brands as Marque, 
            Nutriscore_grades.nutriscore_grade as Nutriscore,
            Stores.stores as Magasins
            FROM Products 
            INNER JOIN Brands ON Brands.brands_id = Products.Brands_brands_id
            INNER JOIN Nutriscore_grades ON Nutriscore_grades.Nutriscore_grade_id = Products.Nutriscore_grades_Nutriscore_grade_id
            INNER JOIN Categories ON Categories.categories_id = Products.Categories_categories_id
            INNER JOIN Products_has_Stores ON Products.products_id = Products_has_Stores.Products_products_id
            INNER JOIN Stores ON Products_has_Stores.Stores_stores_id = Stores.stores_id
            WHERE Products_products_id = '{product_id}'
            LIMIT 1
            """
        Log = Db_connect().database_log()
        fetched_product = Log.request(request) 
        return fetched_product



        # request = f"""
        #         SELECT products_id as ID, 
        #         Codes_products_OFF.code as OFF_code, 
        #         product_name_fr as Produits, 
        #         Brands.brands as Marque, 
        #         Nutriscore_grades.nutriscore_grade as Nutriscore, 
        #         Categories.categories as Categories, 
        #         Stores.stores as Magasins, 
        #         url 
        #         FROM Products 
        #         INNER JOIN Brands ON Brands.brands_id = Products.Brands_brands_id 
        #         INNER JOIN Codes_products_OFF ON Codes_products_OFF.Codes_products_OFF_id = Products.Codes_products_OFF_Codes_products_OFF_id
        #         INNER JOIN Nutriscore_grades ON Nutriscore_grades.Nutriscore_grade_id = Products.Nutriscore_grades_Nutriscore_grade_id
        #         INNER JOIN Categories ON Categories.categories_id = Products.Categories_categories_id
        #         INNER JOIN Products_has_Stores ON Products.products_id = Products_has_Stores.Products_products_id
        #         INNER JOIN Stores ON Products_has_Stores.Stores_stores_id = Stores.stores_id
        #         WHERE Categories.categories = '{category}'
        #         AND Nutriscore_grades.nutriscore_grade > 'C'
        #         ORDER BY RAND ()               
        #         LIMIT {self.NBPRODUCTS}    
        #         """