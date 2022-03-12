import os


# default config
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = '\x8d1K\x1f\x17\xd5\xbbU\xbc\xd3\xc3n\xfd,umH\x1b\xe94Wc\x90'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# dev config
class DevelopmentConfig(BaseConfig):
    DEBUG = True


# production config
class ProductionConfig(BaseConfig):
    DEBUG = False

