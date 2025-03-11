from flask import Blueprint, render_template, current_app
from app import db

errors_bp = Blueprint('errors', __name__)

@errors_bp.app_errorhandler(404)
def not_found_error(error):
    current_app.logger.error(f'404 error: {error}', exc_info=error)
    return render_template('errors/404.html'), 404

@errors_bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    current_app.error(f'500 error: {error}', exc_info=error)
    return render_template('errors/500.html'), 500