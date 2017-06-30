#!/usr/bin python
# -*- coding: utf-8 -*-
'''
define general functions to be used in all the single module-files

everything that requires the db-sesssion is made in this function, so we only
have one file where we have to connect to the database and we never need to
import the session anywhere else
'''

from flask import session as login_session
from db_setup import Base, Categorie, Item, User
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.util import has_identity

'''
we want to be able to cast /catalog/Snowboard/My-fancy-Snowboard without any
troubles, so we have to also store a slugified version of the name into the
database. We use https://github.com/un33k/python-slugify
Usage:
slug=slugify("this string shall be slugified", max_length=17,
             stopwords=['the', 'in', 'a'], word_boundary=True)
'''
from slugify import slugify


#Connect to Database and create database session
engine = create_engine('sqlite:///productcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Catalog helper functions
def make_slug(string):
    return slugify(string, max_length=17, stopwords=['the', 'in', 'a'],
                   word_boundary=True)


def not_logged_in():
    if not login_session.get('access_token', None):
        return True


def not_owner(categorie_name, item_slug):
    owner = getItem(categorie_name, item_slug).user_id
    if not login_session.get('username') == owner:
        return True


def getCategorieIdFromName(categorie_name):
    try:
        cat = session.query(Categorie).filter_by(name=categorie_name).one()
        return cat.id
    except:
        return None


def getAllCategories():
    return session.query(Categorie).order_by(asc(Categorie.name))


def getAllItems():
    return session.query(Item).order_by(asc(Item.name))


def getRecentItems():
    return session.query(Item).order_by(desc(Item.id)).limit(10)


def getItemsFromCategorie(categorie_name):
    categorie_id = getCategorieIdFromName(categorie_name)
    return session.query(Item).filter_by(categorie_id=categorie_id).all()


def getItem(categorie_name, item_slug):
    categorie_id = getCategorieIdFromName(categorie_name)
    item = session.query(Item).filter_by(categorie_id=categorie_id) \
                              .filter_by(slug=item_slug) \
                              .one()
    return item


def saveItem(form, categorie_name):
    slug = make_slug(form['name'])
    count = 0
    while session.query(Item).filter_by(slug=slug).count() > 0:
        print("\n=====\n" + slug + " does exist, make it ")
        slug += "-" + str(count)
        count += 1
        print(slug + " and check again \n=====\n")
    newItem = Item(name=form['name'],
                   slug=slug,
                   description=form['description'],
                   categorie_id=getCategorieIdFromName(categorie_name),
                   user_id=getUserIdByName(login_session.get('username')))
    session.add(newItem)
    session.commit()


def addAndCommit(dbentry):
    session.add(dbentry)
    session.commit()


def deleteItemFromDb(item):
    session.delete(item)
    session.commit()


# User helper functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
        'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserIdByMail(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def getUserIdByName(username):
    try:
        user = session.query(User).filter_by(name=username).one()
        return user.name
    except:
        return None
