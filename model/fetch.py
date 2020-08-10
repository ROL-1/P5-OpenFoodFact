"""Class to retrives informations from database."""

from controller.api_config import FIELDS
from model.config import NBPRODUCTS, NUTRISCORE_MIN

class Fetch:
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

    def fetch_saved_searches(self, user_id):
        """Find all saved searches for user."""
        request = """
            SELECT p1.product_name_fr as Produits, p2.product_name_fr as Substituts, create_time as Date
            FROM Searches_saved s
            INNER JOIN Products p1 ON p1.products_id = s.product_id
            INNER JOIN Products p2 ON p2.products_id = s.substitute_id
            WHERE Users_user_id = '%s'
            """ % (user_id)
        fetched_stores = self.Log.request(request)
        return fetched_stores
