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
    print(file_name, file_id)


    # Download file from Google Drive if it is not already in the data folder
    if not os.path.isfile(file_name):
        download_file(file_id, file_name)



    # Unzip file if it is not already in the data folder
    if not os.path.isfile('_glove.840B.300d.word2vec.txt'):  
        if file_name.endswith('.7z'):
            print('Unzipping file...')
            Archive(file_name).extractall('')
            print('Unzipping complete')

    


    # Load model in cache
    if not cache.get('model_ml'):
        model_ml = load_model('_glove.840B.300d.word2vec.txt')
        cache.set('model_ml', model_ml)
        with app.app_context():
            current_app.config["MODEL"] = model_ml
            print('Model loaded')
    else:
        model_ml = cache.get('model_ml')
        with app.app_context():
            current_app.config["MODEL"] = model_ml
            print('Model loaded from cache')

    return app

class ChunkHolder(object):

    def __init__(self,file):
        self.chunk = None
        self.file = file

    def write(self, chunk):
        """Save current chunk"""
        self.chunk = chunk
        #write to file
        self.file.write(chunk)

def download_file(file_id, destination):
    print('Downloading file from Google Drive')
    request = drive.files().get_media(fileId=file_id)
    def download_stream():
        done = False
        file = open(destination,"wb")
        fh = ChunkHolder(file)
        downloader = MediaIoBaseDownload(fh, request, chunksize=8000 * 8000)

        # Download the file in chunks and store it at the given path
        while not done:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

        file.close()

    return download_stream()