from asyncio.log import logger

from time import sleep
from flask import request, current_app, Flask
from flask_restx import Resource
from app.main.util.decorator import token_required
from app.main.workers import modelDownloaderWorker
from ..util.dto import GameDto
from ..service.game_service import save_new_game, get_all_games, get_a_game, end_game, get_a_game_by_multiplayer_code
from ..service.game_round_service import save_new_game_round
from ..service.round_word_service import save_new_round_word
from ..service.game_score_service import get_a_game_score, save_new_game_score
from ..service.auth_helper import Auth
from typing import Dict, Tuple
from ..socketio import socketio
from flask_socketio import emit, join_room, leave_room, rooms


thread = None

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
        return end_game(data=data)

@api.route('/<game_id>')
@api.param('game_id', 'The Game identifier')
@api.response(404, 'Game not found.')
class Game(Resource):
    @api.doc('get a game')
    @token_required
    @api.marshal_with(_game)
    def get(self, game_id):
        """get a user given its identifier"""
        game = get_a_game(game_id).to_json()
        if not game:
            api.abort(404)
        else:
            return game



@api.route('/update_model')
class UpdateModel(Resource):

    @api.doc('update model')
    def post(self) -> Tuple[Dict[str, str], int]:

        cur_app = current_app._get_current_object()
        thread = modelDownloaderWorker(cur_app)
        #TODO Load model and then return success... diferent thread, thread will send a response to the client

        #wait for the model to thread to finish
        thread.join()

        return  {
                    'status': 'success',
                    'message': 'Model has been updated successfully!'
                }



#object response for socket messages 
class SocketResponse:
    def __init__(self, status, message, data):
        self.status = status
        self.message = message
        self.data = data
    
    #convert to json
    def toJSON(self):
        return {
            'status': self.status,
            'message': self.message,
            'data': self.data
        }

@socketio.on('connect', namespace='/game')
def connect_to_socket( auth):
    user, status = Auth.get_logged_in_user_socket(auth['Authorization'])
    id = user.get('data').get('user_id')
    if not id:
        emit('disconnect', {'data': 'Disconnected'})
    print('Client connected to socketio')
    response = SocketResponse('success', 'Connected to socketio', None).toJSON()
    emit('server_response', response)

@socketio.on('disconnect')
def disconnect_from_socket():
    emit('disconnect', {'data': 'Disconnected'}, broadcast=True)
    print('User disconnected')

@socketio.on('creator_disconnect', namespace='/game')
def creator_disconnect(data):
    """
    Creator disconnects from the game
    data = {
        Authorization: token,
        }
    """
    user, status = Auth.get_logged_in_user_socket(data['Authorization'])
    id = user.get('data').get('user_id')
    if not id:
        emit('disconnect', {'data': 'Disconnected'}, broadcast=True)
    
    #get the game
    games = get_all_games(id)
    print("user", user)
    for game in games:
        print(game)
        if game['user_id'] == id:
            #delete the game
            end_game(game['game_id'])
            emit('disconnect', {'data': 'Disconnected'}, broadcast=True)

@socketio.on('create_multiplayer_game', namespace='/game')
def create_multiplayer_game(data):
    """
    Create a multiplayer game
    data = {
        Authorization: token,
        gameData: {
            GameModel
        }
    emits a server_response event:
        {
        status: 'success' or 'fail',
        message: 'Game created successfully' or 'Failed to create game',
        data: {
            GameModel
        }
    """
    user, status = Auth.get_logged_in_user_socket(data['Authorization'])
    id = user.get('data').get('user_id')
    if not id:
        emit('disconnect', {'data': 'Disconnected'}, broadcast=True)


    #create a new game 
    game = save_new_game(user_id=id, data=data['gameData'], session_id=request.sid)
    if game:
        #join the room
        join_room(game['game']["multiplayer_code"])
        game_score = save_new_game_score(user_id=id, game_id=game['game']['game_id'])

        #send the game to the client
        returnObj = {
            'game': game['game'],
            'game_score': game_score,
            'user': user.get('data').get('username')
        }
        response = SocketResponse('success', 'Game created successfully', returnObj).toJSON()
        emit('server_response', response, broadcast=True)


