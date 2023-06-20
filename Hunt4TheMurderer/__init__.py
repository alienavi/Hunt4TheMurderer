from flask import Flask, render_template
from config import Config
from flask_session import Session
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def page_not_found(e):
    return render_template('404.html'), 404

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
    bcrypt.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .rooms import rooms as rooms_blueprint
    app.register_blueprint(rooms_blueprint)

    from .filters import filters as filters_blueprint
    app.register_blueprint(filters_blueprint)

    app.register_error_handler(404, page_not_found)

    Session(app)
    socketio = SocketIO(app)

    return app, socketio