#! /usr/bin/env python3
# coding: utf-8
"""config file for api_requests.py."""

REQUEST_PARAMS = [
    "action=process",
    "tagtype_0=categories",
    "tag_contains_0=contains",
    "json=1",
    "page_size=25",
    "fields=",
]

FIELDS = "generic_name_fr,product_name_fr,nutriscore_grade,\
stores,brands,code,categories,url"

# Add, delete or change categories.
CATEGORIES = ["Pizzas", "Sandwichs", "Sodas", "Chocolats", "Brioches"]

# Minimum number of products by categories.
MIN_PROD = 50
