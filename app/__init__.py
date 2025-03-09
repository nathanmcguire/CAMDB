from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv
from app.utils import format_datetime

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

    # Register Blueprints
    from app.controllers.index import index_bp
    from app.controllers.assets import assets_bp
    from app.controllers.controls import controls_bp
    from app.controllers.user import user_bp
    from app.controllers.dashboard import dashboard_bp
    app.register_blueprint(index_bp)
    app.register_blueprint(assets_bp)
    app.register_blueprint(controls_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(dashboard_bp)

    # Create all tables
    with app.app_context():
        db.create_all()

    return app