"""Main file to launch program and install database."""

import argparse

from model.dbconfig import SQL_FILE
from model.dbconnection import DBconnect
from model.dbcreation import DBcreate
from model.sqlconfig import DBsql, DBname
from model.dbrequest import DBrequests
from model.dbinsertion import DBinsert
from controller.api_cleaner import Api_Requests



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
        ReadSQL = DBsql(SQL_FILE,verbose)
        sql_readed = ReadSQL.read_sql(SQL_FILE,verbose)
        # Write database name in dbname.py
        Database_name = DBname(sql_readed, verbose)
        Database_name.database_name(sql_readed, verbose)
        # Create database.
        Create_database = DBcreate(sql_readed, verbose)
        Create_database.create_db(sql_readed, verbose)
        # Retrieves the maximum number of characters for the fields (dictionary).
        Fields_charmax = DBrequests().characters_max()
        # Retrives datas from Api and reject unsuitable datas.
        Api_data = Api_Requests(Fields_charmax,verbose).api_get_data(Fields_charmax,verbose)
        # Insertion in database.
        DBinsert(Api_data, verbose).insert_data(Api_data, verbose)
        
    else:
        #application utilisateur en s'assurant que la bdd est correctement configuré, affichage du menu ect 
        print('RUN THE PROGRAM')


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