#! /usr/bin/env python3
# coding: utf-8

"""class to get informations from API."""

import os
import json
import requests

from controller.dbrequest import DBrequests
from controller.api_config import REQUEST_PARAMS,CATEGORIES,FIELDS,MIN_PROD

class Api_Requests:
    """..."""

    def __init__(self, Fields_charmax, verbose):
        """..."""               

    def api_get_data(self, Fields_charmax, verbose):              
        """Get datas from api by looping on each category until it's filled."""
        if verbose:
            print('Getting data from API...')
        page_nb = 1
        scraped  = []
        endpoint = 'https://fr.openfoodfacts.org/cgi/search.pl?'      
            
        for category in CATEGORIES:
            print('Loading',category)
            category_filled = False     
            while category_filled is False:              
                params = '&'.join(REQUEST_PARAMS)+FIELDS+'&page='+str(page_nb)+'&tag_0='              
                # Get datas from api by creating endpoint with parameters.
                request = requests.get(endpoint+params+category)
                load = json.loads(request.text)
                for i in load['products'] : scraped.append(i)
                # Call cleaner, if category is not filled : loop on next page. 
                if verbose:
                    print('Cleaning data for',category)  
                for product in scraped:                
                    # Add field to manage injection in database
                    product["injection"] = 'True'

                    def data_missing():
                        """Check 1 : if field or data is missing."""
                        # Field missing
                        for element in FIELDS.split(','):
                            if element not in product.keys():
                                return 'False'  
                        # String missing 
                        for string in product.values():    
                            if string == "" :
                                return 'False'

                    def string_length(Fields_charmax):
                        """Check 2 : if string is too long for database field."""
                        for field, string in product.items():
                            # Excludes verification for the 'injection' field
                            if field != 'injection':
                                # Make verification only for fields find with characters_max() (char or varchar)
                                if field in Fields_charmax.keys():
                                    # Make verification only for element with the maximum length for 'categories' and 'brands'.
                                    if field == ("categories" or "brands"):                                
                                        if len(max(string.split(','), key=len)) > Fields_charmax[field]:
                                            return 'False'
                                    else:
                                        if len(string) > Fields_charmax[field]:
                                            return 'False'
                    
                    # Launch Checks
                    Data = data_missing()
                    Strings = string_length(Fields_charmax)
                    # Change injection field if a check is failed.
                    if (Data or Strings) == 'False':
                        product["injection"] = 'False'

                # Check how many products by categories are suitables.
                # for category in CATEGORIES:
                products_nb = 0
                for product in scraped:                                               
                    if category in product['categories'].split(','):
                        products_nb += 1
                if products_nb < MIN_PROD:                    
                    page_nb += 1
                else:                    
                    category_filled = True
                    page_nb = 1
        print('Datas cleaned. Founded', MIN_PROD,'products minimum by categories.')
        with open("scraped_file.json", "w") as write_file:
            json.dump(scraped, write_file, indent=4)  
        return scraped
         