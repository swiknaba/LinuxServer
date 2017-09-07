# Linux Server
## Progress of setting up
- generate new SSh key pair "grader.pem", permissions: 400
- change SSH port to: 2200 (/etc/ssh/sshd_config: PORT 2200)
    => ssh ubuntu@35.158.70.106 -p 2200
- disable root login (/etc/ssh/sshd_config: PermitRootLogin no)
- create a new user "grader" as explained at [Stack Exchange](https://unix.stackexchange.com/questions/210228/add-a-user-wthout-password-but-with-ssh-and-public-key)

- generate ssh keyfile: 
your identification has been saved in grader.
Your public key has been saved in grader.pub.
The key fingerprint is:
SHA256:6Y8OM+aCgexbF+khyHx1bJPDpR9ZI2HykUSEXsqO/9U lud@Ludwigs-MacBook-Pro.local
The key's randomart image is:

`
      +---[RSA 2048]----+
      |       .=Xoo     |
      |      o.Bo= .    |
      |     .oXo+       |
      |o . . +++..      |
      |.= o +o S.       |
      |..o o.oo    .    |
      |.  + o* .  . E   |
      | .o oo = o.      |
      | ..  ...+..      |
      +----[SHA256]-----+
`

- give new user root rights: $ sudo usermod -aG sudo grader
- verify, if successful: `grep -Po '^sudo.+:\K.*$' /etc/group`
    => ubuntu, grader

ubuntu@ip-18-194-4-174:/$ sudo ufw status
Status: active

    To                         Action      From
    --                         ------      ----
    2200/tcp                   ALLOW       Anywhere
    80/tcp                     ALLOW       Anywhere
    123/udp                    ALLOW       Anywhere
    2200/tcp (v6)              ALLOW       Anywhere (v6)
    80/tcp (v6)                ALLOW       Anywhere (v6)
    123/udp (v6)               ALLOW       Anywhere (v6)

Because I had troubles with apache, I gave up on it and used nginx.

Following the [digital ocean tutorial](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-16-04) for setting up ngix + flask to be served as uwsgi application. Be aware, that the tutorial for Ubuntu 14 and 16 do have important differences! I used Ubuntu 16 since that was offered by Amazon Lightsail.

This tutorial did work in the end, however I ran into several problems, documented in the [Udactiy forum](https://discussions.udacity.com/t/solved-uwsgi-proxy-not-working-connection-refused-manual-starting-works/353197).
1. sudo nano /etc/nginx/sites-available/catalogapp
  This line: `uwsgi_pass unix:///home/ubuntu/catalogapp/catalogapp.sock` note the `///` instead of `/` as shown in the tutorial
2. the app secret key needs to be also above (not only inside) the `if __name__ == '__main__':` loop of the wsgi.py file.
- secret_key: `TVLb2,zX,V#geo6j^dD%uzEgtsjaBoG8*AEKvMeeWR2{3;YNQ2{>3CgLrE4k2Lb3`
3. add the following to the `wsgi.ph` file: `sys.path.insert(0, '/home/ubuntu/catalogapp')`

- sudo systemctl restart nginx
- for the virtual environment install all necessary python packages, which are (additionally to the list below "Stack/Dependencies")
   - oauth2client
   - requests
   - MySql-Python
   - flask-sqlalchemy

# How to login via ssh

    ssh grader@18.194.4.174 -p 2200
    
Use the provided private ssh key `grader` for authentication (found in main folder of this project). Copy it to your machines /.ssh folder and chmod the permission to be 400 than add it to your keychain (e.g. for macOS: `ssh-add -K /.ssh/grader`)

=== Readme for the app itself:

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