@socketio.on('join_multiplayer_game', namespace='/game')
def join_multiplayer_game(data):
    """
    Join a multiplayer game
    data = {
        Authorization: token,
        multiplayer_code: string
        emits a server_response event:
        {
            status: 'success' or 'fail',
            message: 'Game joined successfully' or 'Failed to join game',
            data: {
                game: GameModel,
                user: UserModel
            }
        }
    """
    user, status = Auth.get_logged_in_user_socket(data['Authorization'])
    id = user.get('data').get('user_id')
    if not id:
        emit('disconnect', {'data': 'Disconnected'}, broadcast=True)
    #get the game
    game = get_a_game_by_multiplayer_code(data['multiplayer_code'])
    print("game", game)
    if game:
        #join the room
        join_room(game["multiplayer_code"])
        

        if(not is_in_score_board(game['game_id'], id)):
            game_score = save_new_game_score(game_id=game['game_id'], user_id=id)
        else:
            game_score = get_a_game_score(id, game['game_id'])
        #send the game to the client
        returnObj = {
            'game': game,
            'game_score': game_score,
            'user': user.get('data').get('username')
        }
        response = SocketResponse('success', 'Game joined successfully', returnObj).toJSON()
        emit('server_response', response, broadcast=True)
    else:
        response = SocketResponse('fail', 'Failed to join game', None).toJSON()
        emit('server_response', response, broadcast=True)

#admin will now start the game
@socketio.on('start_new_round', namespace='/game')
def start_new_round(data):
    """
    Start a new round
    data = {
        Authorization: token,
        game_id: string
    }
    emits a server_response event:
        {
            status: 'success' or 'fail',
            message: 'Game started successfully' or 'Failed to start game',
            data: {
                round: RoundModel
                }
        }
    """
    user, status = Auth.get_logged_in_user_socket(data['Authorization'])
    id = user.get('data').get('user_id')
    if not id:
        emit('disconnect', {'data': 'Disconnected'}, broadcast=True)
    round = save_new_game_round(data)
    if round[0]['status'] == 'success':
        #send the game to the client
        response = SocketResponse('success', round[0]['message'], round).toJSON()
        emit('server_response', response, broadcast=True)
    else:
        response = SocketResponse('error',  round[0]['message'], None).toJSON()
        emit('server_response', response, broadcast=True)
        
#guess the word
@socketio.on('guess_round_word', namespace='/game')
def guess_word(data):
    """
    Guess the word
    data = {
        Authorization: token,
        game_id: string,
        round_id: string,
        word: string
        }
        
    emits a server_response event:
        {
            status: 'success' or 'fail',
            message: 'Word guessed successfully' or 'Failed to guess word',
            data: {
                round_id: string,
                word: string
            }
        }
    """
    #check if user is in the room
    user, status = Auth.get_logged_in_user_socket(data['Authorization'])
    id = user.get('data').get('user_id')
    if not id:
        emit('disconnect', {'data': 'Disconnected'}, broadcast=True)

    if(not is_in_score_board(data['game_id'],id)):
        response = SocketResponse('error', 'You are not in this room', None).toJSON()
        emit('server_response', response, broadcast=True)
        return

    #guess the word
    round_word = save_new_round_word(user_id=id, data=data)

    if(round_word[0]['status'] == 'fail'):
        response = SocketResponse('error', round_word[0]['message'], None).toJSON()
        emit('server_response', response, broadcast=True)
        return
    else:
        #send the game to the client
        response = SocketResponse('success',  round_word[0]['message'], round_word[0]["round_word"]).toJSON()
        emit('server_response', response, broadcast=True)
 
def is_in_score_board(game_id,user_id):

    score = get_a_game_score(user_id=user_id,game_id=game_id)
    if score:
        return True
    else:
        return False

def is_admin(game_id,user_id):
    #check if the user is is linked to the current game 

    game = get_a_game(game_id)
    #check if the user is the game creator
    if game['game']['user_id'] == user_id:
        return True
    else:
        return False

