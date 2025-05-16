from flask import Blueprint, render_template, redirect, url_for, request, flash,session
from datetime import timedelta
from sqlalchemy.exc import IntegrityError, DataError, DatabaseError, InterfaceError, InvalidRequestError
from werkzeug.routing import BuildError
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from .models import User, Clue, RoomCompletion
from . import db,login_manager
from .forms import login_form, register_form, delete_form
import logging

auth = Blueprint('auth',__name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
def load_all_users():
    return User.query.all()

@auth.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        if current_user.admin:
            return redirect(url_for('auth.admin'))
        return redirect(url_for('main.start_game'))
    
    form = login_form()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):
                # Set session as permanent if remember is checked
                if form.remember.data:
                    session.permanent = True
                
                # Login user and update active status
                login_user(user, remember=form.remember.data)
                user.is_active = True
                db.session.commit()
                
                # Clear any existing flash messages
                session.pop('_flashes', None)
                
                # Redirect based on user type
                if user.admin:
                    return redirect(url_for('auth.admin'))
                return redirect(url_for('main.start_game'))
            else:
                flash('Invalid username or password', 'danger')
        except Exception as e:
            logging.error(f"Login error: {str(e)}")
            flash('An error occurred during login. Please try again.', 'danger')
            db.session.rollback()
    
    return render_template(
        'login.html',
        form=form,
        login_status=current_user.is_authenticated
    )

@auth.route('/register', methods=['POST','GET'])
@login_required
def register():
    if current_user.admin == True :
        form = register_form()
        if form.validate_on_submit():
            try:
                username = form.username.data
                password = form.password.data
                admin = form.admin.data
                newuser = User(
                    username = username,
                    password = generate_password_hash(password),
                    admin = admin
                )
                db.session.add(newuser)
                db.session.commit()
                flash(f'Account Successfully Created','success')
                return redirect(url_for('auth.login'))
            except InvalidRequestError:
                db.session.rollback()
                flash(f"Something went wrong!", "danger")
            except IntegrityError:
                db.session.rollback()
                flash(f"User already exists!.", "warning")
            except DataError:
                db.session.rollback()
                flash(f"Invalid Entry", "warning")
            except InterfaceError:
                db.session.rollback()
                flash(f"Error connecting to the database", "danger")
            except DatabaseError:
                db.session.rollback()
                flash(f"Error connecting to the database", "danger")
            except BuildError:
                db.session.rollback()
                flash(f"An error occured !", "danger")    
    return render_template('auth.html', form=form, text='Create account', title='Register', btn_action='Register account')

@auth.route('/logout')
def logout():
    current_user.is_active = False
    db.session.commit()
    session.clear()
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():    
    if current_user.is_authenticated:
        if current_user.admin == True:
            form = delete_form()
            if form.validate_on_submit():
                logging.debug(f"Delete form submitted. User ID: {form.user_id.data}")
                try:
                    user = User.query.get(form.user_id.data)
                    logging.debug(f"Found user: {user.username if user else 'None'}")
                    if user and not user.admin:  # Prevent deleting admin users
                        logging.debug(f"Deleting user: {user.username}")
                        # Delete associated clues first
                        Clue.query.filter_by(user_id=user.id).delete()
                        # Delete room completions
                        RoomCompletion.query.filter_by(user_id=user.id).delete()
                        # Now delete the user
                        db.session.delete(user)
                        db.session.commit()
                        flash('User successfully deleted!', 'success')
                    else:
                        logging.debug("Cannot delete - user is admin or not found")
                        flash('Cannot delete admin users!', 'warning')
                except Exception as e:
                    logging.error(f"Error deleting user: {str(e)}")
                    db.session.rollback()
                    flash('Error deleting user!', 'danger')
            users = load_all_users()            
            return render_template('admin.html', userlist=users, login_status=current_user.is_authenticated, delete_form=form)

@login_manager.unauthorized_handler
def unauthorized_callback():
    logging.debug('Unauth Handler')
    return redirect(url_for('auth.login'))