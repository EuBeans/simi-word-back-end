from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),

    })

class GameDto:
    api = Namespace('game', description='game related operations')
    game = api.model('game', {
        'user_id': fields.String(required=True, description='game user id'),
        'game_id': fields.String(description='game Identifier'),
        'score': fields.Integer(required=True, description='game score'),
        'start_time': fields.String(required=True, description='game start time'),
        'end_time': fields.String(required=True, description='game end time'),
        'created_at': fields.String(required=True, description='game created at'),
        'game_mode': fields.String(required=True, description='game game mode'),
        'game_level': fields.String(required=True, description='game game level'),
        'theme': fields.String(required=True, description='game theme'),
        'max_round_number': fields.Integer(required=True, description='game max round number'),
        'multiplayer_code': fields.String(required=True, description='game multiplayer code'),
    })
    game_create= api.model('game_create', {
        'game_mode': fields.String(required=True, description='game game mode'),
        'game_level': fields.String(required=True, description='game game level'),
        'theme': fields.String(required=True, description='game theme'),
        'max_round_number': fields.Integer(required=True, description='game max round number'),
    })
    game_update = api.model('game_update', {
        'game_id': fields.String(required=True, description='game update game id'),
        'score': fields.Integer(required=True, description='game update score'),
        'status': fields.String(required=True, description='game update status'),
    })
    

class GameRoundDto:
    api = Namespace('game_round', description='game round related operations')
    game_round = api.model('game_round', {
        'game_id': fields.String(required=True, description='game round game id'),
        
        'round_number': fields.Integer(required=True, description='game round number'),
        'round_word': fields.String(required=True, description='game round word'),
        'start_time': fields.String(required=True, description='game round start time'),
        'end_time': fields.String(required=True, description='game round end time'),
        'status': fields.String(required=True, description='game round status'),
        'number_of_guesses': fields.Integer(required=True, description='game round number of guesses'),
        'round_score': fields.Integer(required=True, description='game round score'),
    })
    game_round_create = api.model('game_round_create', {
        'game_id': fields.String(required=True, description='game round game id'),
    })
    game_round_update = api.model('game_round_update', {
        'game_round_id': fields.String(required=True, description='game round update game round id'),
        'status': fields.String(required=True, description='game round update status'),
    })

    game_round_similar_words = api.model('game_round_similar_words', {
        'word': fields.String(required=True, description='game round get all similar words word'),
        'distance': fields.Integer(required=True, description='game round get all similar words distance'),
    })
    
    game_round_all_similar_words = api.model('game_round_all_similar_words', {
        'results': fields.List(fields.Nested(game_round_similar_words), required=True, description='game round get all similar words results'),
    })


class RoundWordDto:
    api = Namespace('round_word', description='round word association related operations')
    round_word = api.model('round_word', {
        'word_id': fields.String(required=True, description='round word association word id'),
        'round_id': fields.String(required=True, description='round word association game round id'),
        'user_id': fields.String(description='round word association Identifier'),
        'guess_number': fields.Integer(required=True, description='round word association guess number'),
        'is_correct': fields.Boolean(required=True, description='round word association is correct'),
        'distance': fields.Integer(required=True, description='round word association distance'),
        'created_at': fields.String(required=True, description='round word association created at'),
    })
    round_word_create = api.model('round_word_create', {
        'word': fields.String(required=True, description='round word association word'),
        'round_id': fields.String(required=True, description='round word association game round id'),
    })

class GameScoreDto:
    api = Namespace('game_score', description='game score related operations')
    game_score = api.model('game_score', {
        'score_id': fields.String(required=True, description='game score id'),
        'game_id': fields.String(required=True, description='game score game id'),
        'user_id': fields.String(description='game score Identifier'),
        'score': fields.Integer(required=True, description='game score score'),
        'created_at': fields.String(required=True, description='game score created at'),
        'updated_at': fields.String(required=True, description='game score updated at'),
    })
    game_score_create = api.model('game_score_create', {
        'game_id': fields.String(required=True, description='game score game id'),
    })
    game_score_update = api.model('game_score_update', {
        'game_id': fields.String(required=True, description='game score update game score id'),
        'score': fields.Integer(required=True, description='game score update score'),
    })

class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })
