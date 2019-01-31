import json
from pprint import pprint

import requests

# Part 1: Basics of calling an API with the requests library

# define which URL to use for the GitHub API
api_url = "https://api.github.com"

# Call the root of the api with GET, store the response
response = requests.get(api_url)

# Get the status code for the response. Should be 200 OK
print("Response status code is: ", response.status_code)

# Get the result as JSON
response_json = response.json()

# Part 2 - Accessing specific resources by URL
# Find out how many stars this repo has: https://github.com/nnja/new-computer

repo_endpoint = '/repos'
owner = '/nnja'
target_repo = '/new-computer'

# This will make a URL like:  https://api.github.com/repositories/nnja/new-computer
repo_url = api_url + repo_endpoint + owner + target_repo

# Call the repository API endpoint
repo_response = requests.get(repo_url)

# check that the status code was 200 OK, otherwise we did something wrong
print("Repos Status Code", repo_response.status_code)

# We get A LOT of data back.
print("Repo response data:")
repo_response_json = repo_response.json()
pprint(repo_response_json)

# We can pull out the information we want from the dictionary created from the JSON response, and ignore everything else.
watch_count = repo_response_json['watchers']
print("nnja's new-computer repository has %s watchers." % watch_count)

# Passing in bad info will result in a 404 (not found)
bad_response = requests.get("https://api.github.com/repositories/doesnt/exist")
print("Bad Response Status Code is:", bad_response.status_code)  # Status code is 404, meaning that resource doesn’t exist.

# We can use a search endpoint by passing in parameters
# Let's search for repositories based on criteria at this endpoint: /search/repositories
repo_search_url = api_url + '/search/repositories'

# Define some params you want to pass in.
# The options for what you can pass in and what you can expect back are generally defined in the API documentation.
params = {
    "q": "language:python",  # q stands for query
    "sort": "stars",  # sort criteria, in this case most stars
}

# Pass those params in with the request.
repo_search_response = requests.get(repo_search_url, params=params)

print("Repo Search Response Status Code is: ", repo_search_response)  # should be 200 OK

json_data = repo_search_response.json()

# Let's pick out the top 3 repos, the results are in the "items" key
top_3_repos = json_data['items'][:3]

# Now let's print some interesting information about these repos like their URL and number of stars
print("Printing info on top 3 Python repos by number of stars.")
for repo in top_3_repos:
    info = "%s repo has %s stars." % (repo["html_url"], repo["stargazers_count"])
    print(info)
