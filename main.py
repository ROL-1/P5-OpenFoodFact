"""Main file to launch program and install database."""

import argparse

from controller.dbconfig import SQL_FILE
from controller.dbconnection import DBconnect
from controller.dbcreation import DBcreation
from controller.dbrequest import DBrequests
from controller.dbinsertion import DBinsert
from controller.api_cleaner import Api_Requests#, Api_Cleaner



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

    if args.install_database: 
        # Create database.   
        # Create_database = DBcreation(SQL_FILE,verbose)
        # Retrieves the maximum number of characters for the fields (dictionary).
        Fields_charmax = DBrequests().characters_max()
        # Retrives datas from Api and reject unsuitable datas.
        Api_data = Api_Requests(Fields_charmax,verbose).api_get_data(Fields_charmax,verbose)
        # Insertion in database.
        DBinsert(Api_data, verbose).insert_data(Api_data, verbose)

        
    else:
        #application utilisateur en s'assurant que la bdd est correctement configuré, affichage du menu ect 
        print('RUN THE PROGRAM')


    # # Disconnect from MySQL Server.
    # Log.close_connection 

if __name__ == "__main__":

    main()


# group = parser.add_mutually_exclusive_group()
# group.add_argument("-v", "--verbose", action="store_true")
# group.add_argument("-q", "--quiet", action="store_true")
# parser.add_argument("x", type=int, help="the base")
# parser.add_argument("y", type=int, help="the exponent")
# if args.quiet:
#     print(answer)
# elif args.verbose:
#     print("{} to the power {} equals {}".format(args.x, args.y, answer))
# else:
#     print("{}^{} == {}".format(args.x, args.y, answer))


# Charge les données de l'api
# Filtre les données
    # NON Sauvegarde les données dans un json 
# Créé la BDD (optionel ?)
# Remplit la BDD
# Vérifie la BDD si qté pas atteinte par catégories = relance Remplit la BDD
# Sollicite l'utilisateur (1. recherche 2.historique)
# Récupère dans la BDD la liste des catégories
# Affiche la liste des catégories
# Récupère dans la BDD la liste des produits de la catégorie
# Affiche la liste des produits de la catégorie
# Interroge l'api pour trouver un substitut ? (même catégorie, meilleur nutriscore)(ou dans la bdd ?)
# Affiche la fiche du substitut pour ce produit
# Propose de sauvegarder la recherche
# Retour au menu