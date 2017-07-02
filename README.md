# Item Catalog
## A Udacity Project

***

### Stack/Dependencies
- python 2.7
- flask
- html/css (bootstrap)
- SQLAlchemy
- [python slugify module](https://github.com/un33k/python-slugify) => You have to install this!
- jQuery (for google sign in)


### Code-Organisation
    ├── client_secrets.json     # for Google OAuth 2
    ├── db_setup.py             # defines the SQLAlchemy database
    ├── populate_db.py          # run to start db with same sample entries
    ├── project.py              # run to start the server
    ├── README.md               # this very file
    ├── modules                 # contains all the python code
    │   ├── __init__.py         # manage blueprints, global routing
    │   ├── catalog.py          # handles catalog and item HTML endpoints
    │   ├── functions.py        # connects to DB, defines helper-functions
    │   ├── makejson.py         # generates JSON endpoints
    │   └── user.py             # handles user action (login, logout)
    ├── static                  # images and css files
    │   ├── style.css           # own styling on top of bootstrap
    │   └── ...                 # multiple imagefiles for background pattern
    └── templates               # all HTML files
        └── ...                 # multiple HTML files, using flask/jinja2 framework

### Run the Project
- make sure you have [Vagrant](https://www.vagrantup.com/intro/getting-started/index.html) intalled and running
- set up Vagrant to use port 5000
- put all files in the Vagrant directory, then turn it on: `>vagrant up` and log in `>vagrant ssh`
- navigate to the itemcatalog folder inside your vagrant directory
- install the database including some sample entries: `>python db_setup.py`
- start your server locally: `>python project.py`

### JSON endpoints
There are basically three types of JSON endpoints:

1. `/catalog/JSON` will show all items
2. `/catalog/Soccer/items/JSON` will show all items for the categorie `Soccer`
3. `/catalog/Baseball/items/baseball-bat/JSON` will show only one item `baseball-bat`

The urls for these endpoints are actually the same used when browsing the app, just append `JSON` to the url


### Login
One can login with a Google Account (OAuth2), only the bare minimum rights have to be granted. Once logged in a user can add/edit/delete items to every category which he/her himself did create originally
