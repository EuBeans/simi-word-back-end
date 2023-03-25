import logging
import os
import threading
from time import sleep
from pyunpack import Archive
import psutil
from app.main import  current_app
from app.main.MachineLearning.model import load_model
from app.main.service.google_drive_service import GoogleDriveService
from googleapiclient.http import MediaIoBaseDownload
from apscheduler.schedulers.blocking import BlockingScheduler

drive = GoogleDriveService().build()



    
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

    
    

    logging.info('Downloading file from Google Drive')
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
            logging.info("Download %d%%.", int(status.progress() * 100))

        file.close()

    return download_stream()




class modelDownloaderWorker():


    def __init__(self, app):
        self.app = app
        #self.cache = cache
        #threads 
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()
  

    def run(self):
        logging.info('Starting model downloader worker')
        #file id to retrieve : 1E_9NU0zKw5sJp5aYIbw55lFToamU8LYB
        file = drive.files().get(fileId='1E_9NU0zKw5sJp5aYIbw55lFToamU8LYB', fields='name').execute()
        file_name = file.get('name')
        file_id = '1E_9NU0zKw5sJp5aYIbw55lFToamU8LYB'
        logging.info('File name: %s', file_name)


        # Download file from Google Drive if it is not already in the data folder
        if not os.path.isfile(file_name):
            #thread the download
            download_file(file_id, file_name)
           
            # Unzip file if it is not already in the data folder 

        if not os.path.isfile('_glove.840B.300d.word2vec.txt'):  
            if file_name.endswith('.7z'):
                # stop gunicorn worker from unzipping the file if  _glove.840B.300d.word2vec.7z is opened by another process
                # tell gunicon to wait for the file to be unzipped
                while True:
                    try:
                        os.rename(file_name, file_name)
                        break
                    except:
                        logging.info('file is being used by another process')
                        sleep(1)

                logging.info('Unzipping file...')
                Archive(file_name).extractall('.')
                logging.info('File unzipped')

        new_file_name = '_glove.840B.300d.word2vec.txt'
        while True:
            try:
                os.rename(new_file_name, new_file_name)
                break
            except:
                logging.info('file is being used by another process')
                sleep(1)
        with self.app.app_context():
                model_ml = load_model(new_file_name)
                current_app.config["MODEL"] = model_ml
                print('Model loaded')
                logging.info('Model loaded')

        """
        # Load model in cache
        if not self.cache.get('model_ml'):
            model_ml = load_model(new_file_name)
            self.cache.set('model_ml', model_ml)
            with self.app.app_context():
                current_app.config["MODEL"] = model_ml
                print('Model loaded')
                logging.info('Model loaded')
        else:
            model_ml = self.cache.get('model_ml')
            with self.app.app_context():
                current_app.config["MODEL"] = model_ml
                print('Model loaded from cache')
                logging.info('Model loaded from cache')
        """

