"""Read SQL file and extract database name to dbname.py."""

import re

class Db_sql:
    """Read sql file."""
    
    def read_sql(sql_file, verbose):
        """Read .sql file.""" 
        if verbose:
            print("Reading '{}'".format(sql_file))       
        with open(sql_file, 'r') as read_sql:
            sql_readed = read_sql.read()
        return sql_readed 

    def database_name(sql_readed, verbose):
        """Find database name in .sql file."""
        result = re.search("USE (.*)",sql_readed)
        database_name = result.group(1).split("`")[1]
        New_line = "DATABASE = '{}'".format(database_name)
        with open('model/db_config.py','r') as f1:
            file_source = f1.read()
        with open('model/db_config.py','r') as f2:
            for line in f2:
                if 'DATABASE' in line:
                    Old_line = re.match(r".*",line).group(0)
        replace_string = file_source.replace(Old_line, New_line)
        with open('model/db_config.py','w') as f2: 
            write_file = f2.write(replace_string)

    


