"""ROM class."""

class Rom():
    """Translate from ptyhon to sql."""

    def simple_insertion(Log, insert_lists):
        """Insert datas to database."""
        for args in insert_lists:
            # table = insert_list[0]
            # column = insert_list[1]
            string = args[-1]
            Log.execute("INSERT IGNORE INTO {} ({}) VALUES (%s)".format(*args),[string])

    def two_values_insertion(Log, insert_lists):
        """Insert datas to database."""
        for args in insert_lists:           
            string = args[-1]
            Log.execute("INSERT IGNORE INTO {} VALUES (%s,%s)".format(*args),string)
    
    def multiple_insertion(Log, insert_lists):
        """Insert datas to database."""
        for args in insert_lists:
            string = args[-1]
            Log.execute("INSERT IGNORE INTO {} ({}) VALUES (%s,%s,%s,%s,%s,%s)".format(*args),string)

    def simple_request(Log, request_lists):
        """Insert datas to database."""
        result_list = []
        for args in request_lists:
            string = args[-1]
            result = Log.request("SELECT {} FROM {} WHERE {} = (%s)".format(*args),[string])[0][0]
            result_list.append(result)
        return result_list