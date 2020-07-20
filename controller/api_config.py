""" config file for api.py"""

# page=x
#  https://world.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0=cereals
research_params = [
    'action=process','tagtype_0=categories','tag_contains_0=contains',
    'tag_0=coffee',
    'json=1',
    'page_size=150',
    'fields=product_name,nutriscore_grade,stores,brands,code,categories,url',
]