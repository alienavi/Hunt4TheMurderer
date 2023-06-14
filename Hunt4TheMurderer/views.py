from flask import Blueprint, render_template, jsonify, request
import json
from random import shuffle

imgList = [
        'Bathroom',
        'Bedroom',
        'Courtyard',
        'DiningRoom',
        'GamesRoom',
        'Garage',
        'Kitchen',
        'LivingRoom',
        'Study'
    ]

main = Blueprint('main',__name__)

@main.route('/', methods=['GET', 'POST'])
def home():
    shuffle(imgList)
    return render_template('index.html')

@main.route('/start_game', methods=['GET', 'POST'])
def start_game():
    return render_template('intro.html')

@main.route('/game', methods=['GET', 'POST'])
def mansion():    
    return render_template('game/main.html', imgList=map(json.dumps, imgList))

@main.route('/kitchen', methods=['GET', 'POST'])
def kitchen():
    print(request.form)
    if 'countries' in request.form:
        name = request.form.get('countries')
        print(name)
        if(name == 'INDIA'):
            result = 1
        else:
            result = 0
        return jsonify(message=result)
    else:
        return '',400