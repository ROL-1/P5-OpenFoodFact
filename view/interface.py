"""Interface with user."""

from model.db_request import Db_requests
from model.db_config import NBPRODUCTS
from controller.api_config import CATEGORIES
from view.sheets import Sheets
from getpass import getpass

class Ui:
    """Allows the user to interact with the program."""

    def __init__(self):
        """..."""
        # Counter for welcome message input.
        self.menu_counter = 0
    
    def connection_params(self):
        """Get parameters for connection to server sql."""
        print('Veuillez saisir les paramètres de connection au serveur sql:')
        host = input('host : ')
        user = input('user : ')
        password = getpass()
        return host, user, password
 

    def _user_choices(self, user_input, choices):
        """Manage user choices."""
        try:
            user_input = int(user_input)
            for i in range(choices):
                if (user_input < 1) or (user_input > choices):
                    print("Ce n'est pas un choix valide.")
                    return False
                elif (i+1) == user_input:                    
                    return (i+1)
        except ValueError:
            print("Ce n'est pas un choix valide.")
            return False
    
    def menu(self):
        """Display the proposals to the user."""
        # Welcome message
        self.menu_counter +=1
        if self.menu_counter == 1:
            print("\nBIENVENUE DANS LE PROGRAMME DE RECHERCHE DE PRODUITS DE SUBSTITUTION.\n",
                "Par l'entreprise Pur Beurre.\n",
                "Avec l'api OpenFoodFact\n")
        # Main menu.
        print("\nVoulez-vous :\n",
              "1. - Trouver un produit de substitution pour un aliment ? - (Appuyez sur 1.)\n",
              "2. - Consulter vos produits de substitution sauvegardés ? - (Appuyez sur 2.)\n",
                )
        # User's choices.
        choices = 2
        user_input = input("Votre choix : ")
        choice = self._user_choices(user_input, choices)
        # Loop if wrong choice, else return choice.
        if choice == False:
            return False
        else:
            return choice

    def categories(self):
        """Display categories to the user."""
        # Categories menu.
        print("\nPour quelle catégorie de produits voulez-vous faire une recherche ?")
        print("Sélectionnez une catégorie :\n")        
        for count, cat in enumerate(CATEGORIES):
            print(count+1,'-', cat)
        # User's choices.
        choices = len(CATEGORIES)
        user_input = input("\nVotre choix : ")
        choice = self._user_choices(user_input, choices)    
        # Loop if wrong choice, else return category.
        if choice == False:
            return False
        else:
            for count, category in enumerate(CATEGORIES):
                if choice == (count+1):
                    return category
    
    def products(self, Log, category):
        """Display products to the user."""
        # Products menu.
        print(f"\nDans la categorie {category},")
        print("vous pouvez rechercher un substitut pour un des produits suivant :")
        print("Sélectionnez un produit.\n")
        fetched_products = Db_requests(Log).fetch_products(category)        
        for count, product in enumerate(fetched_products):
            Sheets.list_sheet(count, product)
        # User's choices.
        choices = NBPRODUCTS
        user_input = input("\nVotre choix : ")
        choice = self._user_choices(user_input, choices)
        # Loop if wrong choice, else return product_id.
        if choice == False:
            return False           
        else:
            for i in range(NBPRODUCTS):
                if i+1 == choice:                
                    product_id = fetched_products[choice-1][0]
                    return product_id

    def substitute(self, Log, product_id, category):
        """Display substitute to the user."""
        # Substitute display.
        substitute = Db_requests(Log).fetch_substitute(category)
        stores = Db_requests(Log).fetch_stores(substitute[0][0]) 
        print(f'\nLe produit suivant obtient un meilleur Nutriscore, dans la catégorie: {category}\n')
        Sheets.sheet(substitute[0], stores)
        # Substituted product display.
        print('\nCe produit peut substituer le produit que vous aviez sélectionné :\n')
        old_product = Db_requests(Log).fetch_product(product_id)
        stores = Db_requests(Log).fetch_stores(old_product[0][0])
        Sheets.sheet(old_product[0], stores)


    