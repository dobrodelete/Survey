from app import create_app, db
from app.database import import_survey_data
from app.models import create_admin_user

app = create_app()


@app.before_first_request
def initialize():
    db.create_all()
    create_admin_user()


if __name__ == '__main__':
    app.run(debug=True)
