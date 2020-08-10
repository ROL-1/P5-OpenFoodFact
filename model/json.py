"""Actions with Json files."""
import json

class Json:
    """Functions to write and read the json file."""

    def save_connection_params(self, host, user, password):
        conn_params = {'host': host, 'user':user, 'password':password}
        with open('model/conn_params.json', 'w') as outfile:
            json.dump(conn_params, outfile)


    def read_connection_params(self):
        with open('model\conn_params.json') as json_file:
            params = json.load(json_file)
        return params['host'],params['user'],params['password']