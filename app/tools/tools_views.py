# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
import threading
from uuid import uuid4

from flask import current_app, url_for, render_template, redirect, abort, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app import db
from . import tools
from app.tools.tools_forms import RevComForm, PoolingForm, SplitLaneForm, DEGForm, VolcanoForm, MAplotForm, EZCLForm, \
    VennForm, EdgeRForm, DESeq2Form, KEGGbublleForm, PCAForm
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

        return redirect(url_for("admin.index"))
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

        return redirect(url_for("admin.index"))
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

        return redirect(url_for("admin.index"))
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

        return redirect(url_for("admin.index"))
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

        return redirect(url_for("admin.index"))
    return render_template('admin/tools/volcano.html', form=form)


@tools.route('/ma_plot.html', methods=["GET", "POST"])
@login_required
def ma_plot():
    form = MAplotForm()
    if form.validate_on_submit():
        taskdir, uuid, inputfile = taskprepare("MA图", form)

        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(
                f"Options: {form.fc.data} {form.fccol.data} {form.pq.data} {form.pqcol.data} {form.exp1.data} {form.exp2.data} {form.outpre.data}\n")
        script = f"perl ./app/static/program/ma_plot/MA_plot.pl -i {inputfile} -log2col {form.fccol.data} -exp1col {form.exp1.data} -exp2col {form.exp2.data} -pvalue {form.pq.data} -pCol {form.pqcol.data} -prefix {form.outpre.data} -f {form.fc.data} 2>>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()

        return redirect(url_for("admin.index"))
    return render_template('admin/tools/ma_plot.html', form=form)


@tools.route('/ezcollinear.html', methods=["GET", "POST"])
@login_required
def ezcollinear():
    form = EZCLForm()
    if form.validate_on_submit():
        f1 = secure_filename(form.fai1.data.filename)
        f2 = secure_filename(form.fai2.data.filename)
        link = secure_filename(form.links.data.filename)
        uuid = uuid4().hex
        taskdir = f"./app/static/user/{current_user.name}/task/{uuid}"
        os.makedirs(taskdir + "/out")
        in1 = taskdir + "/" + f1
        in2 = taskdir + "/" + f2
        in3 = taskdir + "/" + link
        form.fai1.data.save(in1)
        form.fai2.data.save(in2)
        form.links.data.save(in3)
        if os.path.getsize(in1) > 10 * 1024 * 1024 or os.path.getsize(in2) > 10 * 1024 * 1024 or os.path.getsize(
                in3) > 10 * 1024 * 1024:
            shutil.rmtree(taskdir)
            abort(413)

        task = Tasklist(
            title="简单共线性图",
            taskid=uuid,
            status="进行中",
            resulturl=taskdir,
            user_id=int(current_user.id)
        )
        db.session.add(task)
        db.session.commit()

        tool = Toolslist.query.filter_by(title="简单共线性图").first()
        tool.usenum += 1
        db.session.add(tool)
        db.session.commit()

        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(
                f"Options: {form.name.data} {form.opacity.data} {form.outpre.data}\n")
        script = f"perl ./app/static/program/ezcollinear/collinearity.pl {in1},{in2} {form.name.data} {in3} {form.outpre.data} {form.opacity.data} 2>>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()

        return redirect(url_for("admin.index"))
    return render_template('admin/tools/ezcollinear.html', form=form)


@tools.route('/venn.html', methods=["GET", "POST"])
@login_required
def venn():
    form = VennForm()
    if form.validate_on_submit():
        uuid = uuid4().hex
        taskdir = f"./app/static/user/{current_user.name}/task/{uuid}"
        os.makedirs(taskdir + "/out")
        files = request.files.getlist('files')
        filelist = []
        for i in files:
            filename = secure_filename(i.filename)
            pfile = taskdir + '/' + filename
            filelist.append(pfile)
            i.save(pfile)
            if os.path.getsize(pfile) > 10 * 1024 * 1024:
                shutil.rmtree(taskdir)
                abort(413)

        task = Tasklist(
            title="Venn图",
            taskid=uuid,
            status="进行中",
            resulturl=taskdir,
            user_id=int(current_user.id)
        )
        db.session.add(task)
        db.session.commit()

        tool = Toolslist.query.filter_by(title="Venn图").first()
        tool.usenum += 1
        db.session.add(tool)
        db.session.commit()

        filestr = ",".join(filelist)
        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(
                f"Options: {form.head.data} {form.col.data}\n")
        script = f"perl ./app/static/program/venn/venn.pl -l {filestr} -h {form.head.data} -col {form.col.data} 2>>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()

        return redirect(url_for("admin.index"))
    return render_template('admin/tools/venn.html', form=form)


@tools.route('/edger.html', methods=["GET", "POST"])
@login_required
def edger():
    form = EdgeRForm()
    if form.validate_on_submit():
        taskdir, uuid, inputfile = taskprepare("edgeR差异分析", form)

        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(
                f"Options: {form.exp1.data} {form.exp2.data} {form.bcv.data} {form.gene.data} {form.outpre.data}\n")
        script = f"perl ./app/static/program/edger/DiffExp_edgeR.pl -i {inputfile} -count1col {form.exp1.data} -count2col {form.exp2.data} -genecol {form.gene.data} -bcv {form.bcv.data} -prefix {form.outpre.data} 2>>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()

        return redirect(url_for("admin.index"))
    return render_template('admin/tools/edger.html', form=form)


@tools.route('/deseq2.html', methods=["GET", "POST"])
@login_required
def deseq2():
    form = DESeq2Form()
    if form.validate_on_submit():
        taskdir, uuid, inputfile = taskprepare("DESeq2差异分析", form)

        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(
                f"Options: {form.exp1.data} {form.exp2.data} {form.gene.data} {form.outpre.data}\n")
        script = f"perl ./app/static/program/deseq2/DiffExp_DeSeq2.pl -i {inputfile} -count1col {form.exp1.data} -count2col {form.exp2.data} -genecol {form.gene.data} -prefix {form.outpre.data} 2>>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()

        return redirect(url_for("admin.index"))
    return render_template('admin/tools/deseq2.html', form=form)


@tools.route('/keggbublle.html', methods=["GET", "POST"])
@login_required
def keggbublle():
    form = KEGGbublleForm()
    if form.validate_on_submit():
        taskdir, uuid, inputfile = taskprepare("KEGG气泡图", form)

        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(
                f"Options: {form.pathcol.data} {form.genecol.data} {form.bgcol.data} {form.pqcol.data} {form.outpre.data}\n")
        script = f"perl ./app/static/program/keggbublle/Pathway_EnrichFigure.pl -i {inputfile} -pathcol {form.pathcol.data} -genecol {form.genecol.data} -background {form.bgcol.data} -pcol {form.pqcol.data} -prefix {form.outpre.data} 2>>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()

        return redirect(url_for("admin.index"))
    return render_template('admin/tools/keggbublle.html', form=form)


@tools.route('/pca.html', methods=["GET", "POST"])
@login_required
def pca():
    form = PCAForm()
    if form.validate_on_submit():
        taskdir, uuid, inputfile = taskprepare("PCA图", form)

        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(
                f"Options: {form.expcol.data} {form.genecol.data} {form.outpre.data}\n")
        script = f"perl ./app/static/program/pca/PCA.pl -i {inputfile} -expcol {form.expcol.data} -genecol {form.genecol.data} -prefix {form.outpre.data} 2>>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()

        return redirect(url_for("admin.index"))
    return render_template('admin/tools/pca.html', form=form)
