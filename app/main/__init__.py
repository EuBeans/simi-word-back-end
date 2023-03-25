import io
import sys
import os
from time import sleep

from flask import Flask, current_app
from flask_caching import Cache

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from .config import config_by_name
from flask.app import Flask
from app.main.MachineLearning.model import load_model
from app.main.workers import modelDownloaderWorker
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler


db = SQLAlchemy()
flask_bcrypt = Bcrypt()
cache = Cache(config={'CACHE_TYPE': 'filesystem','CACHE_DIR': os.getcwd()})
scheduler = BackgroundScheduler()


def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    cache.init_app(app)
    # schedule model download run only once
    cur_app = current_app._get_current_object()
    modelDownloaderWorker(cur_app, cache)
   
    return app

