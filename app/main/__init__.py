import io
import sys
import os

from flask import Flask, current_app
from flask_caching import Cache

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from .config import config_by_name
from flask.app import Flask
from app.main.MachineLearning.model import load_model

from pyunpack import Archive

from app.main.service.google_drive_service import GoogleDriveService
from googleapiclient.http import MediaIoBaseDownload



drive = GoogleDriveService().build()
cache = Cache(config={'CACHE_TYPE': 'filesystem','CACHE_DIR': os.getcwd()})

db = SQLAlchemy()
flask_bcrypt = Bcrypt()

def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    cache.init_app(app)



    #file id to retrieve : 1E_9NU0zKw5sJp5aYIbw55lFToamU8LYB
    file = drive.files().get(fileId='1E_9NU0zKw5sJp5aYIbw55lFToamU8LYB', fields='name').execute()
    file_name = file.get('name')
    file_id = '1E_9NU0zKw5sJp5aYIbw55lFToamU8LYB'

    # Download file from Google Drive if it is not already in the data folder
    if not os.path.isfile('app/main/data/' + file_name):
        print('Downloading file from Google Drive')
        drive.files().get_media(fileId=file_id).execute()
        #show loading bar
        print('Downloading content "{}"'.format(file_name))
        #download file
        request = drive.files().get_media(fileId=file_id)
        fh = io.FileIO('app/main/data/' + file_name, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        print('Download complete')
        #let go of the file handle
        fh.close()
    # Unzip file if it is not already in the data folder
    if not os.path.isfile('app/main/data/_glove.840B.300d.word2vec.txt'):  
        if file_name.endswith('.7z'):
            print('Unzipping file...')
            Archive('app/main/data/' + file_name).extractall('app/main/data/')
            print('Unzipping complete')
    # Load model in cache
    if not cache.get('model_ml'):
        model_ml = load_model('app/main/data/_glove.840B.300d.word2vec.txt')
        cache.set('model_ml', model_ml)
        #insert model into current_app so that it can be accessed by the flask app
        with app.app_context():
            current_app.config["MODEL"] = model_ml
            print('Model loaded')
    else:
        #model is in cache
        #get model from cache
        
        model_ml = cache.get('model_ml')
        #insert model into current_app so that it can be accessed by the flask app
        with app.app_context():
            current_app.config["MODEL"] = model_ml
            print('Model loaded from cache')

    return app
