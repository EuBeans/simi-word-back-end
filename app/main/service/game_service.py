import random
import string
import uuid
import datetime

from app.main import db
from app.main.model.game import Game
from typing import Dict, Tuple
from ..model.game import Theme, GameMode, GameLevel, GameStatus


def save_new_game(user_id:str, data: Dict[str, str], session_id:str = None) -> Tuple[Dict[str, str], int]:

    try:

        
        theme = Theme(data['theme'])
        game_mode = GameMode(data['game_mode'])
        game_level = GameLevel(data['game_level'])
        game_status = GameStatus.in_progress
        max_round_number = data['max_round_number']
        multiplayer_code = None
        gameSessionId = None
        #if game_mode is multiplayer, multiplayer_code must be set
        if game_mode == GameMode.multiplayer:
            #generate a random code with letters and numbers and 6 characters
            multiplayer_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if session_id:
                gameSessionId = session_id
        #check if there was a previous game in progress and set it to completed
        previous_game = Game.query.filter_by(user_id=user_id, game_status=GameStatus.in_progress).first()
        if previous_game:
            previous_game.game_status = GameStatus.completed
            previous_game.end_time = datetime.datetime.utcnow()
            db.session.commit()

        new_game = Game(
            game_id= str(uuid.uuid4()),
            user_id= user_id,
            game_mode= game_mode,
            game_level= game_level,
            theme = theme,
            score = 0,
            start_time=datetime.datetime.utcnow(),
            created_at=datetime.datetime.utcnow(),
            game_status = game_status,
            max_round_number = max_round_number,
            multiplayer_code = multiplayer_code,
            gameSessionId = gameSessionId
        )
        save_changes(new_game)
        

        return  {
            'status': 'success',
            'message': 'Game successfully created.',
            'game': new_game.to_json(),
        }, 201  
    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401
    

def get_all_games(user_id: str):
    #for each .to_json() in the list, it will call the to_json() method in the model
    return [game.to_json() for game in Game.query.filter_by(user_id=user_id).all()]


def get_a_game(game_id: str) -> Game:
    return Game.query.filter_by(game_id=game_id).first()

def get_a_game_by_multiplayer_code(multiplayer_code):
    # check if game is in progress
    game = Game.query.filter_by(multiplayer_code=multiplayer_code, game_status=GameStatus.in_progress).first()
    if not game:
        return None
    else:
        return game.to_json()
def get_a_game_by_session_id_and_user_id(session_id, user_id):
    return Game.query.filter_by(gameSessionId=session_id, user_id=user_id).first().to_json()

def end_game(game_id):
    game = Game.query.filter_by(game_id=game_id).first()
    if not game:
        response_object = {
            'status': 'fail',
            'message': 'Game does not exist.'
        }
        return response_object
    
    else:
        game.game_status = GameStatus.completed
        game.end_time = datetime.datetime.utcnow()
        db.session.commit()
        return game.to_json()

def update_score(game_id, score):
    game = Game.query.filter_by(game_id=game_id).first()
    if not game:
        response_object = {
            'status': 'fail',
            'message': 'Game does not exist.'
        }
        return response_object
    else:
        game.score = game.score + score
        db.session.commit()
        return game.to_json()

def save_changes(data: Game) -> None:
    db.session.add(data)
    db.session.commit()
