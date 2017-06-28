#!/usr/bin python
# -*- coding: utf-8 -*-
'''
json.py generates all the JSON endpoints
'''

from flask import jsonify
from functions import getItemsFromCategorie, getAllItems, getItem

routes = []


def catalogJSON():
    #catalog = session.query(Categorie).all()
    #items = session.query(Item).all()
    ## how do I create JSON output from two databases?
    #return jsonify(catalog=[r.serialize for r in catalog])
    items = getAllItems()
    return jsonify(All_Items=[i.serialize for i in items])
routes.append(dict(
    rule='catalog/JSON',
    view_func=catalogJSON))


def categorieJSON(categorie_name):
    items = getItemsFromCategorie(categorie_name)
    return jsonify(Items=[i.serialize for i in items])
routes.append(dict(
    rule='catalog/<string:categorie_name>/items/JSON',
    view_func=categorieJSON))


def itemJSON(categorie_name, item_slug):
    item = getItem(categorie_name, item_slug)
    return jsonify(Item=item.serialize)
routes.append(dict(
    rule='catalog/<string:categorie_name>/items/<string:item_slug>/JSON',
    view_func=itemJSON))
