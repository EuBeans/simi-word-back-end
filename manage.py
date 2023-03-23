import sys
import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask import current_app
from app import blueprint
from app.main import create_app, db
from app.main.model import user, blacklist
from app.main.MachineLearning.model import load_model

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pyunpack import Archive



#check if already authenticated
if os.path.exists("mycreds.txt"):
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")
gauth.LocalWebserverAuth() # client_secrets.json need to be in the same directory as the script
#store credentials
gauth.SaveCredentialsFile("mycreds.txt")
drive = GoogleDrive(gauth)

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
    file_list = drive.ListFile({'q': "'1RxUNxOG2amm36p4IiuHQEXfDSMbhfk6i' in parents and trashed=false"}).GetList()
    for file in file_list:
        file_id = file['id']
        file_name = file['title']
        print( file['title'], file['id'])
        print('title: %s, mimeType: %s' % (file['title'], file['mimeType']))

        # Download file from Google Drive if it is not already in the data folder
        if not os.path.isfile('app/main/data/' + file_name):
            print('Downloading file from Google Drive')
            downloaded = drive.CreateFile({'id': file_id})
            #show loading bar
            print('Downloading content "{}"'.format(downloaded))
            downloaded.GetContentFile('app/main/data/' + file_name)    
        #unzip file
        if file_name.endswith('.7z'):
            print('Unzipping file...')
            Archive('app/main/data/' + file_name).extractall('app/main/data/')
            #the code above is returning NotImplementedError: That compression method is not supported
            #so I am using the following code instead          
    
    with app.app_context():
        current_app.model = load_model('app/main/data/_glove.840B.300d.word2vec.txt')
    manager.run()
