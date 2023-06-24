from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from flask_login import login_required, current_user
from . import login_manager
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
@main.route('/home', methods=['GET', 'POST'])
def home():
    shuffle(imgList)
    return render_template('index.html', login_status=current_user.is_authenticated)

@main.route('/start_game')
@login_required
def start_game():
    print('Main - Start Game')
    return render_template('intro.html', username=current_user.username, login_status=current_user.is_authenticated)

@main.route('/game', methods=['GET', 'POST'])
@login_required
def mansion():    
    return render_template('game/main.html', imgList=map(json.dumps, imgList), login_status=current_user.is_authenticated)

@main.route('/contact', methods=['GET','POST'])
def contact():
    return 'Contact Us'