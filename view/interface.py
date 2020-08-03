"""Interface with user."""


from model.db_request import Db_requests
from model.db_config import NBPRODUCTS
from controller.api_config import CATEGORIES

class Ui():
    """Allows the user to interact with the program."""

    def __init__(self):
        """..."""
        self.menu_counter = 0
        self.menu()

    def _user_choices(self, user_input, choices):
        """Manage user choices."""
        try:
            int(user_input)
            for i in range(choices):
                if (int(user_input) < 1) or (int(user_input) > choices):
                    print("Ce n'est pas un choix valide.")
                    return False
                elif int(user_input) == i+1:
                    print('vous avez fait le choix : ',i+1)
                    return (i+1)
        except ValueError:
            print("Ce n'est pas un choix valide.")
            return False
    
    def menu(self):
        """Display the proposals to the user."""
        self.menu_counter +=1
        if self.menu_counter == 1:
            print("\nBIENVENUE DANS LE PROGRAMME DE RECHERCHE DE PRODUITS DE SUBSTITUTION.\nPar l'entreprise Pur Beurre.\n")        
        print("\nVoulez-vous :\n",
              "1. - Trouver un produit de substitution pour un aliment ? - (Appuyez sur 1.)\n",
              "2. - Consulter vos produits de substitution sauvegardés ? - (Appuyez sur 2.)\n",
                )
        choices = 2
        user_input = input("Votre choix : ")
        choice = self._user_choices(user_input, choices)
        if choice != False:
            if choice == 1 :
                self.categories()
            elif choice == 2 :
                print('SAUVEGARDES')
            else:
                self.menu()
        else:
            self.menu()

    def categories(self):
        """Display categories to the user."""
        print("\nSur quelle catégorie de produits voulez-vous faire une recherche ?")
        for count, category in enumerate(CATEGORIES):
            print(count+1,'-', category)
        choices = len(CATEGORIES)
        user_input = input("\nVotre choix : ")
        choice = self._user_choices(user_input, choices)
        if choice != False:
            for count, category in enumerate(CATEGORIES):
                if choice == (count+1):                    
                    self.products(category)
                    return ################## OK ? 
            self.categories()
        else:
            self.categories()
    
    def products(self, category):
        """Display products to the user."""
        print(f"\nDans la categorie {category},")
        print("vous pouvez rechercher un substitut pour un des produits suivant :\n")
        fetched_products = Db_requests().fetch_products(category)
        for count, product in enumerate(fetched_products):
            print(count+1,'-',product)
        choices = NBPRODUCTS
        user_input = input("\nVotre choix : ")
        choice = self._user_choices(user_input, choices)
        if choice != False:
            for i in range(NBPRODUCTS):
                if i+1 == choice:                
                    self.substitute(fetched_products[choice-1][0], category)
                    return ################## OK ? 
            self.products(category)
        else:
            self.products(category)

    def substitute(self, product_id, category):
        """Display substitute to the user."""
        substitute = Db_requests().fetch_substitute(category)
        print('\nLe produit suivant obtient un meilleur Nutriscore, dans la même Catégorie:')
        print(substitute[0])
        print('\nCe produit peut substituer le produit que vous aviez sélectionné :')
        old_product = Db_requests().fetch_product(product_id)
        print(old_product[0])
    