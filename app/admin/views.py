# coding:utf-8
from datetime import timedelta

from flask import current_app, send_from_directory, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app.admin.forms import LoginForm, RegisterForm, ForgetPasswordForm, ForgetPasswordRequestForm, RevComForm, \
    EditProfileForm
from app.lib.email import send_mail
from app.models import User, db, Userlog, Toolslist, Tasklist, Videolist, Playvideo
from . import admin
from flask import render_template, redirect, url_for, request, flash
from uuid import uuid4
import os, threading, subprocess, pathlib


@admin.route('/index/<int:page>.html', methods=["GET", "POST"])
@login_required
def index(page=None):
    if page is None:
        page = 1
    page_data = Tasklist.query.filter_by(
        user_id=int(current_user.id)
    ).order_by(
        Tasklist.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/index.html', page_data=page_data)


@admin.route("/download/<path:dirname>", methods=['GET'])
def download(dirname):
    root_dir = pathlib.Path(os.getcwd())
    return send_from_directory(root_dir / dirname, 'out.gz', as_attachment=True)


@admin.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash("用户不存在，请注册", 'info')
            return redirect(url_for('admin.register'))
        elif not user.confirm:
            flash("请前往邮箱激活账号", 'info')
        elif user.check_password(form.pwd.data):
            userlog = Userlog()
            userlog.ip = request.remote_addr
            userlog.user_id = user.id
            login_user(user, remember=True, duration=timedelta(seconds=3600))  # duration 是设置remember_token的过期时间
            #  设置session 过期时间   remember_token和session 必须同时设置过期时间
            session.permanent = True
            current_app.permanent_session_lifetime = timedelta(seconds=3600)
            flash("登录成功", "success")
            db.session.add(userlog)
            db.session.commit()
            return redirect(url_for('admin.index', page=1))
        flash("密码错误", "warning")
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
        flash("激活成功，请登录", "success")
    else:
        flash("激活失败", "danger")
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
            flash("邮件已发送到你的邮箱" + accoutn_email + "请及时查收", "success")
            return redirect(url_for('admin.login'))
        flash('该邮箱未注册！', "warning")
    return render_template("user/forget_password_request.html", form=form)


@admin.route('/forget_password.html/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ForgetPasswordForm(request.form)
    if request.method == "POST" and form.validate():
        success = User.reset_password(token, form.pwd.data)
        if success:
            flash("密码重置成功", "success")
            return redirect(url_for('admin.login'))
        else:
            flash("密码重置失败", "danger")
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
        videolist_id=video_list_id).order_by(Playvideo.id).all()
    if play_video:
        if id == 0:
            video = play_video[0]
        else:
            video = Playvideo.query.filter_by(id=id).first()
        video.playnum = video.playnum + 1
        db.session.add(video)
        db.session.commit()
    else:
        flash("没有可播放视频", "danger")
        return redirect(url_for('admin.videolist'))

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
            tl.status = "运行错误"
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
        # 不能使用pathlib，与flask存储文件用法冲突
        taskdir = f"./app/static/user/{current_user.name}/task/{uuid}"
        os.makedirs(taskdir)
        inputfile = taskdir + "/" + filename
        form.url.data.save(inputfile)

        # 导入任务数据库
        task = Tasklist(
            title="DNA反向互补",
            taskid=uuid,
            status="进行中",
            resulturl=inputfile + ".gz",
            user_id=int(current_user.id)
        )
        db.session.add(task)
        db.session.commit()

        # 异步运行执行程序
        script = f"python ./app/static/program/rev_com/rev_com.py {inputfile} {form.func.data} 2>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()

        return redirect(url_for("admin.index", page=1))
    return render_template('admin/tools/rev_com.html', form=form)
