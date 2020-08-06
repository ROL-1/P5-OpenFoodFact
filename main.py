"""Main file to launch program and install database."""

import argparse

from model.db_config import SQL_FILE
from model.db_connection import Db_connect
from model.db_creation import Db_create
from model.sql_read import Db_sql
from model.db_request import Db_requests
from model.db_insertion import Db_insert
from controller.api_requests import Api_requests
from view.interface import Ui



def main():
    """..."""
    parser = argparse.ArgumentParser(description="Launch the program !")
    parser.add_argument("-v", "--verbose", action="store_true", help="add output verbosity")
    parser.add_argument("--install_database", action="store_true", help="install database")
    args = parser.parse_args()
    verbose = args.verbose

    if args.verbose:
        print("Running '{}'".format(__file__))
    host, user, password = Ui().connection_params()

    if args.install_database: 
        # Server sql connection.
        Log = Db_connect(host, user, password)
        # Read sql.   
        sql_readed = Db_sql.read_sql(SQL_FILE,verbose)
        # Write database name in dbname.py
        Database_name = Db_sql.database_name(sql_readed, verbose)
        # Create database.
        Db_create.create_db(Log, sql_readed, verbose)
        # Retrieves the maximum number of characters for the fields (dictionary).
        Fields_charmax = Db_requests(Log).characters_max()
        # Retrives datas from Api and reject unsuitable datas.
        Api_data = Api_requests().api_get_data(Fields_charmax,verbose)
        # Insertion in database.
        Db_insert(Log, Api_data, verbose).insert_data(Api_data, verbose)
        
    else:
        # Server connection.
        Log = Db_connect(host, user, password)
        # Database connection.
        Log.database_log()
        # Booleans for loops.
        choice = False
        category = False 
        product_id = False
        substitute = False
        # Display menu. 
        Run = Ui()            
        while choice == False :
            choice = Run.menu()
        # Launch search for substitute.        
        if choice == 1 :
            # Display categories
            while category == False :
                category = Run.categories()
            # Display products.
            while product_id == False :
                product_id = Run.products(Log, category)
            # Display substitute
            while substitute == False :
                substitute = Run.substitute(Log, product_id, category)
            # Save result, leave or loop.

        # Display saved searches.
        elif choice == 2 :
            print('SAUVEGARDES')
        else:
            print('FAIL')


if __name__ == "__main__":

    main()


# Charge les données de l'api
# Filtre les données
# Vérifie si assez de produits par categories, sinon relance une recherche pour la categorie.
# Créé la BDD 
# Remplit la BDD
# Sollicite l'utilisateur (1. recherche 2.historique)
# Récupère dans la BDD la liste des catégories
# Affiche la liste des catégories
# Récupère dans la BDD la liste des produits de la catégorie
# Affiche la liste des produits de la catégorie
# Interroge l'api pour trouver un substitut ? (même catégorie, meilleur nutriscore)(ou dans la bdd ?)
# Affiche la fiche du substitut pour ce produit
# Propose de sauvegarder la recherche
# Retour au menu