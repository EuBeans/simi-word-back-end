import uuid
import datetime
from app.main import db
from app.main.model.game import GameMode, GameStatus
from app.main.model.game_score import GameScore
from app.main.service.game_service import get_a_game, end_game, update_score
from typing import Dict, Tuple
from app.main.MachineLearning.model import get_word_from_theme, get_similar_word_list

def save_new_game_score(user_id:str, game_id:str) -> Tuple[Dict[str, str], int]:
    """Create a new Score """
    game = get_a_game(game_id)
    game_mode = GameMode(game['game_mode'])
    if not game:
        response_object = {
            'status': 'fail',
            'message': 'Game does not exist.',
        }
        return response_object, 409

    if(game['game_status'] != GameStatus.in_progress.value):
        response_object = {
            'status': 'fail',
            'message': 'Game is not in progress.',
        }
        return response_object, 409
    
    print(game_mode, GameMode.multiplayer, game_mode != GameMode.multiplayer)
    if(game_mode != GameMode.multiplayer):
        response_object = {
            'status': 'fail',
            'message': 'Game is not in multiplayer mode.',
        }
        return response_object, 409
    

    new_game_score = GameScore(
        score_id = str(uuid.uuid4()),
        user_id= user_id,
        game_id= game_id,
        score= 0,
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow(),
    )
    save_changes(new_game_score)

    return  {
        'status': 'success',
        'message': 'Game successfully created.',
        'game_score': new_game_score.to_json()
    }

#update score
def update_game_score(user_id:str, game_id:str, score:int) -> Tuple[Dict[str, str], int]:
    """Update a Score """
    game = get_a_game(game_id)
    game_mode = GameMode(game['game_mode'])
    if not game:
        response_object = {
            'status': 'fail',
            'message': 'Game does not exist.',
        }
        return response_object, 409

    if(game['status'] != 'in_progress'):
        response_object = {
            'status': 'fail',
            'message': 'Game is not in progress.',
        }
        return response_object, 409
    
    if(game_mode != GameMode.multiplayer):
        response_object = {
            'status': 'fail',
            'message': 'Game is not in multiplayer mode.',
        }
        return response_object, 409
    

    game_score = get_a_game_score(user_id, game_id)
    game_score.score = game_score.score + score
    game_score.updated_at = datetime.datetime.utcnow()
    save_changes(game_score)

    return  {
        'status': 'success',
        'message': 'Game successfully created.',
        'game_score': game_score.to_json()
    }

def get_a_game_score(user_id, game_id):
    """Get a game score given user_id and game_id"""
    return GameScore.query.filter_by(user_id=user_id, game_id=game_id).first()

def get_all_users_game_scores(game_id):
    """Get all game scores given game_id"""
    return GameScore.query.filter_by(game_id=game_id).all()

def save_changes(data):
    """Save the changes to the database"""
    db.session.add(data)
    db.session.commit()