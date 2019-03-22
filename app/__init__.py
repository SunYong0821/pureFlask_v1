# coding:utf-8
from flask import Flask, render_template
from app.extensions import db, login_manager, mail, scheduler


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('./setting.py')
    app.config.from_pyfile('./secure.py')

    register_extensions(app)
    register_blueprint(app)
    register_errorhandlers(app)
    with app.app_context():
        db.create_all()
    return app


def register_extensions(app):
    """注册扩展"""
    db.app = app
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    scheduler.init_app(app)
    scheduler.start()


def register_errorhandlers(app):
    """注册 errorhandler """

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def page_forbidden(error):
        return render_template('403.html'), 403

    @app.errorhandler(413)
    def file_is_bigger(error):
        return render_template('413.html'), 413


def register_blueprint(app):
    """注册蓝图"""
    from app.admin import admin
    from app.tools import tools
    app.register_blueprint(admin)
    app.register_blueprint(tools, url_prefix="/tools")


def register_logging(app):
    """注册日志"""
    pass
