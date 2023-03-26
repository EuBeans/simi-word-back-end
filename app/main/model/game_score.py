import uuid
from .. import db, flask_bcrypt
import datetime
from ..config import key
from typing import Union
import enum
from sqlalchemy import Enum


class GameScore(db.Model):
    """ Game Score Model for storing player score for a game """
    __tablename__ = "game_scores"

    score_id = db.Column(db.String(100), primary_key=True)
    game_id = db.Column(db.String(100), db.ForeignKey('games.game_id'), nullable=False)
    user_id = db.Column(db.String(100), db.ForeignKey('users.public_id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    # constraint unique game_id and user_id
    __table_args__ = (db.UniqueConstraint('game_id', 'user_id', name='_game_id_user_id_uc'),)

    def __repr__(self) -> str:
        return "<Game '{}'>".format(self.game_id)
    
    def to_json(self):
        return {
            'id': self.score_id,
            'game_id': self.game_id,
            'user_id': self.user_id,
            'score': self.score,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
        }


