from flask import Blueprint

survey_bp = Blueprint('survey', __name__, template_folder='templates/survey')

from . import routes
