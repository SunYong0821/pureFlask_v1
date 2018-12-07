# coding:utf-8
from flask import current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app.admin.forms import LoginForm, RegisterForm, ForgetPasswordForm, ForgetPasswordRequestForm, RevComForm, \
    EditProfileForm
from app.lib.email import send_mail
from app.models import User, db, Userlog, Toolslist, Tasklist, Videolist, Playvideo
from . import admin
from flask import render_template, redirect, url_for, request, flash
from uuid import uuid4
import os, threading, subprocess


@admin.route('/')
@login_required
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
            login_user(user, remember=True)
            flash("登录成功")
            db.session.add(userlog)
            db.session.commit()
            return redirect(url_for('admin.index'))
        flash("密码错误")
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
        user = User.query.filter_by(email=accoutn_email).first()
        if user:
            send_mail(to=accoutn_email, subject='重置您的密码', template='email/reset_password.html', user=user,
                      token=user.generate_token())
            flash("邮件已发送到你的邮箱" + accoutn_email + "请及时查收")
            return redirect(url_for('admin.login'))
        flash('该邮箱未注册！')
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
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))


@admin.route('/videolist.html')
@login_required
def videolist():
    video_list = Videolist.find_all_video_by_page()
    return render_template('admin/videolist.html', video_list=video_list)


@admin.route('/<int:video_list_id>/<int:id>/playvideo_list.html', methods=['GET', 'POST'])
@login_required
def play_video_list(video_list_id, id):
    play_video = Playvideo.query.filter_by(
        videolist_id=video_list_id).order_by(Playvideo.addtime).all()
    if id == 0:
        video = play_video[0]
    else:
        video = Playvideo.query.filter_by(id=id).first()
    return render_template('admin/playvideo.html', play_video=play_video, video=video)


@admin.route('/biotoolslist.html', methods=["GET"])
@login_required
def biotoolslist():
    tools_list = Toolslist.query.filter_by(
        group="bio"
    ).order_by(
        Toolslist.addtime
    ).all()
    return render_template('admin/biotoolslist.html', tools_list=tools_list)


@admin.route('/infotoolslist.html')
@login_required
def infotoolslist():
    tools_list = Toolslist.query.filter_by(
        group="info"
    ).order_by(
        Toolslist.addtime
    ).all()
    return render_template('admin/infotoolslist.html', tools_list=tools_list)


@admin.route('/profile.html', methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.info = form.info.data
        db.session.add(current_user)
        db.session.commit()
        flash('个人信息更改成功')
        return render_template('admin/profile.html', form=form)

    form.info.data = current_user.info
    return render_template('admin/profile.html', form=form)


@admin.route('/loginlog/<int:page>.html', methods=["GET"])
@login_required
def loginlog(page=None):
    if page is None:
        page = 1
    page_data = Userlog.query.filter_by(
        user_id=int(current_user.id)
    ).order_by(
        Userlog.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/loginlog.html', page_data=page_data)


def runtools(app, script, uuid):
    with app.app_context():
        rc = subprocess.run(script, shell=True)
        tl = Tasklist.query.filter_by(taskid=uuid).first()
        if rc.returncode == 0:
            tl.status = "已完成"
            db.session.add(tl)
        else:
            tl.status = "服务区故障"
            db.session.add(tl)
        db.session.commit()


@admin.route('/tools/rev_com.html', methods=["GET", "POST"])
@login_required
def rev_com():
    form = RevComForm()
    if form.validate_on_submit():

        # 保存文件
        filename = secure_filename(form.url.data.filename)
        uuid = uuid4().hex
        taskdir = "./app/static/user/" + current_user.name + "/task/" + uuid
        os.makedirs(taskdir)
        form.url.data.save(taskdir + "/" + filename)

        # 导入任务数据库
        task = Tasklist(
            title="DNA反向互补",
            taskid=uuid,
            status="进行中",
            user_id=int(current_user.id)
        )
        db.session.add(task)
        db.session.commit()

        # 异步运行执行程序
        programpath = "python ./app/static/program/rev_com/rev_com.py "
        script = programpath + filename + " " + form.func.data
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()

        return redirect(url_for("admin.index"))
    return render_template('admin/tools/rev_com.html', form=form)
