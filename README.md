# Linux Server
## Progress
- generate new SSh key pair "grader.pem", permissions: 400
- change SSH port to: 2200 (/etc/ssh/sshd_config: PORT 2200)
    => ssh ubuntu@35.158.70.106 -p 2200
- disable root login (/etc/ssh/sshd_config: PermitRootLogin no)
- new user "grader": https://unix.stackexchange.com/questions/210228/add-a-user-wthout-password-but-with-ssh-and-public-key
our identification has been saved in grader.
Your public key has been saved in grader.pub.
The key fingerprint is:
SHA256:6Y8OM+aCgexbF+khyHx1bJPDpR9ZI2HykUSEXsqO/9U lud@Ludwigs-MacBook-Pro.local
The key's randomart image is:
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
-
- give new user root rights: $ sudo usermod -aG sudo grader
- verify, if successful: $ grep -Po '^sudo.+:\K.* $' /etc/group   (before copy-paste: remove space between * and S)
    => ubuntu, grader
- ubuntu@ip-172-26-7-109:/$ sudo ufw status
Status: active

To                         Action      From
--                         ------      ----
2200/tcp                   ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
123/udp                    ALLOW       Anywhere
2200/tcp (v6)              ALLOW       Anywhere (v6)
80/tcp (v6)                ALLOW       Anywhere (v6)
123/udp (v6)               ALLOW       Anywhere (v6)
- sudo apt-get install apache2
- sudo apt-get install libapache2-mod-wsgi
    => WSGIScriptAlias /catalog var/www/html/catalog.wsgi
- sudo apt-get install postgresql
- installed pip, slugify
- Git: sudo apt-get install build-essential libssl-dev libcurl4-gnutls-dev libexpat1-dev gettext unzip
  => sudo git clone https://github.com/swiknaba/LinuxServer.git
- SQLAlchemy: https://stackoverflow.com/questions/22353512/how-to-install-sqlalchemy-on-ubuntu
- no module oauth2client.client => sudo pip install --upgrade google-api-python-client
- no module requests => sudo pip install requests
- https://devops.profitbricks.com/tutorials/install-and-configure-mod_wsgi-on-ubuntu-1604-1/
- sudo service apache2 restart  // sudo service apache2 reload
- sudo a2enconf wsgi
- updated google oauth credentials. Problem: can't add IP address as authorized uri
    => solution: https://stackoverflow.com/questions/14238665/can-a-public-ip-address-be-used-as-google-oauth-redirect-uri
    => use 35.157.147.219.xip.io/login

Apache2 is failing and I don't get it to run, trying Nginx:
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-16-04
- uwsgi --socket 0.0.0.0:80 --protocol=http -w wsgi
- sudo source catalogappenv/bin/activte
- sudo uwsgi --socket 0.0.0.0:80 --protocol=http -w wsgi:app --master
- if socket.error: address already in use:
    -> sudo lsof -i:80
    -> sudo kill PID
- secret_key: TVLb2,zX,V#geo6j^dD%uzEgtsjaBoG8*AEKvMeeWR2{3;YNQ2{>3CgLrE4k2Lb3
        => has to be defined in the wsgi.py file!
- sudo systemctl restart nginx

Changing the owner of /var/www/django/ to www-data made it work.
Specifically the problem was with ownership of the file /etc/nginx/uwsgi_params

AFTER:
sudo rm -rf /usr/share/nginx/html/index.html .
rm: refusing to remove '.' or '..' directory: skipping '.'
grader@ip-172-26-7-109:~$ sudo rm -rf /usr/share/nginx/html/index.html
grader@ip-172-26-7-109:~$ sudo ln -s /usr/share/nginx/html/ /var/www/html/catalogapp/
grader@ip-172-26-7-109:~$ sudo systemctl restart nginx
grader@ip-172-26-7-109:~$ sudo nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is su ccessful
THE IP SAYS: FORBIDDEN

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
