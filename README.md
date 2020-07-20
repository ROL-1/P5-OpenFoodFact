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


Trello : https://trello.com/b/c5Zmq94p/p5-openfoodfacts

### Fichiers
Créer la base de données :
A partir du fichier DBOFF1.sql, avec la commande :
SOURCE <adresse du fichier>\DBOFF1.sql

MVC avec :  


MODEL :  
mysql.py : classe pour faire le lien entre la base de donnée et le programme  
VIEW :  
interface.py : classe gérant l'interface pour l'utilisateur (option)  
CONTROLER :  
main.py : lance l'application et distribue les autres fichiers  
program.py : le programme (algo)  
product.py : classe "fiche-produit"  
api.py : classe pour récupérer les infos de l'api  
user.py : classe pour la fiche client  
