import logging
import os
from time import sleep
import unittest
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app.main import create_app, db
from app import blueprint
from app.main.socketio import socketio

# Register SocketIO event handlers

app = create_app(os.getenv('SEMIWORD_ENV') or 'dev')
app.register_blueprint(blueprint)
app.app_context().push() 

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

# associate socketio event handlers with socketio instance, 
socketio.init_app(app, async_mode="eventlet", engineio_logger=True,log_level=logging.DEBUG)

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,PATCH,DELETE,OPTIONS')
  return response


@manager.command
def run():
    socketio.run(app)

@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()      
        
