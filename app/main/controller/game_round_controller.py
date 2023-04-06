from flask import request
from flask_restx import Resource
from app.main.MachineLearning.model import load_model
from app.main.util.decorator import token_required
from ..util.dto import GameRoundDto
from ..service.game_round_service import get_a_game_round, save_new_game_round, get_all_game_rounds, end_game_round, get_all_similar_words_for_game_round
from ..service.auth_helper import Auth
from typing import Dict, Tuple

api = GameRoundDto.api
_game_round = GameRoundDto.game_round
_game_round_create = GameRoundDto.game_round_create
_game_round_update = GameRoundDto.game_round_update
_game_round_all_similar_words = GameRoundDto.game_round_all_similar_words

@api.route('/<game_id>')
@api.param('game_id', 'The Game Round identifier')
class GameRoundList(Resource):
    @api.doc('list_of_games_round')
    @token_required 
    @api.marshal_list_with(_game_round, envelope='data')
    def get(self,game_id):
        """List all registered games round"""
        return get_all_game_rounds(game_id)

@api.route('/')
class GameRound(Resource):
    @api.expect(_game_round_create, validate=True)
    @token_required
    @api.response(201, 'Game Round successfully created.')
    @api.doc('create a new game round')
    def post(self) -> Tuple[Dict[str, str], int]:
        """Creates a new Game  round"""
        data = request.json
        return save_new_game_round(data=data)
    
    @api.expect(_game_round_update, validate=True)
    @token_required
    @api.response(201, 'Game Round successfully ended.')
    @api.doc('create a new game round')
    def patch(self) -> Tuple[Dict[str, str], int]:
        """End game round with status """
        data = request.json
        return end_game_round(round_id = data['game_round_id'], status = data['status'])


    


@api.route('/<round_id>/similar_words')
@api.param('round_id', 'The Game Round identifier')
@api.response(404, 'Game Round not found.')
class GameRound(Resource):
    @api.doc('get all similar words for a game round')
    @token_required
    @api.marshal_with(_game_round_all_similar_words)
    def get(self, round_id):
        """get all similar words for a game round given its identifier"""
        words = get_all_similar_words_for_game_round(round_id)
        print(words)
        if not words:
            api.abort(404)
        else:
            return words
        
