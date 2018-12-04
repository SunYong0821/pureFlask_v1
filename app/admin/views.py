# coding:utf-8
from app.admin.forms import LoginForm
from app.models import User
from . import admin
from flask import render_template, redirect, url_for, request


@admin.route('/')
def index():
    return render_template('admin/index.html')


@admin.route('/login.html', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            pass
    return render_template('user/login.html', form=form)


@admin.route('/logout.html')
def logout():
    return redirect(url_for('login'))


@admin.route('/videolist.html')
def videolist():
    return render_template('admin/videolist.html')


@admin.route('/playvideo.html')
def playvideo():
    return render_template('admin/playvideo.html')


@admin.route('/biotoolslist.html')
def biotoolslist():
    return render_template('admin/biotoolslist.html')


@admin.route('/infotoolslist.html')
def infotoolslist():
    return render_template('admin/infotoolslist.html')


@admin.route('/runtool.html')
def runtool():
    return render_template('admin/runtool.html')


@admin.route('/profile.html')
def profile():
    return render_template('admin/profile.html')


@admin.route('/loginlog.html')
def loginlog():
    return render_template('admin/loginlog.html')
