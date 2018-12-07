# coding:utf-8

from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Seralize

from app import login_manager, db

import os, pathlib


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    _password = db.Column('pwd', db.String(128))
    email = db.Column(db.String(100), unique=True)
    info = db.Column(db.Text)
    img = db.Column(db.String(255))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())
    confirm = db.Column(db.Boolean, default=False)

    userlogs = db.relationship('Userlog', backref='user')
    task_id = db.relationship('Tasklist', backref='user')

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    # 当前账号激活状态

    @property
    def password(self):
        return self._password

    # 密码设置为hash
    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    # 生成token方法
    def generate_token(self):
        s = Seralize(current_app.config['SECRET_KEY'])
        return s.dumps({'id': self.id})

    def check_token(token):
        s = Seralize(current_app.config['SECRET_KEY'])
        # 从当前的token中拿出
        try:
            id = s.loads(token)['id']
        except:
            return False
        u = User.query.get(id)
        if not u:
            return False
        if not u.confirm:
            u.confirm = True
            db.session.add(u)
            db.session.commit()
            os.makedirs(pathlib.Path('./app/static/user/' + u.name + '/profile'))
            os.makedirs(pathlib.Path('./app/static/user/' + u.name + '/task'))
        return True

    def reset_password(token, new_password):
        s = Seralize(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        user = User.query.get(uid)
        user.password = new_password
        db.session.add(user)
        return True

    def check_password(self, pwd):
        return check_password_hash(self._password, pwd)

    def __repr__(self):
        return f'<User {self.name}>'


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))


class Userlog(db.Model):
    __tablename__ = 'userlog'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Userlog {self.id}>'


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    auths = db.Column(db.String(1000))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())

    userid = db.relationship('User', backref='role')

    def __repr__(self):
        return f'<Role {self.name}>'


class Videolist(db.Model):
    __tablename__ = 'videolist'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    img = db.Column(db.String(255))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())

    playvideo = db.relationship('Playvideo', backref='videolist')

    def __repr__(self):
        return f'<Videolist {self.title}>'


class Playvideo(db.Model):
    __tablename__ = 'playvideo'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)
    playnum = db.Column(db.BigInteger)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())

    videolist_id = db.Column(db.Integer, db.ForeignKey('videolist.id'))

    def __repr__(self):
        return f'<Playvideo {self.title}>'


class Toolslist(db.Model):
    __tablename__ = 'toolslist'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    img = db.Column(db.String(255))
    info = db.Column(db.Text)
    usenum = db.Column(db.BigInteger)
    group = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())

    def __repr__(self):
        return f'<Toolslist {self.title}>'

class Tasklist(db.Model):
    __tablename__ = 'tasklist'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    taskid = db.Column(db.String(255), unique=True)
    status = db.Column(db.String(255))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f'<Tasklist {self.title}>'


if __name__ == '__main__':
    db.create_all()

    """ from werkzeug.security import generate_password_hash
    admin = Admin(
        name='admin',
        pwd=generate_password_hash('12345@')
    )
    db.session.add(admin)
    db.session.commit() """
