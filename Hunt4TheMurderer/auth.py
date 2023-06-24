from flask import Blueprint, render_template, redirect, url_for, request, flash,session
from datetime import timedelta
from sqlalchemy.exc import IntegrityError, DataError, DatabaseError, InterfaceError, InvalidRequestError
from werkzeug.routing import BuildError
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from .models import User
from . import db,login_manager
from .forms import login_form, register_form

auth = Blueprint('auth',__name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
def load_all_users():
    return User.query.all()

@auth.route('/login', methods=['GET','POST'])
def login():    
    if current_user.is_authenticated:        
        if current_user.admin == True :            
            return redirect(url_for('auth.admin'))
        else :
            return redirect(url_for('auth.player'))
    form = login_form()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                try :
                    user.is_active = True
                    db.session.commit()
                except e as error:
                    db.session.rollback()
                if user.admin == True :                    
                    return redirect(url_for('auth.admin'))
                else :
                    return redirect(url_for('auth.player'))
        except Exception as e:
            flash(e, 'Danger')
    return render_template(
        'auth.html',
        form=form,
        text='Login',
        title='Login',
        btn_action='Login'
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
        
    return render_template(
        'auth.html',
        form=form,
        text='Create account',
        title='Register',
        btn_action='Register account'
        )

@auth.route('/logout')
def logout():
    current_user.is_active = False
    db.session.commit()
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/admin', methods=['GET', 'POST'])
def admin():    
    if current_user.is_authenticated:
        if current_user.admin == True :
            users = load_all_users()            
            return render_template('admin.html', userlist=users, login_status=current_user.is_authenticated)
        else :
            return 'Forbidden'
    else :
        return redirect(url_for('auth.login'))
    
@auth.route('/player')
def player():
    if current_user.is_authenticated:
        return redirect(url_for('main.start_game'))
    else:
        return redirect(url_for('auth.login'))

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('auth.login'))