import uuid
import datetime
from app.main import db
from app.main.model.game_round import GameRound, GameRoundStatus
from app.main.service.game_service import get_a_game, end_game, update_score
from app.main.service.game_score_service import update_game_score
from typing import Dict, Tuple
from app.main.MachineLearning.model import get_word_from_theme, get_similar_word_list
from app.main.model.game import Game, GameMode
def save_new_game_round(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    """Creates a new Game Round"""
    game = get_a_game(data['game_id'])
    if not game:
        response_object = {
            'status': 'fail',
            'message': 'Game does not exist.',
        }
        return response_object, 409
    
    #get highest round number round with same game_id
    prev_game_round = GameRound.query.filter_by(game_id=data['game_id']).order_by(GameRound.round_number.desc()).first()
    round_number = 1
    response_object = None
    if prev_game_round:
        if prev_game_round.round_number < game.max_round_number:
            round_number = prev_game_round.round_number + 1
        elif  prev_game_round.round_number == game.max_round_number:
            response_object = {
                'status': 'fail',
                'message': 'Game has reached max round number.',
            }
        if(prev_game_round.status.value == GameRoundStatus.in_progress.value):
            end_game_round(prev_game_round.round_id)

        if response_object:
            return response_object, 409
    
    round_word = get_word_from_theme(game.theme.value, game.game_level.value)
    new_game_round = GameRound(
        round_id = str(uuid.uuid4()),
        game_id= data['game_id'],
        round_word = round_word,
        round_number= round_number,
        status= GameRoundStatus.in_progress.value,
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow(),
        start_time=datetime.datetime.utcnow(),
        number_of_guesses=0,
        round_score=0
    )
    save_changes(new_game_round)

    return  {
        'status': 'success',
        'message': 'Game Round successfully created.',
        'game_round': new_game_round.to_json()
    } , 201

def update_number_guesses(round_id):
    """Update number of guesses for game round"""
    game_round = GameRound.query.filter_by(round_id=round_id).first()
    if not game_round:
        response_object = {
            'status': 'fail',
            'message': 'Game does not exist.',
        }
        return response_object, 409
    else:
        game_round.number_of_guesses = game_round.number_of_guesses + 1
        game_round.updated_at = datetime.datetime.utcnow()
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Game successfully updated.',
            'game_round': game_round.to_json()
        }
        return response_object, 200

def end_game_round(round_id, status = GameRoundStatus.completed.value, user_id = None, guess_number = 0):
    """End game round with status"""
    game_round = GameRound.query.filter_by(round_id=round_id).first()
    if not game_round:
        response_object = {
            'status': 'fail',
            'message': 'Game does not exist.',
        }
        return response_object, 409
    else:

        
        game_round.status = GameRoundStatus(status)

        game_round.end_time = datetime.datetime.utcnow()
        game_round.updated_at = datetime.datetime.utcnow()
        game_round.round_score = calculate_score(game_round)
        db.session.commit()

        game = get_a_game(game_id  = game_round.game_id)
        
        if(status == GameRoundStatus.completed.value):
            if game.game_mode.value == GameMode.multiplayer.value and user_id:
                #update the score in the game Score table
                score = calculate_score(game_round, guess_number)
                update_game_score(user_id, game_round.game_id,score)
            else:

                update_score(game_round.game_id, game_round.round_score)
        new_game_round = None
        if(game_round.round_number == game.max_round_number):
            end_game(game_round.game_id)
        else:
            #start new round
            new_game_round = save_new_game_round({'game_id': game_round.game_id})[0]['game_round']


        response_object = {
            'status': 'success',
            'message': 'Game successfully updated.',
            'prev_game_round': game_round.to_json(),
            'new_game_round': new_game_round
        }
        return response_object, 200

def calculate_score(game_round, guess_number = None):
    """Calculate score for game round"""
    if not game_round:
        response_object = {
            'status': 'fail',
            'message': 'Game does not exist.',
        }
        return response_object, 409
    else:
        score = 0
        if game_round.status.value == GameRoundStatus.completed.value:
            if(guess_number):
                score = 100 - guess_number
            else:
                score = 100 - game_round.number_of_guesses
        return score

def get_a_game_round(round_id: str) -> GameRound:
    game_round = GameRound.query.filter_by(round_id=round_id).first()
    if not game_round:
        return None
    else:
        return game_round.to_json()

def get_all_game_rounds(game_id: str) -> GameRound:
    #for each game round in game_id, return game_round.to_json()
    return [gameRound.to_json() for gameRound in GameRound.query.filter_by(game_id=game_id).all()]

def get_all_similar_words_for_game_round(round_id: str) -> Dict[str, str]: 
    game_round = GameRound.query.filter_by(round_id=round_id).first()
    if not game_round:
        return None
    else:
        return get_similar_word_list(game_round.round_word)

        

def save_changes(data: GameRound) -> None:
    db.session.add(data)
    db.session.commit()

