from ....manage import model

import uuid
import datetime
from flask import current_app

from app.main import db
from app.main.model.game import Game
from typing import Dict, Tuple
from ..model.game import Theme, GameMode, GameLevel, GameStatus


def get_word_set(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    """Get a word set for a game round"""
    try:
        game = Game.query.filter_by(id=data['game_id']).first()
        if game:
            word_set = model.get_word_set(game.theme, game.game_mode, game.game_level)
            return word_set, 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'Game does not exist.',
            }
            return response_object, 409
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': str(e),
        }
        return response_object, 500


