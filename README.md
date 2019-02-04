# A Quick Intro to using Python and [`requests`](https://github.com/requests/requests) to work with APIs in 45 minutes

In this screencast you'll learn a bit about the anatomy of an API call, what to look for in a request and response, and how to differentiate HTTP status codes. With this foundation, you'll learn the basics of using the popular [`requests`](https://github.com/requests/requests) library and Python to work with APIs.

### Who am I?

I'm Nina Zakharenko, a Senior Cloud Developer Advocate at Microsoft focusing on Python. Before joining Microsoft, I was a Senior Software Engineer with over a decade of experience writing software for companies like Reddit, Meetup, and HBO.

I'm nnja around the web. Follow me on:
- [Twitter](https://twitter.com/nnja)
- [GitHub](https://github.com/nnja)
- [LinkedIn](https://linkedin.com/in/nnja)

Repo will live at: https://github.com/nnja/learn_requests

I'm going to go fast today because I want to get through a lot of material. Don't worry if you can't keep up -- all the material is on GitHub, and the screencast can be watched again. What's important is the concepts.

Lastly, don't click through the links. Those are meant to be read and researched after, not during, the workshop.

### Pre-requisites
- Python3 Installed https://realpython.com/installing-python/
- Visual Studio Code Installed https://code.visualstudio.com/docs/languages/python?WT.mc_id=winfosec-cast-ninaz
- [Python Extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- *(Optional)* install the [`requests`](https://github.com/requests/requests) library. If you don’t know how, I’ll cover the topic in the first few minutes of the session.

## Checking pre-requisites

*Make sure that Python 3 is installed*

```shell
$ python3 --version
```

**Should return version 3.6 or higher.**

```shell
$ code
```

*Should open Visual Studio Code.*

# Step 1: Open Visual Studio Code

[Visual Studio Code](https://code.visualstudio.com/?WT.mc_id=winfosec-cast-ninaz) is a lightweight cross platform editor from Microsoft. It works seamlessly on Linux, Mac, and Windows. It's also a great option for Python, which is why I'll be using it for the rest of the exercises.

If it's not already open from the previous step, you can open it by typing:

```shell
$ code
```
into the terminal, or double clicking on the icon.

# Step 2: Open the terminal in VS Code

Open it by hitting ctrl + ` or Terminal -> New Terminal from the menu.

Make a new folder for your api project, and a new file in that folder called `apis.py`

```shell
$ cd
$ mkdir apis
$ cd apis
$ touch apis.py
```

# Step 3: Make a Virtual Environment

Virtual Environments in Python allow you to create isolated environments which you can then populate with just the packages that you need to work on your project. This of it as a container of all your dependencies for a specific Python project.

```shell
$ python3 -m venv env
$ source env/bin/activate
```

By activating the environment by running `source` in the shell script, you're using the sandboxed version of Python from that virtual environment, not your system python.

Once you activate your virtual environment, your prompt should look like this:

```shell
(env)$
```

You can confirm that by running:

```shell
(env)$ which python
```

For the most part, you'll want to use virtual environments for all of your Python projects to prevent conflicts with package versions and help keep your system Python clean.

Remember that if you close your terminal, or open a new window, your virtual environment won't be activated any more. Any time you want to work on this project, you'll need to type `source env/bin/activate` into the terminal. I recommend you leave a text note in your project, so you remember that step.

**Note:** If you'd like to _deactivate_ your virtual environment in the current terminal you can just type `deactivate`, but **don't** do this now, as we'll be using the virtual environment in the next steps.

### Important: Select the Virtual Environment Python in VS Code.

You'll see a python version on the left hand side of the blue bar on the bottom of the screen. Click on that and select `./env/bin/python` as the interpreter. Remember, that's the version of Python in the virtual environment directory.

# 3-Minute Python Overview

If you haven't worked with Python before, or don't know much about it you'll be pleasantly surprised. Most people think that Python is just for scripting, but it's not. It's a very powerful language used for data science, and it's responsible for some of the most popular sites on the internet like reddit.

In other languages like java or c++, you define scope with curly braces. That's caused some interesting security bugs, like the [famous Apple bug](https://blog.codecentric.de/en/2014/02/curly-braces/) that broke some of the SSL verification.

In Python, you define scope with whitespace. That means that when writing Python programs, white space is very important. Pay attention to it. If you mess it up, your Python program won't run or it will run incorrectly.

For example, if you define a function and the code underneath the function definition is indented, that means that the code belongs to that function.

Example:

```python
def foo()
    x = 42
```

Python's package manager is called [`pip`](https://pip.pypa.io/en/stable/quickstart/) and the packages live in a repository called [`PyPi` - The Python Package Index](https://pypi.org/). I always recommend investigating the PyPi page of a Python package you'd like to add to your program. Make sure it's legit, because [nefarious folks can capitalize on typos](https://incolumitas.com/2016/06/08/typosquatting-package-managers/) in popular package names.

# A Few Things About APIs

[RESTful APIs](https://www.mulesoft.com/resources/api/what-is-rest-api-design) are the most common ones that you'll come across these days. They follow a well defined formula that maps common HTTP operations like GET, PUT, and POST to operations on a data-set.

There are a lot of APIs out there. Some of them are free to use, some are locked behind a paywall. Some are open to everyone, while other's require some form of authentication. Most APIs are rate-limited to prevent someone from sending too many requests at once, or within a certain time frame.

You make a request of an API at a particular URL that points to the data you want to work with.

You can also send along headers with more details about what you're looking for, or data that you want to submit to the server. You can pass in things like authorization tokens, a content type for the data of data you're sending, and more.

Most times, if you don't send along herders, the server will have some form of defaults.

After you send a request to the API, you'll get back a response with a HTTP Status Code.

A [HTTP Status Code](https://httpstatuses.com/) in the:
* 200 range means everything went great
    * A common one is `200 OK`
* 300 range is a warning, like a resource has moved
* 400 range means a client error.
    * `404 NOT FOUND` - you requested a resource that doesn't exist
* 500 range means a server error.

These are guidelines, but there are also some silly ones. Like [`HTTP 418 I'M A TEAPOT` aka the Hyper Text Coffee Pot Control Protocol](https://en.wikipedia.org/wiki/Hyper_Text_Coffee_Pot_Control_Protocol).

Sometimes there's data associated with the response, and that data will tend to have a response type. The response can come in a binary format, text, xml, or most commonly, JSON. JSON is just a format for representing data, with a bunch of extra curly braces that I don't care for.

Know that Python has an incredible standard library, but the `requests` framework is much easier and more intuitive to use than the library code that comes with Python. It makes interacting with APIs much easier, so that's what we're going to use.

# Step 4 - Install [`requests`](http://docs.python-requests.org/en/master/)

We need to make sure that pip, the tool we use to install Python packages, is pointing to the right Python version. The one in the `env` folder of where your project is.

```shell
(env)$ pip --version
```

Next, install requests.

```shell
(env)$ pip install requests
```

Make a new python file named `apis.py` and open it in VS Code.

**Tip:** In VS Code, you can run Python code by highlighting it and pressing Shift+Enter. Make sure that you run the steps in order, or you'll get unexpected results.

# Step 5 - Start Calling APIs

The API that we're going to work with is the [GitHub API Version 3](https://developer.github.com/v3/). They offer a few endpoints we can use to grab interesting data without authenticating. But, there's a catch. The GitHub API only allows 60 unauthenticated requests per hour per IP. That's more than enough to complete the remaining exercises, but it's something to keep in mind when you're trying this at home.

## Part 1: Basics of calling an API with the requests library

In your `apis.py` file:

```python
# First thing we'll do is import the requests library
import requests

# Define a variable with the URL of the GitHub API
api_url = "https://api.github.com"

# Call the root of the api with GET, store the answer in a response variable
# This call will return all the other API endpoints that we can explore
response = requests.get(api_url)

# Get the status code for the response. Should be 200 OK
# Which means everything worked as expected
print("Response status code is: ", response.status_code)

# Keep in mind that as we’re working with the response
# we’re working with the stored object in Python.
# We’re not making any more requests at this time.
# Get the result as JSON
response_json = response.json()

# Print it. Should see a lot of information
print(response_json)
```

That was all you had to do to call an API in Python! Easy.

## Part 2: Accessing specific resources by URL

When we want to work with a particular object, we usually pass in information about it as part of the URL.

Let's call the API to find out how many stars this repo has: https://github.com/nnja/new-computer - We can do that by calling the `repos` endpoint and appending the owner and the name of the target repo we're interested in.

```python
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
```

## Passing in bad data returns a 404

```python
# Passing in bad info will result in a 404 (not found)
bad_response = requests.get("https://api.github.com/repositories/doesnt/exist")
print("Bad Response Status Code is:", bad_response.status_code)  # Status code is 404, meaning that resource doesn’t exist.
```

## Part 3: Passing in Parameters

We want to search for the top 3 Python repositories in GitHub, based on the number of stars for all time.

We can use the [GitHub API Search Endpoint](https://developer.github.com/v3/search/) to accomplish this task.

In order to do that, we'll need to pass in 2 parameters:
* `q` - the search query
* `sort` - what to sort by. In this case, we care about stars.


```python
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
```



## Next Steps

Now you know the basics, just enough to get started with working with APIs in Python with the requests library. You know just enough to see how powerful Python can be. You can chain all of these requests together into a fully functioning program that does so much more.

The next topics to study are:
* [How to authenticate to APIs](http://docs.python-requests.org/en/master/user/authentication/)
* How to use the other HTTP methods, just as POST to create resources, or PUT to update them
* Read the [requests Quick Start Guide](http://docs.python-requests.org/en/master/user/quickstart/)

## Additional Resources

* [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) - For learning the A-Z of Python web apps
* [Hitchhickers Guide to Python](https://docs.python-guide.org/) - free Book
* [Intro to Python](https://frontendmasters.com/workshops/intro-to-python/) & [Intermediate Python](https://frontendmasters.com/workshops/intermediate-python/) - 2 day course I'm teaching. Will be free to watch as a live stream in March, and available via subscription afterwards.
