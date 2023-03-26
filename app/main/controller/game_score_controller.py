from flask import request
from flask_restx import Resource
from app.main.util.decorator import token_required
from ..util.dto import GameScoreDto
from ..service.game_score_service import save_new_game_score, get_all_users_game_scores, get_a_game_score, update_game_score
from ..service.auth_helper import Auth
from typing import Dict, Tuple

api = GameScoreDto.api
_game_score = GameScoreDto.game_score
_game_score_create = GameScoreDto.game_score_create
_game_score_update = GameScoreDto.game_score_update


@api.route('/<game_id>')
@api.param('game_id', 'The Game identifier')
class GameScoreList(Resource):
    @api.doc('list_of_scores')
    @token_required 
    @api.marshal_list_with(_game_score, envelope='data')
    def get(self,game_id):
        """List all registered Score for Game and user id"""
        return get_all_users_game_scores(game_id)

@api.route('/')
class GameScore(Resource):
    @api.expect(_game_score_create, validate=True)
    @token_required
    @api.response(201, 'Score successfully created.')
    @api.doc('create a new Score')
    def post(self) -> Tuple[Dict[str, str], int]:
        """Creates a new Word"""
        user, status = Auth.get_logged_in_user(request)
        user_id = user.get('data').get('user_id')
        if not user_id:
            return 
        data = request.json
        return save_new_game_score(user_id=user_id,game_id=data['game_id'])
    
    @api.expect(_game_score_update, validate=True)
    @token_required
    @api.response(201, 'Score successfully updated.')
    @api.doc('update a Score')
    def put(self) -> Tuple[Dict[str, str], int]:
        """Updates a Score"""
        user, status = Auth.get_logged_in_user(request)
        user_id = user.get('data').get('user_id')
        if not user_id:
            return 
        data = request.json
        return update_game_score(user_id=user_id,data=data)

@api.route('/<game_score_id>')
@api.param('game_score_id', 'The Game Score identifier')
@api.response(404, 'Game Score not found.')
class GameScore(Resource):
    @api.doc('get a game score')
    @token_required
    @api.marshal_with(_game_score)
    def get(self, game_score_id):
        """get a game score given its identifier"""
        game_score = get_a_game_score(game_score_id)
        if not game_score:
            api.abort(404)
        else:
            return game_score



