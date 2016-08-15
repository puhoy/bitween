
from flask import Blueprint

gui = Blueprint('gui', __name__, template_folder='templates', static_folder='static')  # Blueprint(moduleName, moduleOrPackage)

from . import views, errors
