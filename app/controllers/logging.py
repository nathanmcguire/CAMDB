import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

def configure_logging(app):
    if not app.debug and not app.testing:
        log_level = getattr(logging, app.config['LOG_LEVEL'].upper(), logging.INFO)

        if app.config['LOG_TYPE'] == 'file':
            # Log errors to a file
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/flaskcmdb.log', maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(log_level)
            app.logger.addHandler(file_handler)
        elif app.config['LOG_TYPE'] == 'console':
            # Log errors to the console
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
            console_handler.setLevel(log_level)
            app.logger.addHandler(console_handler)

        app.logger.setLevel(log_level)
        app.logger.info('FlaskCMDB startup')

        # Email errors to the administrators
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='FlaskCMDB Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)