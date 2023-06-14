from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from importlib import import_module

db = SQLAlchemy()
migrate = Migrate()
socket_io = SocketIO()


def register_blueprints(app):
    for module_name in ["base", "blog"]:
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app(config):

    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db=db)
    socket_io.init_app(app)
    register_blueprints(app)
    configure_database(app)

    @app.route('/')
    def index():
        return "Hello Flask App!"
    
    return app