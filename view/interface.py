#! /usr/bin/env python3
# coding: utf-8
"""Interface with user."""

from getpass import getpass

from controller.api_config import CATEGORIES
from model.config import NBPRODUCTS
from model.fetch import Fetch
from view.menus import menus
from view.sheets import Sheets


class Ui:
    """Allows the user to interact with the program."""

    def __init__(self):
        # Counter for welcome message input.
        self.menu_counter = 0

    def connection_params(self):
        """Ask parameters for connection to server sql."""
        print(
            "\nVeuillez saisir les paramètres de connection au serveur sql:"
        )
        host = input("host : ")
        user = input("user : ")
        password = getpass()
        return host, user, password

    def print_menu(self, sub_menu):
        for line in menus[sub_menu]:
            print(line)

    def log_menu(self):
        """Log menu."""
        self.print_menu("log_menu")
        self.print_menu("log_menu_choices")
        choices = len(menus["log_menu_choices"])
        user_input = input("\n Votre choix : ")
        log_choice = self._user_choices(user_input, choices)
        if log_choice == False:
            return False
        else:
            return log_choice

    def log_user(self):
        """Ask user informations, to log."""
        print("\nConnexion au compte utilisateur :")
        print("\nSaisissez votre nom d'utilisateur :")
        log_user = input("Votre choix : ")
        if log_user == "":
            return False
        else:
            return log_user

    def create_user(self):
        """Ask user informations, to register."""
        print("\nCréer un compte utilisateur :")
        print("\nChoisissez un nom d'utilisateur (25 caractères maximum) :")
        user_name = input("Votre choix : ")
        if user_name == "":
            return False
        else:
            return user_name

    def _user_choices(self, user_input, choices):
        """Manage user choices."""
        try:
            user_input = int(user_input)
            for i in range(choices):
                if (user_input < 1) or (user_input > choices):
                    print("Ce n'est pas un choix valide.")
                    return False
                elif (i + 1) == user_input:
                    return i + 1
        except ValueError:
            print("Ce n'est pas un choix valide.")
            return False

    def menu(self):
        """Display the proposals to the user."""
        # Welcome message
        self.menu_counter += 1
        if self.menu_counter == 1:
            self.print_menu("main_menu_welcome")
        # Main menu.
        self.print_menu("main_menu")
        self.print_menu("main_menu_choices")
        # User's choices.
        choices = len(menus["main_menu_choices"])
        user_input = input("Votre choix : ")
        menu_choice = self._user_choices(user_input, choices)
        # Loop if wrong choice, else return choice.
        if menu_choice == False:
            return False
        else:
            return menu_choice

    def categories(self):
        """Display categories to the user."""
        # Categories menu.
        self.print_menu("categories_menu")
        for count, cat in enumerate(CATEGORIES):
            print(count + 1, "-", cat)
        # User's choices.
        choices = len(CATEGORIES)
        user_input = input("\nVotre choix : ")
        choice = self._user_choices(user_input, choices)
        # Loop if wrong choice, else return category.
        if choice == False:
            return False
        else:
            for count, category in enumerate(CATEGORIES):
                if choice == (count + 1):
                    return category

    def products(self, Log, category):
        """Display products to the user."""
        # Products menu.
        print(f"\nDans la categorie {category},")
        self.print_menu("products_menu")
        fetched_products = Fetch(Log).fetch_products(category)
        Sheets.list_sheet(fetched_products)

        # User's choices.
        choices = NBPRODUCTS
        user_input = input("\nVotre choix : ")
        choice = self._user_choices(user_input, choices)
        # Loop if wrong choice, else return product_id.
        if choice == False:
            return False
        else:
            for i in range(NBPRODUCTS):
                if i + 1 == choice:
                    product_id = fetched_products[choice - 1][0]
                    return product_id

    def substitute(self, Log, product_id, category):
        """Display substitute to the user."""
        # Substitute display.
        substitute = Fetch(Log).fetch_substitute(category)
        stores = Fetch(Log).fetch_stores(substitute[0][0])
        print(
            f"\nLe produit suivant obtient un meilleur Nutriscore, dans la catégorie: {category}\n"
        )
        Sheets.sheet(substitute[0], stores)
        # Substituted product display.
        print(
            "\nCe produit peut substituer le produit que vous aviez sélectionné :\n"
        )
        old_product = Fetch(Log).fetch_product(product_id)
        stores = Fetch(Log).fetch_stores(old_product[0][0])
        Sheets.sheet(old_product[0], stores)
        return substitute[0][0]

    def save_menu(self, Log):
        """Save or loop to menu."""
        self.print_menu("save_menu")
        self.print_menu("save_menu_choices")
        choices = len(menus["save_menu_choices"])
        user_input = input("Votre choix : ")
        save_choice = self._user_choices(user_input, choices)
        if save_choice == False:
            return False
        else:
            return save_choice

    def saves_display(self, Log, user_id):
        """Display searches saved."""
        fetched_products = Fetch(Log).fetch_saved_searches(user_id)
        if fetched_products == []:
            print("Vous n'avez aucune recherche sauvegardée.")
        else:
            print("\n Voici vos anciennes recherches :")
            Sheets.saves_sheet(fetched_products)

    def bye_message(self, user_name):
        if user_name != False:
            print('\nA bientôt "{}" !'.format(user_name))
        else:
            print("\nA bientôt !")
