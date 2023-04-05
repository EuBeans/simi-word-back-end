import uuid
import datetime
from app.main import db
from app.main.model.game_round import GameRoundStatus
from app.main.model.round_words import RoundWords
from app.main.service.game_round_service import get_a_game_round
from app.main.MachineLearning.model import guess_word, check_word_in_model
from app.main.service.game_round_service import update_number_guesses,end_game_round
from typing import Dict, Tuple

GUESS_LIMIT = 200
def save_new_round_word(user_id: str,data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    """Creates a new round_word_association """
    round = get_a_game_round(data['round_id'])
    guessed_word = data['word']

    if not round:
        response_object = {
            'status': 'fail',
            'message': 'Game Round does not exist.',
        }
        return response_object, 202

    if(guess_word == ""):
        response_object = {
            'status': 'fail',
            'message': 'Word cannot be empty.',
        }
        return response_object, 202

    if(not check_word_in_model(guessed_word)):
        response_object = {
            'status': 'fail',
            'message': 'Word not in model.',
        }
        return response_object, 202

    if(round['status'] != GameRoundStatus.in_progress.value):
        response_object = {
            'status': 'fail',
            'message': 'Game Round is not in progress.',
        }
        return response_object, 202
    
    # check to see if word has been used in this round
    all_words = RoundWords.query.filter_by(round_id=data['round_id'],user_id=user_id).all()
    for word in all_words:
        if word.word == guessed_word:
            response_object = {
                'status': 'fail',
                'message': 'Word already used.',
            }
            return response_object, 202

    #get previous round_word_association with same round_id
    prev_round_word = RoundWords.query.filter_by(round_id=data['round_id'],user_id=user_id).order_by(RoundWords.created_at.desc()).first()
    guess_number = 1
    if prev_round_word:
        if prev_round_word.word == guessed_word:
            response_object = {
                'status': 'fail',
                'message': 'Word already used.',
            }
            return response_object, 202
        guess_number = prev_round_word.guess_number + 1

        if(guess_number > GUESS_LIMIT):
            response_object = {
                'status': 'fail',
                'message': 'Guess limit reached.',
            }
            return response_object, 202
    

    update_number_guesses(data['round_id'])
    round_word = round['round_word']
    #get distance between words
    distance = guess_word(round_word, guessed_word)
    is_correct = False
    if distance == 0:
        is_correct = True
        end_game_round(data['round_id'],GameRoundStatus.completed.value, user_id=user_id , guess_number=guess_number)

    new_round_word= RoundWords(
        word_id = str(uuid.uuid4()),
        round_id = data['round_id'],
        user_id = user_id,
        word = guessed_word.lower(),
        guess_number = guess_number,
        distance = distance,
        is_correct = is_correct,
        created_at = datetime.datetime.utcnow(),
    )
    save_changes(new_round_word)
    return  {
        'status': 'success',
        'message': 'Word added successfully.',
        'round_word': new_round_word.to_json()
    }, 201

def get_all_round_words(round_id: str):
    #for each .to_json() in the list, it will call the to_json() method in the model
    return [round_word.to_json() for round_word in RoundWords.query.filter_by(round_id=round_id).all()]

def get_a_round_word(word_id: str):
    return RoundWords.query.filter_by(word_id=word_id).first()

def save_changes(data: RoundWords):
    db.session.add(data)
    db.session.commit()
