from flask import render_template

from app import db
from app.base import blueprint


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    return "Login page"


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404