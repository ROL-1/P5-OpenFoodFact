#! /usr/bin/env python3
# coding: utf-8
"""class to get informations from API."""

import json

import requests

from controller.api_config import CATEGORIES, FIELDS, MIN_PROD, REQUEST_PARAMS


class ApiRequests:
    """Create requests for api."""

    def __init__(self, Fields_charmax=None, verbose=None):
        """Get datas from api by looping on each category until it's filled."""
        if verbose:
            print("Getting data from API...")
        self.scraped = []
        self.cleaned_scraped = []
        self.endpoint = "https://fr.openfoodfacts.org/cgi/search.pl?"
        self.page_nb = 1

    def api_request(self, category):
        """Get datas from api by creating endpoint with parameters."""
        params = (
            "&".join(REQUEST_PARAMS) + FIELDS + "&page=" +
            str(self.page_nb) + "&tag_0="
        )
        request = requests.get(self.endpoint + params + category)
        return request

    def add_scraped(self, request):
        """Add products in list scraped."""
        load = json.loads(request.text)
        for product in load["products"]:
            self.scraped.append(product)

    def define_category(self, product):
        """Check 1 : Change 'categories' to class the product in database."""
        search_category = True
        i = 0
        while search_category and i < len(CATEGORIES):
            for category in CATEGORIES:
                if category in product["categories"].split(", "):
                    product["categories"] = category
                    search_category = False
                i += 1
        if search_category:
            product["categories"] = ""

    def wrong_caracters(self, product):
        """Check 2 : Empty string if there is a forbiden caracter."""
        for field, string in product.items():
            if ("\n" or "\t" or "\r") in string:
                product[field] = ""

    def data_missing(self, product):
        """Check 3 : if field or data is missing."""
        # Field missing
        for field in FIELDS.split(","):
            if field not in product.keys():
                return "False"
        # String missing
        for string in product.values():
            if string == "":
                return "False"

    def string_length(self, Fields_charmax, product):
        """Check 4 : if string is too long for database field."""
        for field, string in product.items():
            # Excludes verification for the 'injection' field.
            if field != "injection":
                # Check for fields with characters_max().
                if field in Fields_charmax.keys():
                    # Check for element with max length for 'stores'.
                    if field == "stores":
                        if len(max(string.split(","), key=len)) > Fields_charmax[field]:
                            return "False"
                    else:
                        if len(string) > Fields_charmax[field]:
                            return "False"

    def products_nb(self, cleaned_scraped, category):
        """Check how many products by categories are suitables."""
        products_nb = 0
        for product in cleaned_scraped:
            if category == product["categories"]:
                products_nb += 1
        if products_nb < MIN_PROD:
            category_filled = False
        else:
            category_filled = True
        return category_filled

    def api_get_data(self, Fields_charmax, verbose):
        """Review categories until there is 'MIN_PROD' products for each."""

        for category in CATEGORIES:
            if verbose:
                print("Loading", category)
            category_filled = False
            # Loop while there is not enough products for the category.
            while category_filled is False:
                # Create request.
                request = self.api_request(category)
                # Add products from the request to 'scraped' list.
                self.add_scraped(request)
                if verbose:
                    print("Cleaning data for", category)
                # Review products.

                for product in self.scraped:
                    # Change "categories" product field for only one category, or nothing if not in 'CATEGORIES' list.
                    self.define_category(product)
                    # Erease string if there is a forbidden character.
                    self.wrong_caracters(product)
                    # Check datas.
                    Data = self.data_missing(product)
                    Strings = self.string_length(Fields_charmax, product)
                    # Fill 'cleaned_scraped' list with product if all checks are true.
                    if (
                        ("categories" in product)
                        and (category in product["categories"])
                        and (Data != "False")
                        and (Strings != "False")
                    ):
                        self.cleaned_scraped.append(product)
                # Check how many products by categories are suitables.
                category_filled = self.products_nb(
                    self.cleaned_scraped, category)
                if category_filled is False:
                    self.page_nb += 1
                else:
                    self.page_nb = 1

        if verbose:
            print(
                "Datas cleaned. Founded", MIN_PROD, "products minimum by categories.",
            )

        # # Write JSON for debug
        # with open("scraped_file.json", "w") as write_file:
        #     json.dump(self.cleaned_scraped, write_file, indent=4)
        return self.cleaned_scraped
