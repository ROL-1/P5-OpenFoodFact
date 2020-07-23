from api_config import FIELDS
from dbconnection import DBconnect

class DBrequests:
    """Requests for questioning database."""

    def __init__(self):
        pass

    def characters_max(self):
        """Retrieves the maximum number of characters for the fields."""    
        log = DBconnect() #TC
        cursor = log.cnx.cursor()#TC
        char_max = {}
        for field in FIELDS.split(','):
            get_char_max = ("""SELECT column_name, character_maximum_length
                                FROM information_schema.columns WHERE column_name = '"""
                                +field
                                +"""'AND (DATA_TYPE = 'char' OR DATA_TYPE = 'varchar')""")
            cursor.execute(get_char_max)
            fetch = cursor.fetchall()         
            char_max.update(fetch)
        # print(char_max)#TC
        log.close_connection #TC
        return char_max # Code = 3 ???

