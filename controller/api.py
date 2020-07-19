#! /usr/bin/env python3
# coding: utf-8

"""class to get informations from API."""

import json
import requests

import api_config


def api_request():
    """Create request to pass to the getter and decode the json (dictionary)."""
    endpoint = 'https://fr.openfoodfacts.org/cgi/search.pl?'
    params = '&'.join(api_config.research_params)
    request = requests.get(endpoint+params)
    print(endpoint+params) #To Clean
    scraped = json.loads(request.text)   
    print(type(scraped)) #To Clean
    print(scraped['products'][0])
    with open("scraped_file.json", "w") as write_file:
        json.dump(scraped, write_file, indent=4)

api_request()



# https://realpython.com/python-json/
# with open("data_file.json", "w") as write_file:
#     json.dump(data, write_file)

# Ou, si vous étiez disposé à continuer à utiliser ces données JSON sérialisées dans votre programme, vous pourriez les écrire dans un strobjet Python natif .

# json_string = json.dumps(data)


# # Map of userId to number of complete TODOs for that user
# todos_by_user = {}

# # Increment complete TODOs count for each user.
# for todo in todos:
#     if todo["completed"]:
#         try:
#             # Increment the existing user's count.
#             todos_by_user[todo["userId"]] += 1
#         except KeyError:
#             # This user has not been seen. Set their count to 1.
#             todos_by_user[todo["userId"]] = 1

# # Create a sorted list of (userId, num_complete) pairs.
# top_users = sorted(todos_by_user.items(), 
#                    key=lambda x: x[1], reverse=True)

# # Get the maximum number of complete TODOs.
# max_complete = top_users[0][1]

# # Create a list of all users who have completed
# # the maximum number of TODOs.
# users = []
# for user, num_complete in top_users:
#     if num_complete < max_complete:
#         break
#     users.append(str(user))

# max_users = " and ".join(users)

# # Define a function to filter out completed TODOs 
# # of users with max completed TODOS.
# def keep(todo):
#     is_complete = todo["completed"]
#     has_max_count = str(todo["userId"]) in users
#     return is_complete and has_max_count

# # Write filtered TODOs to file.
# with open("filtered_data_file.json", "w") as data_file:
#     filtered_todos = list(filter(keep, todos))
#     json.dump(filtered_todos, data_file, indent=2)

