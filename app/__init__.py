# coding:utf-8
from flask import Flask, render_template
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

mail = Mail()
login_manager = LoginManager()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
    app.config.from_pyfile('./setting.py')
    app.config.from_pyfile('./secure.py')

    register_blueprint(app)

    mail.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    login_manager.login_message = "请先登录或注册"
    login_manager.remember_cookie_duration = timedelta(days=1)
    
    db.init_app(app)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def page_forbidden(error):
        return render_template('403.html'), 403

    with app.app_context():
        db.create_all()
    return app


def register_blueprint(app):
    from app.admin import admin
    from app.tools import tools
    app.register_blueprint(admin)
    app.register_blueprint(tools, url_prefix="/tools")
