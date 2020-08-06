"""Class to retrives informations from database."""

from controller.api_config import FIELDS
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

    def user_insert(self, user_name):
        """User acount : create request for insertion."""
        User_name = ['Users', 'username', user_name]        
        insert_lists = [User_name,]
        return insert_lists  

    def tables_list(self, product):
        """Tables : create request for insertion."""
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
        """Table Products : create request to get fields id."""
        Codes_products_OFF_id =  ['Codes_products_OFF_id', 'Codes_products_OFF', 'code', product['code']]
        BrandID = ['brands_id', 'Brands', 'brands', product['brands']]
        Nutriscores_grades_ID = ['nutriscore_grade_id', 'Nutriscore_grades', 'nutriscore_grade', product['nutriscore_grade']]
        Product_category_ID = ['categories_id', 'Categories', 'categories', product['categories']]            
        id_list = [Codes_products_OFF_id, BrandID, Nutriscores_grades_ID, Product_category_ID]
        return id_list

    def products_list(self, product, Codes_products_OFF_id, BrandID, Nutriscores_grades_ID, Product_category_ID):
        """Table Products : create request for insertion."""
        Products = ['Products',
            'Codes_products_OFF_Codes_products_OFF_id, product_name_fr, generic_name_fr, url, Brands_brands_id, Nutriscore_grades_nutriscore_grade_id, Categories_categories_id',
            (Codes_products_OFF_id, product['product_name_fr'], product['generic_name_fr'], product['url'] ,BrandID, Nutriscores_grades_ID, Product_category_ID)
            ]
        insert_lists = [Products,]    
        return insert_lists
    
    def phs_id(self, product):
        """Create request to get Product_ID."""
        ProductID = ['products_id', 'Products', 'product_name_fr', product['product_name_fr']]
        request_lists = [ProductID,]
        return request_lists

    def store_id(self, store):
        """Create request to get store_ID."""
        StoreID = ['stores_id', 'Stores', 'stores', store]
        request_lists = [StoreID,]
        return request_lists