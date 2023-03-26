from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.game_controller import api as game_ns
from .main.controller.game_round_controller import api as game_round_ns
from .main.controller.round_word_controller import api as round_word_ns
from .main.controller.game_score_controller import api as game_score_ns

blueprint = Blueprint('api', __name__)
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    blueprint,
    title='SemiWord API',
    version='1.0',
    description='API for SemiWord project',
    authorizations=authorizations,
    security='apikey'
)

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
api.add_namespace(game_ns, path='/game')
api.add_namespace(game_round_ns, path='/game_round')
api.add_namespace(round_word_ns, path='/round_word')
api.add_namespace(game_score_ns, path='/game_score')

