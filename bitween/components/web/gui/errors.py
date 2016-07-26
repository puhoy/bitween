from flask import render_template, request
from . import gui
from flask import jsonify


@gui.app_errorhandler(403)
def page_not_found(e):
    """Handler for 403 Forbidden

    :param e: errormsg
    :return: rendered template or json
    """
    return render_template('403.html'), 403


@gui.app_errorhandler(404)
def page_not_found(e):
    """Handler for 404 Not found

    :param e: errormsg
    :return: rendered template or json
    """
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template('404.html'), 404


@gui.app_errorhandler(500)
def internal_server_error(e):
    """Handle for 500 Internal Server Error

    :param e: errormsg
    :return: rendered template or json
    """
    return render_template('500.html'), 500
