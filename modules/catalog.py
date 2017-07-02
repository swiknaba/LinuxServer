#!/usr/bin python
# -*- coding: utf-8 -*-
'''
catalog.py handles everything related to categories and items
'''

from flask import render_template, redirect, request
from functions import not_logged_in
from functions import getItemsFromCategorie, getAllCategories, getItem
from functions import saveItem, addAndCommit, getCategorieIdFromName, make_slug
from functions import deleteItemFromDb, getRecentItems, not_owner

routes = []


def showCategories():
    categories = getAllCategories()
    items = getRecentItems()
    if not_logged_in():
        return render_template('showCategories_public.html',
                               categories=categories, items=items)
    else:
        return render_template('showCategories.html', categories=categories,
                               items=items)
routes.append(dict(
    rule='catalog/',
    view_func=showCategories))


def showAllItems(categorie_name):
    categories = getAllCategories()
    items = getItemsFromCategorie(categorie_name)
    if not_logged_in():
        return render_template('showAllItems_public.html',
                               categories=categories, items=items)
    else:
        return render_template('showAllItems.html', categories=categories,
                               items=items)
routes.append(dict(
    rule='catalog/<string:categorie_name>/items/',
    view_func=showAllItems))


def showItem(categorie_name, item_slug):
    item = getItem(categorie_name, item_slug)
    if not_logged_in():
        return render_template('showItem_public.html', item=item)
    else:
        if not_owner(categorie_name, item_slug):
            return render_template('showItem.html', item=item)
        else:
            return render_template('showItem.html', item=item, owner=True)
routes.append(dict(
    rule='catalog/<string:categorie_name>/items/<string:item_slug>/',
    view_func=showItem))


def createItem(categorie_name):
    if not_logged_in():
        return redirect('login')
    if request.method == 'POST':
        saveItem(request.form, categorie_name)
        return redirect('catalog/' + categorie_name + '/items/')
    else:
        return render_template('createItem.html',
                               categorie_name=categorie_name)
routes.append(dict(
    rule='catalog/<string:categorie_name>/items/new',
    view_func=createItem,
    options=dict(methods=['GET', 'POST'])))


def updateItem(categorie_name, item_slug):
    if not_logged_in():
        return redirect('login')
    item = getItem(categorie_name, item_slug)
    if not_owner(categorie_name, item_slug):
        return redirect('catalog/' + categorie_name + '/items/' + item.slug)
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
            item.slug = make_slug(request.form['name'])
        if request.form['categorie']:
            cat_name = request.form['categorie']
            item.categorie_id = getCategorieIdFromName(cat_name)
        if request.form['description']:
            item.description = request.form['description']
        addAndCommit(item)
        return redirect('catalog/' + cat_name + '/items/' + item.slug)
    else:
        return render_template('editItem.html', item=item)
routes.append(dict(
    rule='catalog/<string:categorie_name>/items/<string:item_slug>/edit',
    view_func=updateItem,
    options=dict(methods=['GET', 'POST'])))


def deleteItem(categorie_name, item_slug):
    if not_logged_in():
        return redirect('login')
    item = getItem(categorie_name, item_slug)
    if not_owner(categorie_name, item_slug):
        return redirect('catalog/' + categorie_name + '/items/' + item.slug)
    if request.method == 'POST':
        item = getItem(categorie_name, item_slug)
        deleteItemFromDb(item)
        return redirect('catalog/' + categorie_name + '/items/')
    else:
        return render_template('deleteItem.html', item=item)
routes.append(dict(
    rule='catalog/<string:categorie_name>/items/<string:item_slug>/delete',
    view_func=deleteItem,
    options=dict(methods=['GET', 'POST'])))
