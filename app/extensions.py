# -*- coding: utf-8 -*-
__author__ = 'zhengpanone'

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from datetime import timedelta
from flask_apscheduler import APScheduler

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
scheduler = APScheduler()

login_manager.login_view = 'admin.login'
login_manager.login_message = "请先登录或注册"
login_manager.remember_cookie_duration = timedelta(days=1)
