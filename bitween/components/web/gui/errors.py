'''
Created on 25.06.2014

@author: Toni
'''

from flask import render_template, request
from . import gui
from flask import jsonify


@gui.app_errorhandler(403)
def page_not_found(e):
    """Errorhandle for 403 Page not Found

    :param e: errormsg
    :return: html
    """
    return render_template('403.html'), 403


@gui.app_errorhandler(404)
def page_not_found(e):
    """
    This ist called type negotiation!!!
    *check wether it is an httprequest or an api request
    The other errorshandlers used by the api are implemented in it's own package.

    :param e: errormsg
    :return: 404.html or an jsonobject {'error': 'not fount'}
    """
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template('404.html'), 404


@gui.app_errorhandler(500)
def internal_server_error(e):
    """Errorhandle for 500 Internal Server ERROR

    :param e: errormsg
    :return: html
    """
    return render_template('500.html'), 500
