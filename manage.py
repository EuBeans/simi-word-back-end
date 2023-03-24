import io
import sys
import os
from time import sleep
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask import current_app
from app import blueprint
from app.main import create_app, db
from app.main.model import user, blacklist
from app.main.MachineLearning.model import load_model

from pyunpack import Archive

from app.main.service.google_drive_service import GoogleDriveService
from googleapiclient.http import MediaIoBaseDownload

drive = GoogleDriveService().build()


app = create_app(os.getenv('SEMIWORD_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push() 
model_ml = None

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run(host='localhost', port=8080)


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
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
    manager.run()
