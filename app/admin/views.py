# coding:utf-8

from . import admin
from flask import render_template, redirect, url_for


@admin.route('/')
def index():
    return render_template('admin/index.html')


@admin.route('/login.html')
def login():
    return render_template('login.html')


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
