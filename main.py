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

    # # Connect to MySQL Server.
    # Log = DBconnect()
    # Log.connection()

    if args.install_database: 
        # Read sql.   
        sql_readed = Db_sql.read_sql(SQL_FILE,verbose)
        # Write database name in dbname.py
        Database_name = Db_sql.database_name(sql_readed, verbose)
        # Create database.
        Db_create.create_db(sql_readed, verbose)
        # Retrieves the maximum number of characters for the fields (dictionary).
        Fields_charmax = Db_requests().characters_max()
        # Retrives datas from Api and reject unsuitable datas.
        Api_data = Api_requests(Fields_charmax,verbose).api_get_data(Fields_charmax,verbose)
        # Insertion in database.
        Db_insert(Api_data, verbose).insert_data(Api_data, verbose)
        
    else:
        #application utilisateur en s'assurant que la bdd est correctement configuré, affichage du menu ect 
        Menu = Ui()


    # # # Disconnect from MySQL Server.
    # Log.close_connection 

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