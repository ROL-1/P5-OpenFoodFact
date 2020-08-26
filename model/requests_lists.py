#! /usr/bin/env python3
# coding: utf-8
"""Lists to make requests to database.

For Insertion.py and orm.py.
"""


class RequestsLists:
    """Contains lists to make requests to database."""

    def user_insert(self, user_name):
        """User account : create request for insertion."""
        User_name = ["Users", "username", [user_name]]
        insert_lists = [
            User_name,
        ]
        return insert_lists

    def user_id(self, user_name):
        """Create request to get user_id."""
        userID = ["user_id", "Users", "username", user_name]
        request_lists = [
            userID,
        ]
        return request_lists

    def save_search(self, product_id, substitute_id, user_id):
        """Create request to save search."""
        save_search = [
            "Searches_saved",
            "Products_products_id, substitute_id, Users_user_id",
            (product_id, substitute_id, user_id),
        ]
        insert_lists = [
            save_search,
        ]
        return insert_lists

    def tables_list(self, product):
        """Tables : create request for insertion."""
        Codes_products_OFF = ["Codes_products_OFF", "code", [product["code"]]]
        Brands = ["Brands", "brands", [product["brands"]]]
        Nutriscore_grades = [
            "Nutriscore_grades",
            "nutriscore_grade",
            [product["nutriscore_grade"]],
        ]
        Categories = ["Categories", "categories", [product["categories"]]]
        insert_lists = [
            Codes_products_OFF,
            Brands,
            Nutriscore_grades,
            Categories,
        ]
        # Defines list for insertion in Table 'Stores' :
        for store in product["stores"].split(","):
            Stores = ["Stores", "stores", [store]]
            insert_lists.append(Stores)
        return insert_lists

    def get_id_list(self, product):
        """Table Products : create request to get fields id."""
        Codes_products_OFF_id = [
            "Codes_products_OFF_id",
            "Codes_products_OFF",
            "code",
            product["code"],
        ]
        BrandID = ["brands_id", "Brands", "brands", product["brands"]]
        Nutriscores_grades_ID = [
            "nutriscore_grade_id",
            "Nutriscore_grades",
            "nutriscore_grade",
            product["nutriscore_grade"],
        ]
        Product_category_ID = [
            "categories_id",
            "Categories",
            "categories",
            product["categories"],
        ]
        request_lists = [
            Codes_products_OFF_id,
            BrandID,
            Nutriscores_grades_ID,
            Product_category_ID,
        ]
        return request_lists

    def products_list(
        self,
        product,
        Codes_products_OFF_id,
        BrandID,
        Nutriscores_grades_ID,
        Product_category_ID,
    ):
        """Table Products : create request for insertion."""
        Products = [
            "Products",
            "Codes_products_OFF_Codes_products_OFF_id, product_name_fr, "
            "generic_name_fr, url, Brands_brands_id, "
            "Nutriscore_grades_nutriscore_grade_id, "
            "Categories_categories_id",
            (
                Codes_products_OFF_id,
                product["product_name_fr"],
                product["generic_name_fr"],
                product["url"],
                BrandID,
                Nutriscores_grades_ID,
                Product_category_ID,
            ),
        ]
        insert_lists = [
            Products,
        ]
        return insert_lists

    def phs_id(self, product):
        """Create request to get Product_ID."""
        ProductID = [
            "products_id",
            "Products",
            "product_name_fr",
            product["product_name_fr"],
        ]
        request_lists = [
            ProductID,
        ]
        return request_lists

    def store_id(self, store):
        """Create request to get store_ID."""
        StoreID = ["stores_id", "Stores", "stores", store]
        request_lists = [
            StoreID,
        ]
        return request_lists
