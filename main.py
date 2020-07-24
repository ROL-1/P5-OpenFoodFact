"""main file to launch program"""

import argparse

from controller.dbcreation import DBcreation
from controller.dbconnection import DBconnect
from controller.dbconfig import SQL_FILE

parser = argparse.ArgumentParser(description="Launch the program !")
parser.add_argument("-v", "--verbose", action="store_true", help="add output verbosity")
parser.add_argument("--install_database", action="store_true", help="install database")
args = parser.parse_args()
# answer = args.x**args.y
if args.verbose:
    print("Running '{}'".format(__file__))

if args.install_database:       
    # Connect to database.
    Testlog = DBconnect()
    
    # Création des tables en python
    #  soit passer par un sql (comme tu as fait) et que tu parse pour ensuite faire appel à cursor.execute
    #  SOIT tu découpe en méthode de classe
    #  et tu écrit directement dans chaque méthode cursor.execute('CREATE...) ce qui t'évitera de devoir parser le fichier sql.
    TESTcreate = DBcreation(SQL_FILE,args.verbose)

    # appel à l'api avec une boucle sur les catégories (données statiques que tu définis toi en config pareil)
    # et appels vers l'api pour récup les infos catégory,product et shop (avec parsing/filtrage des données)

    # Insertion en bdd des résultats après filtrage.

    # Disconnect from database.
    Testlog.close_connection 
else:
    #application utilisateur en s'assurant que la bdd est correctement configuré, affichage du menu ect 
    print('RUN THE PROGRAM')
# print(answer)

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