#! /usr/bin/env python3
# coding: utf-8
"""Main file to launch program and install database."""

import argparse

from controller.api_requests import ApiRequests
from model.config import SQL_FILE
from model.connection import Connection
from model.create import Create
from model.fetch import Fetch
from model.insert import Insert
from model.json import Json
from model.orm import Orm
from model.requests_lists import RequestsLists
from model.sql_read import SqlRead
from view.interface import Ui


def main():
    """Main file for substitute program from 'Pur Beurre'."""
    try:
        parser = argparse.ArgumentParser(description="Launch the program !")
        parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="add output verbosity",
        )
        parser.add_argument(
            "--install_database", action="store_true", help="install database"
        )
        args = parser.parse_args()
        verbose = args.verbose

        if args.verbose:
            print("Running '{}'".format(__file__))

        if args.install_database:
            # Ask parameters for sql server connection and save in Json.
            Run = Ui()
            host, user, password = Run.connection_params()
            Json().save_connection_params(host, user, password)
            print("Installing...")
            # Server sql connection.
            Log = Connection(host, user, password)
            # Read sql.
            Sql = SqlRead(verbose)
            sql_readed = Sql.read_sql(SQL_FILE)
            # Write database name in dbname.py
            Sql.database_name(sql_readed)
            # Create database.
            Create(Log, sql_readed).create_db(verbose)
            # Retrieves the maximum number of characters for the fields.
            Fields_charmax = Fetch(Log).characters_max()
            # Retrives datas from Api and reject unsuitable datas.
            Api_data = ApiRequests().api_get_data(Fields_charmax, verbose)
            # Insertion in database.
            Insert(Log, verbose).insert_data(Api_data)
            print("Database installed.")

        else:
            try:
                with open("model/conn_params.json"):
                    pass
                with open("model/database_name.json"):
                    pass
            except IOError:
                print(
                    "\nInformations de connection manquantes.\n",
                    "Veuillez utiliser l'option : --install_database\n",
                )
                exit()
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
            user_name = False
            Run = Ui()
            while log_choice is False:
                log_choice = Run.log_menu()
            # User log.
            if log_choice == 1:
                logged = False
                while logged is False:
                    user_name = Run.log_user()
                    if isinstance(user_name, str):
                        try:
                            request_lists = RequestsLists().user_id(user_name)
                            user_id = Orm(Log_db).simple_request(
                                request_lists
                            )[0]
                            logged = True
                        except IndexError:
                            print("\n- Ce nom d'utilisateur n'existe pas.")
                    else:
                        print("\n- Veuillez saisir un nom d'utilisateur.")
            # User create account.
            elif log_choice == 2:
                while user_name is False:
                    user_name = Run.create_user()
                    try:
                        request_lists = RequestsLists().user_id(user_name)
                        user = Orm(Log_db).simple_request(request_lists)
                        user_name = False
                        print("\nCe nom d'utilisateur existe déjà.")
                    except IndexError:
                        insert_lists = RequestsLists().user_insert(user_name)
                        Insert(Log_db, verbose).insert_user(insert_lists)
                        request_lists = RequestsLists().user_id(user_name)
                        user_id = Orm(Log_db).simple_request(request_lists)[0]

            while Loop is False:
                # Booleans for loops.
                menu_choice = False
                category = False
                product_id = False
                substitute_id = False
                save_choice = False
                # Display menu.
                while menu_choice is False:
                    menu_choice = Run.menu()
                # Launch search for substitute.
                if menu_choice == 1:
                    # Display categories
                    while category is False:
                        category = Run.categories()
                    # Display products.
                    while product_id is False:
                        product_id = Run.products(Log, category)
                    # Display substitute
                    while substitute_id is False:
                        substitute_id = Run.substitute(
                            Log, product_id, category
                        )
                    # Save result, leave or loop.
                    while save_choice is False:
                        save_choice = Run.save_menu(Log)
                    if save_choice == 1:
                        insert_lists = RequestsLists().save_search(
                            product_id, substitute_id, user_id
                        )
                        Insert(Log_db, verbose).insert_save(insert_lists)
                        print("\nRecherche sauvegardée.")
                    elif save_choice == 2:
                        pass
                    elif save_choice == 3:
                        exit(Ui().bye_message(user_name))

                # Display saved searches.
                elif menu_choice == 2:
                    Run.saves_display(Log_db, user_id)
                # Quit.
                elif menu_choice == 3:
                    exit(Ui().bye_message(user_name))

    except KeyboardInterrupt:
        Ui().bye_message(user_name)


if __name__ == "__main__":

    main()
