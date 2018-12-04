# coding:utf-8
from flask import Flask, render_template
import pymysql
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

mail = Mail()
login_manager = LoginManager()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('./setting.py')
    app.config.from_pyfile('./secure.py')
    register_blueprint(app)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    login_manager.login_message = "请先登录或注册"

    db.init_app(app)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    with app.app_context():
        db.create_all()
    return app


def register_blueprint(app):
    from app.admin import admin
    app.register_blueprint(admin)
