from .. import db, flask_bcrypt
import datetime
from ..config import key
from typing import Union


class RoundWords(db.Model):
    """ Round Word Association Model for storing word association related details """
    __tablename__ = "round_words"

    word_id = db.Column(db.String(100), primary_key=True)
    round_id = db.Column(db.String(100), db.ForeignKey('game_rounds.round_id'), nullable=False)
    user_id = db.Column(db.String(100), db.ForeignKey('users.public_id'), nullable=False)
    word = db.Column(db.String(100), nullable=False)
    guess_number = db.Column(db.Integer, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    

    # constraints
    __table_args__ = (
        #distance must be positive
        db.CheckConstraint('distance >= 0'),
        #guess_number must be positive
        db.CheckConstraint('guess_number >= 0'),
    )


    def __repr__(self) -> str:
        return "<Game '{}'>".format(self.game_id)
    
    def to_json(self):
        return {
            'word_id': self.word_id,
            'round_id': self.round_id,
            'user_id': self.user_id,
            'word': self.word,
            'is_correct': self.is_correct,
            'distance': self.distance,
            'guess_number': self.guess_number,
            'created_at':  str(self.created_at),
        }
    
    



    



