# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
import threading
from uuid import uuid4

from flask import current_app, url_for, render_template, redirect, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app import db
from . import tools
from app.tools.tools_forms import RevComForm, PoolingForm, SplitLaneForm, DEGForm, VolcanoForm
from app.models import Tasklist, Toolslist


def runtools(app, script, uuid):
    with app.app_context():
        rc = subprocess.run(script, shell=True)
        tl = Tasklist.query.filter_by(taskid=uuid).first()
        if rc.returncode == 0:
            tl.status = "任务完成"
            db.session.add(tl)
        else:
            tl.status = "运行错误"
            db.session.add(tl)
        db.session.commit()


def taskprepare(toolname, form):
    filename = secure_filename(form.url.data.filename)
    uuid = uuid4().hex
    # 不能使用pathlib，与flask存储文件用法冲突
    taskdir = f"./app/static/user/{current_user.name}/task/{uuid}"
    os.makedirs(taskdir + "/out")
    inputfile = taskdir + "/" + filename
    form.url.data.save(inputfile)
    if os.path.getsize(inputfile) > 10 * 1024 * 1024:
        shutil.rmtree(taskdir)
        abort(413)

    # 导入任务数据库
    task = Tasklist(
        title=toolname,
        taskid=uuid,
        status="进行中",
        resulturl=taskdir,
        user_id=int(current_user.id)
    )
    db.session.add(task)
    db.session.commit()

    # 导入使用次数
    tool = Toolslist.query.filter_by(title=toolname).first()
    tool.usenum += 1
    db.session.add(tool)
    db.session.commit()

    return taskdir, uuid, inputfile


@tools.route('/rev_com.html', methods=["GET", "POST"])
@login_required
def rev_com():
    form = RevComForm()
    if form.validate_on_submit():
        taskdir, uuid, inputfile = taskprepare("DNA反向互补", form)

        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(f"Options: {form.func.data}\n")
        # 异步运行执行程序
        script = f"python ./app/static/program/rev_com/rev_com.py {inputfile} {form.func.data} 2>>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()

        return redirect(url_for("admin.index", page=1))
    return render_template('admin/tools/rev_com.html', form=form)


@tools.route('/pooling.html', methods=["GET", "POST"])
@login_required
def pooling():
    form = PoolingForm()
    if form.validate_on_submit():
        taskdir, uuid, inputfile = taskprepare("文库Pooling", form)

        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(
                f"Options: {form.lane.data} {form.vol.data} {form.sizes.data}\n")
        script = f"python ./app/static/program/pooling/libraryPooling.py {inputfile} {form.lane.data} {form.vol.data} {form.sizes.data} 2>>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()

        return redirect(url_for("admin.index", page=1))
    return render_template('admin/tools/pooling.html', form=form)


@tools.route('/splitlane.html', methods=["GET", "POST"])
@login_required
def splitlane():
    form = SplitLaneForm()
    if form.validate_on_submit():
        taskdir, uuid, inputfile = taskprepare("文库分Lane", form)

        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(f"Options: {form.lane.data}\n")
        script = f"python ./app/static/program/splitlane/splitlane.py {inputfile} {form.lane.data} 2>>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()

        return redirect(url_for("admin.index", page=1))
    return render_template('admin/tools/splitlane.html', form=form)


@tools.route('/deg_filter.html', methods=["GET", "POST"])
@login_required
def deg_filter():
    form = DEGForm()
    if form.validate_on_submit():
        taskdir, uuid, inputfile = taskprepare("差异表达筛选", form)

        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(
                f"Options: {form.fc.data} {form.fccol.data} {form.pq.data} {form.yuzhi.data} {form.pqcol.data} {form.outpre.data}\n")
        if form.pq.data == "1":
            script = f"perl ./app/static/program/deg_filter/Select_DiffexpGene.pl -i {inputfile} -fc {form.fc.data} -fccolumn {form.fccol.data} -pvalue {form.yuzhi.data} -pcolumn {form.pqcol.data} -head -prefix {form.outpre.data} 2>>{taskdir}/run.log"
        else:
            script = f"perl ./app/static/program/deg_filter/Select_DiffexpGene.pl -i {inputfile} -fc {form.fc.data} -fccolumn {form.fccol.data} -fdr {form.yuzhi.data} -fdrcolumn {form.pqcol.data} -head -prefix {form.outpre.data} 2>>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()

        return redirect(url_for("admin.index", page=1))
    return render_template('admin/tools/deg_filter.html', form=form)


@tools.route('/volcano.html', methods=["GET", "POST"])
@login_required
def volcano():
    form = VolcanoForm()
    if form.validate_on_submit():
        taskdir, uuid, inputfile = taskprepare("火山图", form)

        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(
                f"Options: {form.fc.data} {form.fccol.data} {form.pq.data} {form.pqcol.data} {form.outpre.data}\n")
        script = f"perl ./app/static/program/volcano/Volcano_plot.pl -i {inputfile} -f {form.fc.data} -log2col {form.fccol.data} -pvalue {form.pq.data} -pCol {form.pqcol.data} -prefix {form.outpre.data} 2>>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()

        return redirect(url_for("admin.index", page=1))
    return render_template('admin/tools/volcano.html', form=form)
