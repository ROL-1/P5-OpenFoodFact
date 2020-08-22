# P5-OpenFoodFact

## Objectif :
Créer un programme qui interagirait avec la base Open Food Facts pour en récupérer les aliments, les comparer et proposer à l'utilisateur un substitut plus sain à l'aliment qui lui fait envie.

-----------------
## Cahier des charges
### Description du parcours utilisateur

L'utilisateur est sur le terminal. Ce dernier lui affiche les choix suivants :

1 - Quel aliment souhaitez-vous remplacer ?  
2 - Retrouver mes aliments substitués.

L'utilisateur sélectionne 1.  
Le programme pose les questions suivantes à l'utilisateur et ce dernier sélectionne les réponses :

- Sélectionnez la catégorie. [Plusieurs propositions associées à un chiffre. L'utilisateur entre le chiffre correspondant et appuie sur entrée]
- Sélectionnez l'aliment. [Plusieurs propositions associées à un chiffre. L'utilisateur entre le chiffre correspondant à l'aliment choisi et appuie sur entrée]
- Le programme propose un substitut, sa description, un magasin ou l'acheter (le cas échéant) et un lien vers la page d'Open Food Facts concernant cet aliment.
- L'utilisateur a alors la possibilité d'enregistrer le résultat dans la base de données.

L'utilisateur sélectionne 2.  
Le programme retourne la liste des aliments substitués précédemment sauvegardés.
 
### Fonctionnalités

- Recherche d'aliments dans la base Open Food Facts.
- L'utilisateur interagit avec le programme dans le terminal, mais si vous souhaitez développer une interface graphique vous pouvez.
- Si l'utilisateur entre un caractère qui n'est pas un chiffre, le programme doit lui répéter la question.
- La recherche doit s'effectuer sur une base MySql.

-----------------
## Suivi du projet
Trello : https://trello.com/b/c5Zmq94p/p5-openfoodfacts

-----------------
## Programme
En étant dans le répertoire de base :

### Pré-requis
Le programme nécessite d'installer les dépendances présentes dans le requirements.txt, dans votre environnement virtuel (activé) ; avec la commande suivante :
```
pip install -r requirements.txt
```
### Premier lancement
ATTENTION : Le programme installera la base de données sur un serveur à partir du fichier .sql fourni. Le nom de la base de données est indiqué dans ce fichier. Si une base de données du même nom est déjà existante elle sera supprimée (les données seront alors perdues).

Il est donc nécessaire d'avoir accès à un serveur SQL et de renseigner ses informations de connexion au programme lors du premier lancement ; avec la commande suivante : 
```
main.py --install_database -v
```
L'option -verbose (-v) est disponible pour plus de lisibilité et faciliter les opérations de débug.

Cette commande peut être utilisée à tout moment pour réinitialiser la base de données et la remettre à jour avec de nouvelles données issues de l'api OpenFoodFact.

Etapes du programme d'installation :
- Sollicite la saisie par l'utilisateur des informations de connexion au serveur SQL (host,user,password).
- Vérifie que la connexion est possible.
- Lit le fichier .sql, passe les requêtes au serveur pour créer la base de données.
- Créé et passe les requêtes à l'API OpenFoodFact pour obtenir les informations sur les produits.
- Filtre et standardise les informations reçues pour ne retenir que les informations utiles pour le programme.
- Alimente la base de données avec les informations filtrées.
- Informe l'utilisateur que la base de donneés est installée. Il est alors possible de lancer le programme.

### Utilisation du programme
Le programme se lance avec la commande suivante :
```
main.py -v
```
L'option -verbose (-v) est disponible pour plus de lisibilité et faciliter les opérations de débug.

Il sera nécessaire de renseigner un nom d'utilisateur.

### Configuration du programme
- controller\api_config.py
    * REQUEST_PARAMS : contient les paramètres de l'endpoint de l'API, dont :  "page_size=xx" : permet de définir combien de produits par pages sont affichés (modifier cette valeur peut permettre d'accélérer l'obtention de la liste de produits retenus pour la base de données).  FIELDS : liste des champs à récupérer dans l'api.
    * CATEGORIES : il est possible de supprimer, remplacer ou ajouter des catégories souhaitées pour le programme de substitution.
    * MIN_PROD : permet de définir le nombre minimum de produits devant être retenus par categorie.

- model\config.py
    * SQL_FILE : nom du fichier sql utilisé.
    * NBPRODUCTS : nombre de produits à afficher à l'utilisateur lors du choix de produits à remplacer.
    * NUTRISCORE_MIN : nutriscore limite entre les produits à remplacer et les substituts.

-----------------
## Architecture du programme
### Lexique :
BDD : base de données.
### à la racine :
- DBOFF1.sql : requêtes pour la création de la BDD.
- main.py : lance le programme.
### controller :
- api_config : paramètres pour api_requests.
- api_requests : récupère les informations de l'API.
### model :
- config.py : paramètres pour connection.py.
- connection.py : gère la connection à la base de données et contiens les fonctions pour y récupérer les données.
- create.py : créé la base de données.
- fetch.py : requêtes à passer pour obtenir des informations de la BDD.
- insert : insert les informations dans la BDD.
- json : actions avec les fichiers .json.
- orm : fait office d'interface pour mettre en langage SQL les requêtes préparées dans requests_lists.py.
- requests_lists.py : listes de champs à passer dans orm.py pour créer les requêtes SQL.
- sql_read.py : lit le fichier SQL et récupère le nom de la BDD et l'enregistre dans database_name.json.
- conn_params.json : sauvegarde les informations de connexion au serveur SQL saisies par l'utilisateur.
- database_name.json : contient le nom de la BDD extrait du fichier SQL.
### view :
- interface : gère l'affichage destiné à l'utilisateur.
- menus : répertorie les menus sous forme de listes pour faciliter leurs modifications.
- sheets : sous menu d'affichage pour les produits et produits substituts.