import os

from app.main.MachineLearning.model import load_model

# uncomment the line below for postgres database url from environment variable

#
#password is SECRET_KEY
postgres_local_base  = 'postgresql://postgres:{}@simordia.cjnlwawh5131.us-east-2.rds.amazonaws.com:5432/simordia'.format(os.getenv('SECRET_KEY'))
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    CACHE_TYPE: "SimpleCache"  # Flask-Caching related configs

    DEBUG = False
    # Swagger
    RESTX_MASK_SWAGGER = False



class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_main.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True

    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    SQLALCHEMY_DATABASE_URI = postgres_local_base

class Celery:
    broker_url = 'amqp://guest:guest@localhost:5672//'
    result_backend = 'rpc://'
    task_serializer = 'json'
    result_serializer = 'json'
    accept_content = ['json']
    timezone = "North America/New York"
    enable_utc = True


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig,
    CELERY=Celery
)

key = Config.SECRET_KEY
