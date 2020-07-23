#! /usr/bin/env python3
# coding: utf-8

"""class to get informations from API."""

import json
import requests

from dbrequest import DBrequests
from api_config import REQUEST_PARAMS,CATEGORIES,FIELDS

class Api_requests:
    """..."""

    def __init__(self):
        """..."""
        pass

    def api_get_data(self):
        """Create request to pass to the getter and decode json in a dictionnary."""
        endpoint = 'https://fr.openfoodfacts.org/cgi/search.pl?'
        params = '&'.join(REQUEST_PARAMS)+FIELDS+'&tag_0='
        
        for category in CATEGORIES:
            request = requests.get(endpoint+params+category)
            self.scraped = json.loads(request.text)
            # print(type(scraped))#TC            
        return self.scraped

    def api_parser_data(self):        
        """Review each product : if a check failed the product will not be injected in database."""
        for product in self.scraped['products']:                
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

            def string_length():
                """Check 2 : if string is too long for database field."""
                for field, string in product.items():
                    # Excludes verification for the 'injection' field
                    if field != 'injection':
                        # Make verification only for fields find with characters_max() (char or varchar)
                        if field in CHARMAX.keys():
                            # Make verification only for string with the maximum length for 'categories' and 'brands'.
                            if field == ("categories" or "brands"):                                
                                if len(max(string.split(','), key=len)) > CHARMAX[field]:
                                    return 'False'
                            else:
                                if len(string) > CHARMAX[field]:
                                    return 'False'
            
            # Launch Checks
            data_missing()
            string_length()
            # Change injection field if a check is failed.
            if (data_missing() or string_length()) == 'False':
                product["injection"] = 'False'
            
            with open("scraped_file.json", "w") as write_file: #TC
                json.dump(self.scraped, write_file, indent=4) #TC   


CM = DBrequests() #TC
CHARMAX = CM.characters_max() #TC
TEST1 = Api_requests() #TC
TEST1.api_get_data()#TC
TEST1.api_parser_data()#TC

           


    # def api_get_data(self):
    #     """Create request to pass to the getter and decode the json (dictionary)."""
    #     endpoint = 'https://fr.openfoodfacts.org/cgi/search.pl?'
    #     params = '&'.join(REQUEST_PARAMS)+FIELDS+'&tag_0='
        
    #     # with open("scraped_file.json", "w") as write_file: #TC
    #     for category in CATEGORIES:
    #         request = requests.get(endpoint+params+category)
    #         scraped = json.loads(request.text)
    #         # Review each product : if a check failed the product will not be injected in database
    #         for product in scraped['products']:                
    #             # Add field with boolean for manage injection in database
    #             product["injection"] = "True" 
    #             # Check 1 : if data is missing 
    #             for value in product.values():                    
    #                 if value == "" :
    #                     product["injection"] = "False"
    #             # Check 2 : if string is too long for database field            
    #             for field, string in product.items():
    #                 # Excludes verification for the 'injection' field
    #                 if field != 'injection':
    #                     # Make verification only for fields find with characters_max() (char or varchar)
    #                     if field in CHARMAX.keys():
    #                         # Make verification only for string with the maximum length for 'categories' and 'brands'.
    #                         if field == "categories" or field == "brands":                                
    #                             if len(max(string.split(','), key=len)) > CHARMAX[field]:
    #                                 product["injection"] = "False"
    #                         else:
    #                             if len(string) > CHARMAX[field]:
    #                                 product["injection"] = "False"


    
        # json.dump(scraped, write_file, indent=4) #TC
                    

