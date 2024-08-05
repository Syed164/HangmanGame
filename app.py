from flask import Flask, render_template, request
import random
from waitress import serve
import webbrowser
import threading

app = Flask(__name__)

word_list = {
    'abruptly': 'suddenly, unexpectedly',
    'absurd': 'wildly unreasonable, illogical',
    'baboon': 'a type of large monkey',
    'camel': 'a desert animal with humps',
    'awkward': 'clumsy, causing difficulty',
    'bookworm': 'a person who loves to read',
    'cycle': 'a series of events that repeat',
    'galaxy': 'a system of stars, planets',
    'galvanize': 'to shock or excite someone',
    'gossip': 'casual talk about others',
    'icebox': 'another term for refrigerator',
    'injury': 'harm or damage to the body',
    'ivory': 'a hard white material from elephant tusks',
    'jackpot': 'a large cash prize',
    'idiot': 'a stupid person',
    'jelly': 'a sweet spread made from fruit',
    'jigsaw': 'a puzzle with many pieces',
    'jinx': 'a person or thing that brings bad luck',
    'lucky': 'having good fortune',
    'luxury': 'a state of great comfort or elegance',
    'pizza': 'a dish of Italian origin',
    'puppy': 'a young dog',
    'puzzling': 'difficult to understand',
    'quartz': 'a hard, crystalline mineral',
    'queue': 'a line of people or vehicles',
    'strength': 'the quality of being strong',
    'whiskey': 'a distilled alcoholic drink',
    'xylophone': 'a musical instrument',
    'yummy': 'delicious',
    'yatch': 'a large boat used for pleasure',
    'zoo': 'a place where animals are kept for public viewing',
    'zigzag': 'a pattern with sharp turns',
    'zombie': 'a fictional undead being',
    'adventure': 'an unusual and exciting experience',
    'butterfly': 'an insect with large, colorful wings',
    'computer': 'an electronic device for storing and processing data',
    'dinosaur': 'a large extinct reptile',
    'elephant': 'a large mammal with a trunk',
    'festival': 'a day or period of celebration',
    'giraffe': 'a tall African mammal with a long neck',
    'helicopter': 'a type of aircraft with rotating blades',
    'kangaroo': 'a marsupial from Australia',
    'laughter': 'the action or sound of laughing',
    'mountain': 'a large natural elevation of the earth',
    'ocean': 'a vast body of salt water',
    'pyramid': 'a monumental structure with a square base and triangular sides',
    'rainbow': 'a spectrum of colors in the sky caused by refraction of sunlight',
    'sunflower': 'a tall plant with a large yellow flower',
    'treasure': 'a quantity of precious metals, gems, or other valuable objects',
    'universe': 'all existing matter and space considered as a whole',
    'volcano': 'a mountain or hill with a crater through which lava erupts',
    'wizard': 'a person who practices magic',
    'yogurt': 'a creamy dairy product made by fermenting milk'
}

stages = [r'''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========
''', r'''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========
''', r'''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========
''', r'''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========
''', r'''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
''', r'''
  +---+
  |   |
  O   |
      |
      |
      |
=========
''', r'''
  +---+
  |   |
      |
      |
      |
      |
=========
''']

@app.route('/')
def index():
    return render_template('index.html', game_active=False, game_data=None)

@app.route('/start_game', methods=['POST'])
def start_game():
    chosen_word, clue = random.choice(list(word_list.items()))
    word_length = len(chosen_word)
    display = ['_'] * word_length
    lives_left = 6
    game_data = {
        'chosen_word': chosen_word,
        'clue': clue,
        'display': display,
        'lives_left': lives_left,
        'stages': stages[lives_left],
        'game_active': True
    }
    return render_template('index.html', game_active=True, game_data=game_data)

@app.route('/guess', methods=['POST'])
def guess():
    data = request.form
    chosen_word = data['chosen_word']
    display = list(data['display'])
    lives_left = int(data['lives_left'])
    guess = data['guess'].lower()

    if guess in display:
        message = "You already guessed that letter."
    elif guess in chosen_word:
        for position, letter in enumerate(chosen_word):
            if letter == guess:
                display[position] = letter
        if '_' not in display:
            return render_template('index.html', game_active=False, game_data={'message': "YOU WIN!", 'display': display, 'lives_left': lives_left, 'stages': stages[lives_left]})
        message = ""
    else:
        lives_left -= 1
        if lives_left == 0:
            return render_template('index.html', game_active=False, game_data={'message': f"GAME OVER! You lose, the word was {chosen_word}", 'display': display, 'lives_left': lives_left, 'stages': stages[lives_left]})
        message = "That's not in the word. You lose a life."
    
    game_data = {
        'chosen_word': chosen_word,
        'clue': data['clue'],
        'display': display,
        'lives_left': lives_left,
        'stages': stages[lives_left],
        'game_active': True,
        'message': message
    }
    return render_template('index.html', game_active=True, game_data=game_data)

def open_browser():
    webbrowser.open('http://127.0.0.1:5000/')

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    serve(app, host='0.0.0.0', port=5000)
