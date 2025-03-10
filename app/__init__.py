from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv
from app.utils import format_datetime
import os
import sqlalchemy as sa
import sqlalchemy.orm as so

# Load environment variables from .env
load_dotenv()

# Initialize extensions here, but don't initialize them until we create the app
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=None):
    app = Flask(__name__)

    app.jinja_env.filters['format_datetime'] = format_datetime

    # Load configuration from config.py
    app.config.from_object(config_class or 'app.config.Config')

    # Initialize extensions here
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = 'users.login'

    # Register Blueprints
    from app.controllers.index import index_bp
    from app.controllers.assets import assets_bp
    from app.controllers.asset_types import asset_types_bp
    from app.controllers.controls import controls_bp
    from app.controllers.control_frameworks import control_frameworks_bp
    from app.controllers.safeguards import safeguards_bp
    from app.controllers.users import users_bp
    from app.controllers.dashboard import dashboard_bp
    from app.controllers.microblog import microblog_bp
    from app.controllers.posts import posts_bp
    app.register_blueprint(index_bp)
    app.register_blueprint(assets_bp)
    app.register_blueprint(asset_types_bp)
    app.register_blueprint(controls_bp)
    app.register_blueprint(control_frameworks_bp)
    app.register_blueprint(safeguards_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(microblog_bp)
    app.register_blueprint(posts_bp)

    # Create all tables
    with app.app_context():
        db.create_all()

    @app.shell_context_processor
    def make_shell_context():
        return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}

    from app.cli import register_commands
    register_commands(app)

    return app

from app.models import User, Post

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
