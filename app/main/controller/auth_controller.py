from flask import request,current_app
from flask_restx import Resource
from app.main.service.auth_helper import Auth
from app.main.workers import modelDownloaderWorker
from ..util.dto import AuthDto
from typing import Dict, Tuple

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

@api.route('/update_model')
class UpdateModel(Resource):


    @api.doc('update model')
    def post(self) -> Tuple[Dict[str, str], int]:

        cur_app = current_app._get_current_object()
        modelDownloaderWorker(cur_app)
        
        return  {
                    'status': 'success',
                    'message': 'Successfully updated model.'
                }