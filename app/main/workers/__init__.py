from ctypes import sizeof
import logging
import os
import threading
from time import sleep
from pyunpack import Archive
from tqdm import tqdm
from app.main import  current_app
from app.main.MachineLearning.model import load_model
from app.main.service.google_drive_service import GoogleDriveService
from googleapiclient.http import MediaIoBaseDownload
from alive_progress import alive_bar

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
    print('Downloading file from Google Drive')
    logging.info('Downloading file from Google Drive')
    request = drive.files().get_media(fileId=file_id)
    def download_stream():
        done = False
        file = open(destination,"wb")
        fh = ChunkHolder(file)
        downloader = MediaIoBaseDownload(fh, request, chunksize=8000 * 8000)


        # get expected file size
        file_size = drive.files().get(fileId=file_id, fields='size').execute().get('size')
        print('File size: %s', file_size)


        #get number of iterations
        iterations = int(int(file_size)/8000/8000)
        print('Iterations: %s', iterations)
        
        with alive_bar(iterations, force_tty=True,title='Downloading File',spinner='wait') as bar:
            while done is False:
                status, done = downloader.next_chunk()
                bar()
        # Download the file in chunks and store it at the given path
        # use alive-progress to show progress in percentage
        
        file.close()

    return download_stream()




class modelDownloaderWorker():


    def __init__(self, app):
        self.app = app
        #self.cache = cache
        #threads 
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()
  

    def run(self):
        print('Starting model downloader worker')
        logging.info('Starting model downloader worker')
        #file id to retrieve : 1E_9NU0zKw5sJp5aYIbw55lFToamU8LYB
        file = drive.files().get(fileId='1E_9NU0zKw5sJp5aYIbw55lFToamU8LYB', fields='name').execute()
        file_name = file.get('name')
        file_id = '1E_9NU0zKw5sJp5aYIbw55lFToamU8LYB'
        logging.info('File name: %s', file_name)

        new_file_name = '_glove.840B.300d.word2vec.txt'
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
                       
                        sleep(1)

                #unzip file
                """
                import py7zr
                with py7zr.SevenZipFile(file_name, mode='r') as z:
                        z.extractall()
                
                print('Unzipping file...')
                logging.info('Unzipping file...')
                """
                
                # Open the .7z file using py7zr
                import py7zr
                with py7zr.SevenZipFile(file_name, mode='r') as z:
                        print('unzipping file...')
                        z.extractall()
                        # indefinite alive bar
     
        with alive_bar() as bar:
            
            while True:
                try:
                    os.rename(new_file_name, new_file_name)
                    break
                except:
                    bar()
                    sleep(1)
        
        with self.app.app_context():
                model_ml = load_model(new_file_name)
                current_app.config["MODEL"] = model_ml
                print('Model loaded')
                logging.info('Model loaded')
        #return current thread 
    

    def join(self):
        self.thread.join()