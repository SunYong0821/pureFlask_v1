# coding:utf-8
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    info = db.Column(db.Text)
    img = db.Column(db.String(255))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())
    uuid = db.Column(db.String(255), unique=True)

    userlogs = db.relationship('Userlog', backref='user')
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    def __repr__(self):
        return f'<User {self.name}>'


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
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())

    def __repr__(self):
        return f'<Toolslist {self.title}>'


if __name__ == '__main__':
    db.create_all()

    """ from werkzeug.security import generate_password_hash
    admin = Admin(
        name='admin',
        pwd=generate_password_hash('12345@')
    )
    db.session.add(admin)
    db.session.commit() """
