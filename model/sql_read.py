"""Read SQL file and extract database name to dbname.py."""

import re
from model.json import Json

class Db_sql:
    """Read sql file."""
    def __init__(self, verbose):
        self.verbose = verbose
    
    def read_sql(self, sql_file):
        """Read .sql file.""" 
        if self.verbose:
            print("Reading '{}'".format(sql_file))       
        with open(sql_file, 'r') as read_sql:
            sql_readed = read_sql.read()
        return sql_readed 

    def database_name(self, sql_readed):
        if self.verbose:
            print("Extract database name.")
        """Find database name in .sql file."""
        result = re.search("USE (.*)",sql_readed)
        database_name = result.group(1).split("`")[1]
        Json.save_database_name(database_name)


    


