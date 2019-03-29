# -*- coding: utf-8 -*-
from app.models import User

__author__ = 'zhengpanone'
from app.extensions import db


def modify_score():
    """定时修改用户积分，每天12点重置积分"""
    with db.app.app_context():
        User.query.filter_by(confirm=1).update({'scores': 10})
        db.session.commit()
