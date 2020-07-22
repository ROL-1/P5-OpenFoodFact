""" config file for api.py"""

# page=x
#  https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&json=1&page_size=150
# &fields=product_name_fr,nutriscore_grade,stores,brands,code,categories,url&tag_0=Yaourts sucrés

REQUEST_PARAMS = [
    'action=process','tagtype_0=categories','tag_contains_0=contains',
    'json=1',
    'page_size=150',
    'fields='
]

FIELDS = 'product_name_fr,nutriscore_grade,stores,brands,code,categories,url'

CATEGORIES = ['Pizzas','Sandwichs','Pâtes à tartiner','Yaourts sucrés','Jambons crus']