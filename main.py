"""Main file to launch program and install database."""

import argparse
import json

from model.config import SQL_FILE
from model.connection import Connection
from model.create import Create
from model.sql_read import Db_sql
from model.fetch import Fetch
from controller.api_requests import Api_requests
from model.requests_lists import Requests_lists
from model.insert import Insert
from view.interface import Ui
from model.orm import Orm
from model.json import Json


def main():
    """..."""
    parser = argparse.ArgumentParser(description="Launch the program !")
    parser.add_argument("-v", "--verbose", action="store_true", help="add output verbosity")
    parser.add_argument("--install_database", action="store_true", help="install database")
    args = parser.parse_args()
    verbose = args.verbose

    if args.verbose:
        print("Running '{}'".format(__file__))    

    if args.install_database:
        # Ask parameters for sql server connection and save in Json.
        Run = Ui()
        host, user, password = Run.connection_params()
        Json().save_connection_params(host, user, password)        
        print('Installing...') 
        # Server sql connection.
        Log = Connection(host, user, password)
        # Read sql.   
        sql_readed = Db_sql.read_sql(SQL_FILE,verbose)
        # Write database name in dbname.py
        Db_sql.database_name(sql_readed, verbose)
        # Create database.
        Create.create_db(Log, sql_readed, verbose)
        # Retrieves the maximum number of characters for the fields (dictionary).
        Fields_charmax = Fetch(Log).characters_max()
        # Retrives datas from Api and reject unsuitable datas.
        Api_data = Api_requests().api_get_data(Fields_charmax,verbose)
        # Insertion in database.
        Insert(Log, Api_data, verbose).insert_data(Api_data, verbose)
        print('Database installed.')
        
    else:
        # Load connection parameters from json.
        host, user, password = Json().read_connection_params()
        # Server connection.
        Log = Connection(host, user, password)
        # Database connection.
        Log_db = Log.database_log()        
        # Booleans for loops.
        Loop = False
        log_choice = False
        # User account.
        Run = Ui()
        while log_choice == False:
            log_choice = Run.log_menu()
        # User log.
        if log_choice == 1:
            logged = False
            while logged == False:
                user_name = Run.log_user()
                request_lists = Requests_lists().user_id(user_name)            
                try:
                    user_id = Orm.simple_request(Log_db, request_lists)[0]
                    logged = True
                except IndexError:
                    print("Ce nom d'utilisateur n'existe pas.")
        # User create account.
        elif log_choice == 2:
            user_name = Run.create_user()
            insert_lists = Requests_lists().user_insert(user_name)
            Insert(Log_db).insert_user(insert_lists)
            request_lists = Requests_lists().user_id(user_name)
            user_id = Orm.simple_request(Log_db, request_lists)[0]

        while Loop == False:
            # Booleans for loops.
            menu_choice = False
            category = False 
            product_id = False
            substitute_id = False
            save_choice = False
            # Display menu.
            while menu_choice == False:
                menu_choice = Run.menu()
            # Launch search for substitute.        
            if menu_choice == 1 :
                # Display categories
                while category == False:
                    category = Run.categories()
                # Display products.
                while product_id == False:
                    product_id = Run.products(Log, category)
                # Display substitute
                while substitute_id == False:
                    substitute_id = Run.substitute(Log, product_id, category)
                # Save result, leave or loop.
                while save_choice == False:
                    save_choice = Run.save_menu(Log)
                if save_choice == 1:
                    insert_lists = Requests_lists().save_search(product_id, substitute_id, user_id)
                    Insert(Log_db).insert_save(insert_lists)
                    print('Recherche sauvegardée.') 
                elif save_choice == 2:
                    exit()                    

            # Display saved searches.
            elif menu_choice == 2:
                Run.saves_display(Log_db, user_id)

        # Close connection
        if args.verbose:
            print("Close connection.")
        Log_db.close_connection()

if __name__ == "__main__":

    main()
