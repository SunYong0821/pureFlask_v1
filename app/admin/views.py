# coding:utf-8

from . import admin
from flask import render_template, redirect, url_for


@admin.route('/')
def index():
    return render_template('admin/index.html')


@admin.route('/login/')
def login():
    return render_template('login.html')


@admin.route('/logout/')
def logout():
    return redirect(url_for('login'))


@admin.route('/videolist/')
def videolist():
    return render_template('admin/videolist.html')


@admin.route('/playvideo/')
def playvideo():
    return render_template('admin/playvideo.html')


@admin.route('/biotoolslist/')
def biotoolslist():
    return render_template('admin/biotoolslist.html')


@admin.route('/infotoolslist/')
def infotoolslist():
    return render_template('admin/infotoolslist.html')


@admin.route('/runtool/')
def runtool():
    return render_template('admin/runtool.html')


@admin.route('/profile/')
def profile():
    return render_template('admin/profile.html')


@admin.route('/loginlog/')
def loginlog():
    return render_template('admin/loginlog.html')
