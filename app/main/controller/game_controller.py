from flask import request
from flask_restx import Resource
from app.main.util.decorator import token_required
from ..util.dto import GameDto
from ..service.game_service import save_new_game, get_all_games, get_a_game
from ..service.auth_helper import Auth
from typing import Dict, Tuple

api = GameDto.api
_game = GameDto.game
_game_create = GameDto.game_create
_gameUpdate = GameDto.game_update

@api.route('/')
class GameList(Resource):
    @api.doc('list_of_games')
    @token_required 
    @api.marshal_list_with(_game, envelope='data')
    def get(self):
        """List all registered games"""
        user, status = Auth.get_logged_in_user(request)
        print(user)
        id = user.get('data').get('user_id')
        if not id:
            return 
        return get_all_games(id)

    @api.expect(_game_create, validate=True)
    @token_required
    @api.response(201, 'Game successfully created.')
    @api.doc('create a new game')
    def post(self) -> Tuple[Dict[str, str], int]:
        """Creates a new Game """
        user, status = Auth.get_logged_in_user(request)
        id = user.get('data').get('user_id')
        if not id:
            return 
        data = request.json
        return save_new_game(user_id=id, data=data)

    @api.expect(_gameUpdate, validate=True)
    @token_required
    @api.response(201, 'Game successfully updated.')
    @api.doc('update a game')
    def put(self) -> Tuple[Dict[str, str], int]:
        """Updates a Game """
        user, status = Auth.get_logged_in_user(request)
        id = user.get('data').get('user_id')
        if not id:
            return 
        data = request.json
        return update_game(data=data)

@api.route('/<game_id>')
@api.param('game_id', 'The Game identifier')
@api.response(404, 'Game not found.')
class Game(Resource):
    @api.doc('get a game')
    @token_required
    @api.marshal_with(_game)
    def get(self, game_id):
        """get a user given its identifier"""
        game = get_a_game(game_id)
        if not game:
            api.abort(404)
        else:
            return game



