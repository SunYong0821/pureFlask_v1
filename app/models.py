# coding:utf-8

import os
import pathlib
from datetime import datetime

from flask import current_app, flash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Seralize
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import login_manager, db


class Permission:
    COMMON = 0x01  # 关注其他用户
    VIP = 0x02  # 评论
    OURS = 0x04  # 写文章
    ADMIN = 0x08  # 管理评论


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    default = db.Column(db.Boolean)
    permissions = db.Column(db.Integer)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    users = db.relationship('User', back_populates='role')

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permission(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return f'<Role {self.name}>'


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    _password = db.Column('pwd', db.String(128))
    email = db.Column(db.String(100), unique=True)
    info = db.Column(db.Text)
    img = db.Column(db.String(255))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    confirm = db.Column(db.Boolean, default=False)
    scores = db.Column(db.Integer, default=100, comment="积分")
    userlogs = db.relationship('Userlog', backref='user')
    task_id = db.relationship('Tasklist', backref='user')
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    role = db.relationship('Role', back_populates='users')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.set_role()

    def set_role(self):
        if self.role is None:
            if self.email == current_app.config['MAIL_USERNAME']:
                self.role = Role.query.filter_by(name='ADMIN').first()
            if self.email.endswith('@microanaly.com'):
                self.role = Role.query.filter_by(name='OURS').first()
            else:
                self.role = Role.query.filter_by(name='COMMON').first()

    # 当前账号激活状态
    @property
    def password(self):
        return self._password

    # 密码设置为hash
    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    # 生成token方法
    def generate_token(self, expiration=36000):
        s = Seralize(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def check_token(token):
        s = Seralize(current_app.config['SECRET_KEY'])
        # 从当前的token中拿出
        try:
            id = s.loads(token)['id']
        except:
            return False
        user = User.query.get(id)
        if not user:
            return False
        if not user.confirm:
            user.confirm = True
            db.session.add(user)
            db.session.commit()
            user_profile = pathlib.Path('./app/static/user/' + user.name + '/profile')
            user_task = pathlib.Path('./app/static/user/' + user.name + '/task')
            if user_profile.exists() or user_task.exists():
                pass
            else:
                os.makedirs(user_profile)
                os.makedirs(user_task)
        return True

    @staticmethod
    def reset_password(token, new_password):
        s = Seralize(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            flash("token已失效请重新发送", "danger")
            return False
        uid = data.get('id')
        user = User.query.get(uid)
        user.password = new_password
        db.session.add(user)
        db.session.commit()
        return True

    def check_password(self, pwd):
        return check_password_hash(self._password, pwd)

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def __repr__(self):
        return f'<User {self.name}>'


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))


class Userlog(db.Model):
    __tablename__ = 'userlog'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Userlog {self.id}>'


class Videolist(db.Model):
    __tablename__ = 'videolist'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    img = db.Column(db.String(255))
    type = db.Column(db.String(255))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    playvideo = db.relationship('Playvideo', backref='videolist')

    @classmethod
    def find_all_video_by_page(cls):
        videolist = Videolist.query.filter_by(type="inside").order_by(Videolist.addtime).distinct().all()
        return videolist

    def __repr__(self):
        return f'<Videolist {self.title}>'


class Playvideo(db.Model):
    __tablename__ = 'playvideo'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)
    playnum = db.Column(db.BigInteger)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    video_owner = db.Column(db.String(255), comment='视频讲解人')

    videolist_id = db.Column(db.Integer, db.ForeignKey('videolist.id'))

    def __repr__(self):
        return f'<Playvideo {self.title}>'


class Toolslist(db.Model):
    __tablename__ = 'toolslist'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255))
    img = db.Column(db.String(255))
    info = db.Column(db.Text)
    group = db.Column(db.String(100))
    usenum = db.Column(db.BigInteger)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return f'<Toolslist {self.title}>'


class Tasklist(db.Model):
    __tablename__ = 'tasklist'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    taskid = db.Column(db.String(300), unique=True)
    status = db.Column(db.String(100))
    resulturl = db.Column(db.String(255))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f'<Tasklist {self.title}>'


class SCIhub(db.Model):
    __tablename__ = 'sci_hub'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    time = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return f'<sci_hub {self.name}>'


class Menu(db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True, comment='编号')
    parent_id = db.Column(db.Integer, db.ForeignKey('menu.id'), comment='父id')
    level = db.Column(db.Integer, comment='级别')
    name = db.Column(db.String(255), comment='菜单名称')
    parent_name = db.Column(db.String(255), comment='父节点名称')
    icon = db.Column(db.String(255), comment='图标颜色')
    url = db.Column(db.String(255), comment='链接地址')
    add_time = db.Column(db.DateTime, default=datetime.now, comment='添加时间')

    child_menus = db.relationship('Menu')

    @classmethod
    def get_tree(cls):
        all_menu = Menu.query.all()  # 查看所有menu
        menu_list = []
        # 查找所有一级菜单
        for root in all_menu:
            if root.level == 1:
                menu_list.append(root)
        # 为一级菜单设置子菜单
        for menu in menu_list:
            menu.child_menus = cls.get_child_menu(menu.id, all_menu)
        return menu_list

    @classmethod
    def get_child_menu(cls, parent_id, all_menu):
        """
        :param parent_id: 父节点id
        :param all_menu: 所有节点
        :return child_list: 子节点
        """
        child_menu_list = []
        # 遍历所有节点，将父节点id与子节点的parent_id进行比较
        for nav in all_menu:
            if nav.parent_id == parent_id:
                child_menu_list.append(nav)
        # 递归 把子菜单的子菜单在此循环
        if len(child_menu_list) != 0:
            for m in child_menu_list:
                m.child_menus = (cls.get_child_menu(m.id, all_menu))
        return child_menu_list


if __name__ == '__main__':
    db.create_all()

    """ from werkzeug.security import generate_password_hash
    admin = Admin(
        name='admin',
        pwd=generate_password_hash('12345@')
    )
    db.session.add(admin)
    db.session.commit() """
