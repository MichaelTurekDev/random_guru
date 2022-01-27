class Config(object):
    DEBUG = False
    TESTING = False
    DB_NAME = 'production-db'


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    DB_NAME = 'development-db'
