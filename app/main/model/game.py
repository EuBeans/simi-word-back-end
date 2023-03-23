import uuid
from .. import db, flask_bcrypt
import datetime
from ..config import key
from typing import Union
import enum
from sqlalchemy import Enum

class GameMode(enum.Enum):
    timed = "timed"
    multiplayer = "multiplayer"
    team = "team"
    challenge = "challenge"

class GameLevel(enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"

class Theme(enum.Enum):
    sports = "sports"
    animals = "animals"
    fruits = "fruits"
    vegetables = "vegetables"
    food = "food"
    clothes = "clothes"
    colors = "colors"
    body = "body"
    family = "family"
    jobs = "jobs"
    transport = "transport"
    weather = "weather"
    house = "house"
    furniture = "furniture"
    kitchen = "kitchen"
    school = "school"
    office = "office"
    holidays = "holidays"
    countries = "countries"
    cities = "cities"
    science = "science"
    history = "history"

class GameStatus(enum.Enum):
    in_progress = "in_progress"
    completed = "completed"


class Game(db.Model):
    """ Game Model for storing game related details """
    __tablename__ = "games"

    game_id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('users.public_id'))
    game_mode = db.Column(Enum(GameMode,create_constraint=True), nullable=False)
    game_level = db.Column(Enum(GameLevel,create_constraint=True), nullable=False)
    theme = db.Column(Enum(Theme,create_constraint=True), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    game_status = db.Column(Enum(GameStatus,create_constraint=True), nullable=False) 
    max_round_number = db.Column(db.Integer, nullable=False)

   #add constraints to the database
    __table_args__ = (
        db.CheckConstraint('score >= 0', name='score_positive'),
        db.CheckConstraint('start_time < end_time', name='start_time_before_end_time'),
        db.CheckConstraint('max_round_number <= 5', name='max_round_number_less_than_5'),
    )

    def __repr__(self) -> str:
        #print json representation of the object
        return str(self.to_json())
    
    def to_json(self):
        return {
            'game_id': self.game_id,
            'user_id': self.user_id,
            'game_mode': self.game_mode.value,
            'game_level': self.game_level.value,
            'theme': self.theme.value,
            'score': self.score,
            'start_time': str(self.start_time) ,
            'end_time': str(self.end_time),
            'created_at': str(self.created_at),
            'game_status': self.game_status.value,
            'max_round_number': self.max_round_number
        }



