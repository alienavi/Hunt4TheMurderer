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

@auth.route('/login', methods=['GET','POST'])
def login():
    form = login_form()
    if form.validate_on_submit():
        print('here')
        try:
            print(form.username.data, form.password.data)
            user = User.query.filter_by(username=form.username.data).first()
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('main.player'))
        except Exception as e:
            flash(e, 'Danger')
    return render_template(
        'auth.html',
        form=form,
        text='Login',
        title='Login',
        btn_action='Login'
    )

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/register', methods=['POST','GET'])
def register():
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
    logout_user()
    return redirect(url_for('auth.login'))