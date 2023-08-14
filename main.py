from blueprints.admin.admin import admin
from blueprints.survey.survey import survey
from blueprints.api.api import api
from blueprints.site.site import site

from flask import Flask

# from setup import setup_project
from config import FLASK_DEBUG, FLASK_SECRET_KEY
# setup_project()

app = Flask(__name__)

app.config["SECRET_KEY"] = FLASK_SECRET_KEY

app.register_blueprint(site, url_prefix="/")
app.register_blueprint(survey, url_prefix="/survey/")
app.register_blueprint(admin, url_prefix="/admin/")
app.register_blueprint(api, url_prefix="/api/v1/")


if __name__ == "__main__":
    app.run(debug=FLASK_DEBUG)
