# default config
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = '\x8d1K\x1f\x17\xd5\xbbU\xbc\xd3\xc3n\xfd,umH\x1b\xe94Wc\x90'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///agents.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
