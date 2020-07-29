"""Read SQL file and extract database name to dbname.py."""

import re

class Db_sql:
    """Read sql file."""
    
    def __init__(self, sql_file, verbose):
        """..."""

    def read_sql(self, sql_file, verbose):
        """Read .sql file.""" 
        if verbose:
            print("Reading '{}'".format(sql_file))       
        with open(sql_file, 'r') as read_sql:
            sql_readed = read_sql.read()
        return sql_readed 

class Db_name:
    """Write database name in dbname.py."""

    def __init__(self, sql_readed, verbose):
        """..."""

    def database_name(self, sql_readed, verbose):
        """Find database name in .sql file.""" 
        result = re.search("USE (.*)",sql_readed)
        DATABASE = result.group(1).split("`")[1]
        with open('model/db_name.py','w') as write_file:
            write_file.write("DATABASE = '{}'".format(DATABASE))
   

    

