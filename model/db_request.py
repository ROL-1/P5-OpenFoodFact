"""Class to retrives informations from database."""

import os
from controller.api_config import FIELDS
from model.db_connection import Db_connect

class Db_requests:
    """Requests for questioning database."""

    def __init__(self):
        """..."""

    def characters_max(self):
        """Retrieve the maximum number of characters for the fields.""" 
        Log = Db_connect() #TC
        char_max = {}
        for field in FIELDS.split(','):
            fetch = Log.request("""SELECT column_name, character_maximum_length
                                FROM information_schema.columns WHERE column_name = '"""
                                +field
                                +"""'AND (DATA_TYPE = 'char' OR DATA_TYPE = 'varchar')""")         
            char_max.update(fetch)
        Log.close_connection
        return char_max