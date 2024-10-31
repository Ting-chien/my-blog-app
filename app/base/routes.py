from flask import render_template
from . import blueprint


@blueprint.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
