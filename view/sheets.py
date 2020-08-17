#! /usr/bin/env python3
# coding: utf-8
"""Structure for products sheets."""

import pandas as pd


class Sheets:
    """Give structure for products sheets."""

    def sheet(product, stores):
        """Sheet."""
        print("Nom :", product[1])
        print("Description :", product[2])
        print("Marque :", product[3])
        print("Nutriscore :", product[4])
        # Remove unwanted characters in 'stores'.
        stores = str(stores)  # TC
        remove_char = ["[", "(", "'", "]"]
        stores = stores.replace(",)", "")
        for char in remove_char:
            stores = stores.replace(char, "")
        print("Magasins :", stores)
        print("Lien OpenFoodFact :", product[5])

    def list_sheet(fetched_products):
        """Product list sheet."""
        nutriscores = []
        brands = []
        products = []
        for fp in fetched_products:
            nutriscores.append(fp[4])
            brands.append(fp[3])
            products.append(fp[1])
        frame = pd.DataFrame(
            {
                "Nutriscores": nutriscores,
                "Produits": products,
                "Marques": brands,
            }
        )
        frame.index = [i + 1 for i in range(len(fetched_products))]
        print(frame)

    def saves_sheet(fetched_products):
        """Searches saved list sheet."""
        # Create lists for frame.
        products = []
        substitutes = []
        codeOFF = []
        for fp in fetched_products:
            products.append(fp[0])
            substitutes.append(fp[1])
            codeOFF.append(fp[2])
        # Create frame.
        frame = pd.DataFrame(
            {
                "Produits": products,
                "Substituts": substitutes,
                "https://fr.openfoodfacts.org/": codeOFF,
            }
        )
        frame.index = [i + 1 for i in range(len(fetched_products))]
        print(frame)
