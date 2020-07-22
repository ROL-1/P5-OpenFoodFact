#! /usr/bin/env python3
# coding: utf-8

"""class to get informations from API."""

import json
import requests

from api_config import REQUEST_PARAMS,CATEGORIES,FIELDS
from dbconnection import DBconnect

def characters_max():
    """Récupére le nombre de caractères maximums pour les champs"""
    # Code = 3 ???
    B = DBconnect() #TC
    cursor = B.cnx.cursor()#TC
    char_max = {}
    for field in FIELDS.split(','):
        get_char_max = ("SELECT column_name, character_maximum_length FROM information_schema.columns WHERE column_name = '"+field+"' AND (DATA_TYPE = 'char' OR DATA_TYPE = 'varchar')")
        cursor.execute(get_char_max)
        fetch = cursor.fetchall()         
        char_max.update(fetch)
    print(char_max)#TC
    DBconnect._close_connection #TC
    return char_max
 
CM = characters_max()#TC

def api_request():
    """Create request to pass to the getter and decode the json (dictionary)."""
    endpoint = 'https://fr.openfoodfacts.org/cgi/search.pl?'
    params = '&'.join(REQUEST_PARAMS)+FIELDS+'&tag_0='
    
    with open("scraped_file.json", "w") as write_file:#TC
        for category in CATEGORIES:
            request = requests.get(endpoint+params+category)
            print(endpoint+params+category) #TC
            scraped = json.loads(request.text)   
            print(type(scraped)) #TC
            print(scraped['products'][0]) #TC  

            # Review each product : if a check failed the product will not be injected in database
            for product in scraped['products']:                
                # Add field with boolean for manage injection in database
                product["injection"] = "True" 
                # Check 1) if data is missing 
                for value in product.values():                    
                    if value == "" :
                        product["injection"] = "False"
                # Check 2) if string is too long for database field            
                for key, value in product.items():
                    for field in FIELDS.split(','):
                        if key == field:
                            if key in CM.keys():
                                if len(value) > CM[key]:
                                    product["injection"] = "False"


    
        json.dump(scraped, write_file, indent=4) #TC
                    
api_request()




# SOURCE D:\Users\Kynes\Documents\Code\PARCOURS\P5\P5-OpenFoodFact\DBOFF1.sql

# https://realpython.com/python-json/
