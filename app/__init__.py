# coding:utf-8
from flask import Flask, render_template
import pymysql
from app.models import db


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('./setting.py')
    app.config.from_pyfile('./secure.py')
    register_blueprint(app)
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
