"""Actions with Json files."""
import json

class Json:
    """Functions to write and read the json file."""

    def save_connection_params(self, host, user, password):
        """Add connection parameters to Json."""
        conn_params = {'host': host, 'user':user, 'password':password}
        with open('model/conn_params.json', 'w') as outfile:
            json.dump(conn_params, outfile)

    def read_connection_params(self):
        """Load and return connection parameters from Json."""
        with open('model/conn_params.json') as json_file:
            params = json.load(json_file)
        return params['host'],params['user'],params['password']
    
    def save_database_name(database_name):
        """Add database name to Json."""
        database = {'DATABASE': database_name}
        with open('model/database_name.json', 'w') as outfile:
            json.dump(database, outfile)
    
    def read_database_name():
        """Load and return database name from Json."""
        with open('model/database_name.json') as json_file:
            database = json.load(json_file)
        return database['DATABASE']