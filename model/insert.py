#! /usr/bin/env python3
# coding: utf-8
"""Insert data in data base."""

from model.orm import Orm
from model.requests_lists import RequestsLists


class Insert:
    """Insert data in data base."""

    def __init__(self, Log, verbose, Api_data=None):
        """Retrive connection to server sql."""
        self.verbose = verbose
        self.Log = Log

    def insert_user(self, insert_lists):
        """Insert user account in database."""
        Orm(self.Log).multiple_insertion(insert_lists)
        self.Log.commit()

    def insert_save(self, insert_lists):
        """Save search in database."""
        Orm(self.Log).multiple_insertion(insert_lists)
        self.Log.commit()

    def insert_data(self, Api_data):
        """Fill database."""
        if self.verbose:
            print("Inserting datas to database.")

        product_count = 0
        Request_lists = RequestsLists()
        for product in Api_data:
            if self.verbose:  # for debug
                print(
                    "Product count:",
                    product_count,
                    "; Product code : ",
                    product["code"],
                )
            # Tables : defines listes for insertion.
            insert_lists = Request_lists.tables_list(product)
            # Tables : datas insertion.
            Orm(self.Log).multiple_insertion(insert_lists)
            # Table Products : get id for fields.
            request_lists = Request_lists.get_id_list(product)
            id_list = Orm(self.Log).simple_request(request_lists)
            # Table Products : define id.
            Codes_products_OFF_id = id_list[0]
            BrandID = id_list[1]
            Nutriscores_grades_ID = id_list[2]
            Product_category_ID = id_list[3]
            # Table Products : insertion.
            insert_lists = Request_lists.products_list(
                product,
                Codes_products_OFF_id,
                BrandID,
                Nutriscores_grades_ID,
                Product_category_ID,
            )
            Orm(self.Log).multiple_insertion(insert_lists)
            # Table products_has_Stores : (many-to-many relationship).
            request_lists = Request_lists.phs_id(product)
            result_list = Orm(self.Log).simple_request(request_lists)
            # Table products_has_Stores : define ProductID.
            ProductID = result_list[0]
            # Table Stores : Get Store_ID and insertion in products_has_Stores.
            for store in product["stores"].split(","):
                request_lists = Request_lists.store_id(store)
                result_list = Orm(self.Log).simple_request(request_lists)
                # Table Stores : define id.
                StoreID = result_list[0]
                Products_has_Stores = [
                    "Products_has_Stores",
                    "Products_products_id, Stores_stores_id",
                    (ProductID, StoreID),
                ]
                insert_lists = [
                    Products_has_Stores,
                ]
                # Table Products_has_Stores : insertion.
                Orm(self.Log).multiple_insertion(insert_lists)
            # Commit changes to database.
            self.Log.commit()
            product_count += 1

        if self.verbose:
            print(f"Database filled after scanning {product_count} products.")
        # Make sure data is committed to the database
        self.Log.commit()
        self.Log.close_connection()
