# coding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@10.10.100.2:7821/magweb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '64ebe6f0ee0411e8a8b56c92bf4f31c4'

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    info = db.Column(db.Text)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())
    uuid = db.Column(db.String(255), unique=True)

    userlogs = db.relationship('Userlog', backref='user')

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


class Video(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)
    tag = db.Column(db.String(100), unique=True)
    playnum = db.Column(db.BigInteger)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())

    def __repr__(self):
        return f'<Movie {self.id}>'


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())

    adminlogs = db.relationship('Adminlog', backref='admin')

    def __repr__(self):
        return f'<Admin {self.id}>'


class Adminlog(db.Model):
    __tablename__ = 'adminlog'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())

    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

    def __repr__(self):
        return f'<Adminlog {self.id}>'


if __name__ == '__main__':
    # db.create_all()

    from werkzeug.security import generate_password_hash
    admin = Admin(
        name='admin',
        pwd=generate_password_hash('12345@')
    )
    db.session.add(admin)
    db.session.commit()
