from flask import Flask, render_template
from config import Config
from flask_session import Session
from flask_socketio import SocketIO

def page_not_found(e):
    return render_template('404.html'), 404

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .views import main
    app.register_blueprint(main)
    
    from .filters import filters
    app.register_blueprint(filters)

    app.register_error_handler(404, page_not_found)

    Session(app)
    socketio = SocketIO(app)

    return app, socketio