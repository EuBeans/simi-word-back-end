from flask import request
from flask_restx import Resource
from app.main.util.decorator import token_required
from ..util.dto import RoundWordDto
from ..service.round_word_service import save_new_round_word, get_all_round_words, get_a_round_word
from ..service.auth_helper import Auth
from typing import Dict, Tuple

api = RoundWordDto.api
_round_word = RoundWordDto.round_word
_round_word_create = RoundWordDto.round_word_create
RoundWordDto
@api.route('/<round_id>')
@api.param('round_id', 'The Game Round identifier')
class GameRoundList(Resource):
    @api.doc('list_of_words')
    @token_required 
    @api.marshal_list_with(_round_word, envelope='data')
    def get(self,round_id):
        """List all registered words for round id"""
        return get_all_round_words(round_id)

@api.route('/')
class GameRound(Resource):
    @api.expect(_round_word_create, validate=True)
    @token_required
    @api.response(201, 'Word successfully created.')
    @api.doc('create a new Word')
    def post(self) -> Tuple[Dict[str, str], int]:
        """Creates a new Word"""
        user, status = Auth.get_logged_in_user(request)
        user_id = user.get('data').get('user_id')
        if not user_id:
            return 
        data = request.json
        return save_new_round_word(user_id=user_id,data=data)



