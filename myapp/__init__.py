from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from myapp.config import Config
from flask_login import LoginManager
from flask_socketio import SocketIO
from .context_processors import inject_current_user



login_manager = LoginManager()
db = SQLAlchemy()





@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    login_manager.init_app(app)
    socketio.init_app(app)

    app.config.from_object(Config)
    app.context_processor(inject_current_user)
    db.init_app(app)

    from myapp.routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app