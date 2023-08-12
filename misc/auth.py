from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/panel/login')
def login():
    return 'Login'

@auth.route('/panel/logout')
def logout():
    return 'Logout'