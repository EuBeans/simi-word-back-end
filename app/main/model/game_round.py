import uuid
from .. import db, flask_bcrypt
import datetime
from ..config import key
from typing import Union
import enum
from sqlalchemy import Enum


class GameRoundStatus(enum.Enum):
    in_progress = "in_progress"
    completed = "completed"
    timed_out = "timed_out"
    skipped = "skipped"
    

class GameRound(db.Model):
    """ Game Round Model for storing game round related details """
    __tablename__ = "game_rounds"

    round_id = db.Column(db.String(100), primary_key=True)
    game_id = db.Column(db.String(100), db.ForeignKey('games.game_id'), nullable=False)
    round_number = db.Column(db.Integer, nullable=False)
    round_word = db.Column(db.String(100), nullable=False)
    round_score = db.Column(db.Integer, nullable=False)
    status = db.Column(Enum(GameRoundStatus,create_constraint=True), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    number_of_guesses = db.Column(db.Integer, nullable=False)

    # constraint unique game_id and round_number
    __table_args__ = (db.UniqueConstraint('game_id', 'round_number', name='_game_id_round_number_uc'),)
    
    def __repr__(self) -> str:
        return "<Game '{}'>".format(self.game_id)



    def to_json(self):
        return {
            'round_id': self.round_id,
            'game_id': self.game_id,
            'round_number': self.round_number,
            'round_word': self.round_word,
            'status': self.status.value,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
            'start_time': str(self.start_time),
            'end_time': str(self.end_time),
            'number_of_guesses': self.number_of_guesses,
            'round_score': self.round_score,
        }



