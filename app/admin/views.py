# coding:utf-8
from flask_login import login_user

from app.admin.forms import LoginForm, RegisterForm, ForgetPasswordForm, ForgetPasswordRequestForm
from app.lib.email import send_mail
from app.models import User, db, Userlog
from . import admin
from flask import render_template, redirect, url_for, request, flash


@admin.route('/')
def index():
    return render_template('admin/index.html')


@admin.route('/login.html', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash("用户不存在，请注册")
            return redirect(url_for('admin.register'))
        elif not user.confirm:
            flash("请前往邮箱激活账号")
        elif user.check_password(form.pwd.data):
            userlog = Userlog()
            userlog.ip = request.remote_addr
            userlog.user_id = user.id
            db.session.add(userlog)
            db.session.commit()
            login_user(user, remember=True)
            next = request.args.get('next')
            flash("登录成功")
            if not next or not next.startswith('/'):
                next = url_for('admin.index')
            return redirect(next)
    return render_template('user/login.html', form=form)


@admin.route('/register.html', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        user = User(
            email=form.email.data,
            name=form.name.data,
            password=form.pwd.data)
        db.session.add(user)
        db.session.commit()
        # 生成token
        token = user.generate_token()
        # 发送邮件
        send_mail(subject="账号激活", to=form.email.data, template='email/activate.html', user=user,
                  token=token)
        flash("注册成功请去邮箱中激活！")
        return redirect(url_for('admin.login'))
    return render_template('user/register.html', form=form)


@admin.route('/activate/<token>')
def activate(token):
    if User.check_token(token):
        flash("激活成功，请登录")
    else:
        flash("激活失败")
    return redirect(url_for('admin.login'))


@admin.route('/forget_password_request.html', methods=['GET', 'POST'])
def forget_password_request():
    form = ForgetPasswordRequestForm(request.form)
    if request.method == "POST" and form.validate():
        accoutn_email = form.email.data
        user = User.query.filter_by(email=accoutn_email).first_or_404()
        send_mail(to=accoutn_email, subject='重置您的密码', template='email/reset_password.html', user=user,
                  token=user.generate_token())
        flash("邮件已发送到你的邮箱" + accoutn_email + "请及时查收")
        return redirect(url_for('admin.login'))
    return render_template("user/forget_password_request.html", form=form)


@admin.route('/forget_password.html/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ForgetPasswordForm(request.form)
    if request.method == "POST" and form.validate():
        success = User.reset_password(token, form.pwd.data)
        if success:
            flash("密码重置成功")
            return redirect(url_for('admin.login'))
        else:
            flash("密码重置失败")
    return render_template("user/forget_password.html", form=form)


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

@admin.route('/tools/rev_com.html')
def rev_com():
    return render_template('admin/tools/rev_com.html')


@admin.route('/profile.html')
def profile():
    return render_template('admin/profile.html')


@admin.route('/loginlog.html')
def loginlog():
    return render_template('admin/loginlog.html')
