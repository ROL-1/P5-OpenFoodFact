"""Class to retrives informations from database."""

from controller.api_config import FIELDS
from model.db_connection import Db_connect
from model.db_config import NBPRODUCTS, NUTRISCORE_MIN

class Db_requests:
    """Requests for questioning database."""

    def __init__(self, Log, category=None, choice=None, product_id=None):
        """..."""
        self.NBPRODUCTS = NBPRODUCTS
        self.Log = Log.database_log()

    def characters_max(self):
        """Retrieve the maximum number of characters for the fields."""
        char_max = {}
        for field in FIELDS.split(','):
            fetch = self.Log.request(
                """SELECT column_name, character_maximum_length
                FROM information_schema.columns WHERE column_name = '%s'
                AND (DATA_TYPE = 'char' OR DATA_TYPE = 'varchar')""" % (field))     
            char_max.update(fetch)
        return char_max
    
    def fetch_products(self, category):
        """Return 'NBPRODUCTS' products from a category."""
        request = """
            SELECT DISTINCT products_id, product_name_fr, generic_name_fr, b.brands, n.nutriscore_grade
            FROM Products p
            INNER JOIN Brands b ON b.brands_id = p.Brands_brands_id
            INNER JOIN Nutriscore_grades n ON n.Nutriscore_grade_id = p.Nutriscore_grades_Nutriscore_grade_id
            INNER JOIN Categories c ON c.categories_id = p.Categories_categories_id
            INNER JOIN Products_has_Stores phs ON p.products_id = phs.Products_products_id
            WHERE c.categories = '%s'
            AND n.nutriscore_grade > '%s'
            ORDER BY RAND ()            
            LIMIT %s
            """ % (category,NUTRISCORE_MIN,self.NBPRODUCTS)

        fetched_products = self.Log.request(request) 
        return fetched_products    
    
    def fetch_substitute(self, category):
        """Find substitute : product with better nutriscore from the same category."""
        request = """
            SELECT products_id, product_name_fr, generic_name_fr, b.brands, n.nutriscore_grade, url
            FROM Products p
            INNER JOIN Brands b ON b.brands_id = p.Brands_brands_id
            INNER JOIN Nutriscore_grades n ON n.Nutriscore_grade_id = p.Nutriscore_grades_Nutriscore_grade_id
            INNER JOIN Categories c ON c.categories_id = p.Categories_categories_id
            WHERE c.categories = '%s'
            AND n.nutriscore_grade <= '%s'
            ORDER BY RAND ()            
            LIMIT 1
            """ % (category,NUTRISCORE_MIN)
        fetched_substitute = self.Log.request(request) 
        return fetched_substitute
    
    def fetch_product(self, product_id):
        """Find product datas."""
        request = """
            SELECT products_id, product_name_fr, generic_name_fr, b.brands, n.nutriscore_grade, url
            FROM Products p
            INNER JOIN Brands b ON b.brands_id = p.Brands_brands_id
            INNER JOIN Nutriscore_grades n ON n.Nutriscore_grade_id = p.Nutriscore_grades_Nutriscore_grade_id
            INNER JOIN Categories c ON c.categories_id = p.Categories_categories_id
            WHERE p.products_id = '%s'
            LIMIT 1
            """ % (product_id)
        fetched_product = self.Log.request(request) 
        return fetched_product

    def fetch_stores(self, product_id):
        """Find all stores for a product."""
        request = """
            SELECT s.stores
            FROM Products p
            INNER JOIN Products_has_Stores phs ON p.products_id = phs.Products_products_id
            INNER JOIN Stores s ON phs.Stores_stores_id = s.stores_id
            WHERE Products_products_id = '%s'
            """ % (product_id)
        fetched_stores = self.Log.request(request)
        return fetched_stores    

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