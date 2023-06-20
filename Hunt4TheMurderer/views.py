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
def home():
    shuffle(imgList)
    return render_template('index.html')

@main.route('/start_game', methods=['GET', 'POST'])
def start_game():
    return render_template('intro.html')

@main.route('/game', methods=['GET', 'POST'])
def mansion():    
    return render_template('game/main.html', imgList=map(json.dumps, imgList))

@main.route('/admin')
@login_required
def admin():
    if current_user.is_authenticated:
        if current_user.username.lower() == 'admin' :
            return 'Howdy Admin'
        else :
            return 'Forbidden'
    
@main.route('/player')
@login_required
def player():
    if current_user.is_authenticated:
        return 'Player - ' + current_user.username
    else:
        return 'Login Required'

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('auth.login'))