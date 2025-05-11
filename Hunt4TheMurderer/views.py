from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from . import login_manager, db
from .models import RoomCompletion, Clue
from .puzzles import ROOM_PUZZLES
from .clues import ROOM_CLUES
import json
from random import shuffle

# Initial rooms that are available from the start
INITIAL_ROOMS = {'Courtyard', 'LivingRoom', 'Kitchen'}

# Room dependencies - which rooms need to be completed to unlock others
ROOM_DEPENDENCIES = {
    'Garage': 'Courtyard',
    'Bedroom': 'LivingRoom',
    'DiningRoom': 'Kitchen',
    'Bathroom': 'Bedroom',
    'Study': 'Bathroom',
    'GamesRoom': 'Bathroom'
}

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

def get_completed_rooms():
    if not current_user.is_authenticated:
        return []
    completions = RoomCompletion.query.filter_by(
        user_id=current_user.id,
        completed=True
    ).all()
    return [c.room_name for c in completions]

def is_room_available(room_name, completed_rooms):
    # Initial rooms are always available
    if room_name in INITIAL_ROOMS:
        return True
    
    # Check if the required room is completed
    required_room = ROOM_DEPENDENCIES.get(room_name)
    if required_room and required_room in completed_rooms:
        return True
    
    return False

@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def home():
    shuffle(imgList)
    return render_template('index.html', login_status=current_user.is_authenticated)

@main.route('/story')
@login_required
def story():
    return render_template('story.html', login_status=current_user.is_authenticated)

@main.route('/intro')
@login_required
def intro():
    return render_template('intro.html', username=current_user.username, login_status=current_user.is_authenticated)

@main.route('/start_game')
@login_required
def start_game():
    return redirect(url_for('main.story'))

@main.route('/game', methods=['GET', 'POST'])
@login_required
def mansion():    
    completed_rooms = get_completed_rooms()
    available_rooms = [room for room in imgList if is_room_available(room, completed_rooms)]
    clues = Clue.query.filter_by(user_id=current_user.id).order_by(Clue.discovered_at.desc()).all()
    
    return render_template('game/main.html', 
                         imgList=imgList, 
                         login_status=current_user.is_authenticated,
                         completed_rooms=completed_rooms,
                         available_rooms=available_rooms,
                         clues=clues)

@main.route('/contact', methods=['GET','POST'])
def contact():
    return 'Contact Us'

@main.route('/room/<room_name>', methods=['GET', 'POST'])
@login_required
def room(room_name):
    if room_name not in imgList:
        return redirect(url_for('main.mansion'))
    
    # Check if room is available
    completed_rooms = get_completed_rooms()
    if not is_room_available(room_name, completed_rooms):
        flash('This room is not available yet. Complete the required room first!', 'error')
        return redirect(url_for('main.mansion'))
    
    # Check if room is already completed
    completion = RoomCompletion.query.filter_by(
        user_id=current_user.id,
        room_name=room_name
    ).first()
    
    if request.method == 'POST':
        user_answer = request.form.get('answer', '').strip().lower()
        correct_answer = ROOM_PUZZLES[room_name]['answer'].lower()
        
        if user_answer == correct_answer:
            if not completion:
                completion = RoomCompletion(
                    user_id=current_user.id,
                    room_name=room_name,
                    completed=True
                )
                db.session.add(completion)
            elif not completion.completed:
                completion.completed = True
            db.session.commit()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': True,
                    'message': 'Correct answer! Room completed!'
                })
            else:
                flash('Correct answer! Room completed!', 'success')
                return render_template('game/room_detail.html',
                                    room_name=room_name,
                                    login_status=current_user.is_authenticated,
                                    puzzle=ROOM_PUZZLES[room_name],
                                    completed=True,
                                    clue=ROOM_CLUES[room_name])
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': False,
                    'message': 'Incorrect answer. Try again!'
                })
            else:
                flash('Incorrect answer. Try again!', 'error')
    
    return render_template('game/room_detail.html',
                         room_name=room_name,
                         login_status=current_user.is_authenticated,
                         puzzle=ROOM_PUZZLES[room_name],
                         completed=completion.completed if completion else False)

@main.route('/add_clue/<room_name>', methods=['POST'])
@login_required
def add_clue(room_name):
    if room_name not in ROOM_CLUES:
        return jsonify({'success': False, 'message': 'Invalid room!'})
    
    # Check if clue already exists
    existing_clue = Clue.query.filter_by(
        user_id=current_user.id,
        room_name=room_name
    ).first()
    
    if not existing_clue:
        clue = Clue(
            user_id=current_user.id,
            room_name=room_name,
            clue_text=ROOM_CLUES[room_name]
        )
        db.session.add(clue)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Clue added to your diary!'})
    else:
        return jsonify({'success': False, 'message': 'You already have this clue in your diary!'})

@main.route('/clear_messages', methods=['POST'])
@login_required
def clear_messages():
    # Clear any flashed messages from the session
    session.pop('_flashes', None)
    return jsonify({'success': True})

@main.route('/submit_final_answer', methods=['POST'])
@login_required
def submit_final_answer():
    suspect = request.form.get('suspect')
    room = request.form.get('room')
    weapon = request.form.get('weapon')
    
    correct_answer = {
        'suspect': 'Jacob Green',
        'room': 'Bedroom',
        'weapon': 'Revolver'
    }
    
    if suspect == correct_answer['suspect'] and room == correct_answer['room'] and weapon == correct_answer['weapon']:
        return jsonify({
            'success': True,
            'message': 'Congratulations! You\'ve solved the mystery!'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'That\'s not quite right. Review the clues and try again!'
        })

@main.route('/congratulations')
@login_required
def congratulations():
    return render_template('congratulations.html', login_status=current_user.is_authenticated)