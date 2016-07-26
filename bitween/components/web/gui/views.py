__author__ = 'meatpuppet'
# -*- coding: utf-8 -*-

from . import gui
from flask import render_template, redirect, abort, url_for, request, flash, make_response, Markup, current_app, flash

from components import handles

from components import contact_shares

@gui.route('/', methods=['GET', 'POST'])
def index():
    """

    :return:
    """

    torrents = []

    for t in handles.get_shares():
        torrents.append(t)

    return render_template('gui_index.html', torrents=torrents)

@gui.route('/search', methods=['GET', 'POST'])
def search():
    """

    :return:
    """
    hashes = {}
    contacts = contact_shares.dict

    for contact in contacts:
        for resource in contacts[contact]:
            for hash, val_dict in contacts[contact][resource]['shares'].iteritems():
                c = hashes.get(hash, {'contacts': []}).get('contacts')
                c.append('%s/%s' % (contact, resource))
                hashes[hash] = {'name': val_dict['name'],
                                'size': val_dict['size'],
                                'contacts': c}


    return render_template('gui_search.html', hashes=hashes)



@gui.route('/favicon.ico')
def favicon():
    return url_for('static', filename='favicon.ico')


@gui.route('/static/about')
def about():
    """
    path to the static about page

    :return:
    """

    return render_template('gui_about.html')

