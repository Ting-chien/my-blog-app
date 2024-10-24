import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
        os.environ.get("DEV_DB_USERNAME"), 
        os.environ.get("DEV_DB_PASSWORD"), 
        os.environ.get("DEV_DB_HOST"),
        os.environ.get("DEV_DB_PORT"), 
        os.environ.get("DEV_DB_NAME")
    )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
        os.environ.get("TESTING_DB_USERNAME"), 
        os.environ.get("TESTING_DB_PASSWORD"), 
        os.environ.get("TESTING_DB_HOST"),
        os.environ.get("TESTING_DB_PORT"), 
        os.environ.get("TESTING_DB_NAME")
    )


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}