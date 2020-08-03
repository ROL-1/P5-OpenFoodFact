""" config file for api.py"""

REQUEST_PARAMS = [
    'action=process','tagtype_0=categories','tag_contains_0=contains',
    'json=1',
    'page_size=10',
    'fields='
]

FIELDS = 'product_name_fr,nutriscore_grade,stores,brands,code,categories,url'

CATEGORIES = ['Pizzas','Sandwichs','Sodas','Yaourts','Jambons']

# Minimum number of products by categories.
MIN_PROD = 5