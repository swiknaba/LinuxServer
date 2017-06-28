#!/usr/bin python
# -*- coding: utf-8 -*-
'''
bundle all modules and define the global routing
'''

from flask import Blueprint, redirect
mod = Blueprint('modules', __name__)


# re-route everything to /catalog/ this is apparently necessary if one uses
# blueprints
@mod.route('/')
def home():
    return redirect('catalog/')


# import all module's routes here
from .catalog import routes as catalog_routes
from .user import routes as user_routes
from .makejson import routes as json_routes

# put together the routes
routes = (
    catalog_routes +
    user_routes +
    json_routes)

# generate global routing
for r in routes:
    mod.add_url_rule(
        r['rule'],
        endpoint=r.get('endpoint', None),
        view_func=r['view_func'],
        **r.get('options', {}))
