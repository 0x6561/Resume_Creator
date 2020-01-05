import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Uno4Dos3Tres2Cuatro1'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SUBJECT_PREFIX = os.environ.get('MAIL_SUBJECT_PREFIX') or 'resume.0x6561.net Resume Creator '
    MAIL_SENDER = os.environ.get('MAIL_SENDER') or 'resume.0x6561.net'
    MAIL_DEBUG=True 
    DEBUG=True 
    MAIL_SUPPRESS_SEND=False
    TESTING = False
    MAIL_SERVER = 'smtp.googlemail.com'
    #MAIL_SERVER = 'resume.0x6561.net'
    MAIL_PORT = 587 
    #MAIL_PORT=465 
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    APP_ADMIN = os.environ.get('APP_ADMIN')
    MAIL_SUBJECT_PREFIX = 'prefix'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig 
}
