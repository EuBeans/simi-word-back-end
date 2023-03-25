from app.main.socketio import socketio
from flask_socketio import emit, join_room, leave_room

@socketio.on('connect')
def handle_connect():
    print('Connecte to socketio')

@socketio.on('disconnect')
def handle_disconnect():
    print('Disconnected')

@socketio.on('join_game')
def handle_join_game(data):
    game_id = data['game_id']
    join_room(game_id)

@socketio.on('leave_game')
def handle_leave_game(data):
    game_id = data['game_id']
    leave_room(game_id)

@socketio.on('guess_word')
def handle_guess_word(data):
    word = data['word']
    game_id = data['game_id']
    #emit('guess_response', {'distance': get_distance(word, game_id)})
