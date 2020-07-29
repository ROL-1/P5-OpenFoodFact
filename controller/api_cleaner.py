#! /usr/bin/env python3
# coding: utf-8

"""class to get informations from API."""

import os
import json
import requests

from model.dbrequest import DBrequests
from controller.api_config import REQUEST_PARAMS,CATEGORIES,FIELDS,MIN_PROD

class Api_Requests:
    """..."""

    def __init__(self, Fields_charmax, verbose):
        """Get datas from api by looping on each category until it's filled."""
        if verbose:
            print('Getting data from API...')       
        self.scraped  = []
        self.endpoint = 'https://fr.openfoodfacts.org/cgi/search.pl?' 
        self.page_nb = 1               

    def api_request(self, category):
        """Get datas from api by creating endpoint with parameters."""
        params = '&'.join(REQUEST_PARAMS)+FIELDS+'&page='+str(self.page_nb)+'&tag_0='              
        request = requests.get(self.endpoint+params+category)
        return request 

    def append_scraped(self, request):
        """Add products in list scraped."""
        load = json.loads(request.text)
        for i in load['products'] : self.scraped.append(i)

    def field_injection(self, scraped):
        """Add field to manage injection in database."""
        for product in scraped:
            product["injection"] = 'True'
    
    def data_missing(self, product):
        """Check 1 : if field or data is missing."""
        # Field missing
        for element in FIELDS.split(','):
            if element not in product.keys():
                return 'False'  
        # String missing 
        for string in product.values():    
            if string == "" :
                return 'False'

    def string_length(self, Fields_charmax, product):
        """Check 2 : if string is too long for database field."""
        for field, string in product.items():
            # Excludes verification for the 'injection' field.
            if field != 'injection':
                # Check for fields with characters_max().
                if field in Fields_charmax.keys():
                    # Check for element with max length for 'stores'.
                    if field == "stores":                                
                        if len(max(string.split(','), key=len)) > Fields_charmax[field]:
                            return 'False'
                    else:
                        if len(string) > Fields_charmax[field]:
                            return 'False'
    
    def define_category(self, category, product):
        """Create 'Db_categories' to class the product in database."""
        if category in product['categories'].split(','):
            product["Db_categories"] = category

    def products_nb(self, scraped, category):
        """Check how many products by categories are suitables."""
        products_nb = 0
        for product in scraped:
            if product["injection"] == 'True':                                              
                if category in product['categories'].split(','):
                    products_nb += 1
        if products_nb < MIN_PROD:                    
            category_filled = False
        else:
            category_filled = True
        return category_filled

    def api_get_data(self, Fields_charmax, verbose):    
        """Review categories until there is 'MIN_PROD' products for each."""
        for category in CATEGORIES:
            if verbose:
                print('Loading',category)
            category_filled = False     
            while category_filled is False:
                request = self.api_request(category)                
                self.append_scraped(request)
                # Call cleaner, if category is not filled : loop on next page. 
                if verbose:
                    print('Cleaning data for',category)
                # Add field 'injection'.
                self.field_injection(self.scraped)
                # Review products.
                for product in self.scraped:
                    # Check datas.                
                    Data = self.data_missing(product)
                    Strings = self.string_length(Fields_charmax, product)
                    # Create category.
                    self.define_category(category, product) 
                    # Change injection field if a check is failed.                   
                    if ((Data or Strings) == 'False') or ('Db_categories' not in product):
                        product["injection"] = 'False'

                # Check how many products by categories are suitables.
                category_filled = self.products_nb(self.scraped, category)
                if category_filled:
                    self.page_nb +=1
                else:
                    self.page_nb = 1         
        if verbose:
            print('Datas cleaned. Founded', MIN_PROD,'products minimum by categories.')

        # Write JSON for debug
        with open("scraped_file.json", "w") as write_file:
            json.dump(self.scraped, write_file, indent=4)  
        return self.scraped
         