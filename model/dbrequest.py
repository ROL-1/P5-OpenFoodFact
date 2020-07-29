"""Class to retrives informations from database."""

from controller.api_config import FIELDS
from model.dbconnection import DBconnect

class DBrequests:
    """Requests for questioning database."""

    def __init__(self):
        """..."""

    def characters_max(self):
        """Retrieve the maximum number of characters for the fields."""     
        Log = DBconnect() #TC
        char_max = {}
        for field in FIELDS.split(','):
            fetch = Log.request("""SELECT column_name, character_maximum_length
                                FROM information_schema.columns WHERE column_name = '"""
                                +field
                                +"""'AND (DATA_TYPE = 'char' OR DATA_TYPE = 'varchar')""")         
            char_max.update(fetch)
        # print(char_max)#TC
        Log.close_connection #TC
        return char_max # Code = 3 ???