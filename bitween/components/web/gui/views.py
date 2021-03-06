from . import gui
from flask import render_template

from bitween.components import handles

from bitween.components import contact_shares

@gui.route('/', methods=['GET'])
def index():
    """
    return rendered template containing the own shares

    :return:
    """
    return render_template('gui_index.html', torrents=handles.get_shares())

@gui.route('/search', methods=['GET'])
def search():
    """
    return a rendered template containing all found shares

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

