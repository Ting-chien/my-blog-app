import os
from app import create_app, db
from app.auth.models import User, Role
from config import config

ENV = os.getenv('FLASK_ENV')


try:
    app_config = config[ENV]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, ...]')

app = create_app(app_config)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)