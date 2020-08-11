"""Object-relational Mapper (ORM) class."""

class Orm():
    """Translate from ptyhon to sql."""
    def __init__(self, Log):
        self.Log = Log

    def simple_insertion(self, insert_lists):
        """Insert datas to database."""
        for args in insert_lists:
            string = args[-1]
            self.Log.execute("INSERT IGNORE INTO {} ({}) VALUES (%s)".format(*args),[string])

    def two_values_insertion(self, insert_lists):
        """Insert datas to database."""
        for args in insert_lists:           
            string = args[-1]
            self.Log.execute("INSERT IGNORE INTO {} VALUES (%s,%s)".format(*args),string)
    
    def triple_values_insertion(self, insert_lists):
        """Insert datas to database."""
        for args in insert_lists:           
            string = args[-1]
            self.Log.execute("INSERT IGNORE INTO {} ({}) VALUES (%s,%s,%s)".format(*args),string)
    
    def multiple_insertion(self, insert_lists):
        """Insert datas to database."""
        for args in insert_lists:
            string = args[-1]
            self.Log.execute("INSERT IGNORE INTO {} ({}) VALUES (%s,%s,%s,%s,%s,%s,%s)".format(*args),string)

    def simple_request(self, request_lists):
        """Insert datas to database."""
        result_list = []
        for args in request_lists:            
            string = args[-1]
            result = self.Log.request("SELECT {} FROM {} WHERE {} = (%s)".format(*args),[string])[0][0]
            result_list.append(result)
        return result_list
