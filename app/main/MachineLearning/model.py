import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
from flask import current_app
LIMIT = 2036775
LIST_LIMIT = 200

def transfer(gloveFile, word2vecFile):
    glove2word2vec(gloveFile, word2vecFile)

def load_model(word2vecFile):
    print("Loading model... (this may take a while)")
    model = KeyedVectors.load_word2vec_format(word2vecFile, binary=False,limit=100000)
    return model

def get_similar_words(model, round_word):
    similar_words = model.similar_by_word(round_word, topn=len(model.key_to_index))
    return similar_words

def get_distance_between_words(similar_words, round_word, guess):
    # do not accept empty strings
    if guess == '':
        return  -1
    
    if guess == round_word:
        return 0
    for i, (word, sim) in enumerate(similar_words):
        if word == guess:
            return i + 1
    return len(similar_words) 

#transfer ('inputs/_glove.840B.300d.txt', 'inputs/_glove.840B.300d.word2vec.txt')

def check_word_in_model(word: str):
    model = current_app.config['model']
    if word in model.key_to_index:
        return True
    else:
        return False    
    
#df = pd.read_csv('../data/_glove.840B.300d.txt',sep=' ')
#model = load_model('../data/_glove.840B.300d.word2vec.txt')

def get_word_from_theme(theme: str, level: str):
    model = current_app.config['model']
    if(level == 'easy'):
        difficultyStart = 0
        difficultyEnd = 40
    elif(level == 'medium'):
        difficultyStart = 41
        difficultyEnd = 100
    elif(level == 'hard'):
        difficultyStart = 100
        difficultyEnd = 200

    custom_word_set = get_similar_words(model, theme)

    round_word = custom_word_set[np.random.randint(difficultyStart, difficultyEnd)][0]

    return round_word.lower()

def guess_word(round_word: str, guess: str):

    round_word = round_word.lower()
    guess = guess.lower()

    model = current_app.config['model']
    similar_words = get_similar_words(model, round_word)
    distance = get_distance_between_words(similar_words, round_word, guess)
    return distance

def get_similar_word_list(round_word: str):
    model = current_app.config['model']
    similar_words = model.similar_by_word(round_word, topn=LIST_LIMIT)
    json = []
    
    # build json of this format {word : value, distance : value}
    #insert first word as the round word and distance as 0
    json.append({
        'word': round_word,
        'distance': 0
    })
    for i, (word, sim) in enumerate(similar_words):
        json.append({
            'word': word,
            'distance': i + 1
        })
    response = {
        'results': json
    }
    return response

