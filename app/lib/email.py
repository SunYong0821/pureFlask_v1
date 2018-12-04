# -*- coding: utf-8 -*-
from threading import Thread

from flask import current_app, render_template
from flask_mail import Message

from app import mail


def async_send_mail(app, msg):
    # 获取文件上下文
    with app.app_context():
        mail.send(message=msg)


def send_mail(subject, to, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(subject=subject, recipients=[to], sender=current_app.config['MAIL_USERNAME'])
    msg.html = render_template(template, **kwargs)
    send = Thread(target=async_send_mail(app, msg))
    send.start()
