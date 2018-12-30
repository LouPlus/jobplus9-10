class BaseConfig(object):
    ''' os.urandom(24)'''
    SECRET_KEY = "\xcaW\x9d\xba\xe5\xfb+'\x88aRP\xfd\xc9fHE;\xec\xc9\xdf,\n\x82"

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@localhost:3306/jobplus?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    COUNTS_PER_PAGE = 9
    ADMIN_PER_PAGE = 10

class ProductionConfig(BaseConfig):
    pass

class TestingConfig(BaseConfig):
    pass


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
    }
