from flask import request, current_app
from flask_restx import Resource
from app.main.service.auth_helper import Auth
from ..util.dto import AuthDto
from typing import Dict, Tuple
from app.main.MachineLearning.model import load_model

api = AuthDto.api
user_auth = AuthDto.user_auth


@api.route('/login')
class UserLogin(Resource):
    """
        User Login Resource
    """
    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    def post(self) -> Tuple[Dict[str, str], int]:
        # get the post data
        post_data = request.json
        #load model
        current_app.config['MODEL'] = load_model('app/main/data/_glove.840B.300d.word2vec.txt')
        return Auth.login_user(data=post_data)


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @api.doc('logout a user')
    def post(self) -> Tuple[Dict[str, str], int]:
        # get auth token
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)


def load_m():
    """
    # Load model in cache
    if not cache.get('model_ml'):
        model_ml = load_model('app/main/data/_glove.840B.300d.word2vec.txt')
        cache.set('model_ml', model_ml)
        #insert model into current_app so that it can be accessed by the flask app
        app.model = model_ml
        print('Model loaded')
    else:
        #model is in cache
        #get model from cache
        model_ml = cache.get('model_ml')
        #insert model into current_app so that it can be accessed by the flask app
        current_app.model = model_ml
    return
    """
    