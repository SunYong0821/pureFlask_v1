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
from app.models import Tasklist, Toolslist
from app.tools.tools_forms import RevComForm, PoolingForm, SplitLaneForm, DEGForm, VolcanoForm, MAplotForm, EZCLForm, \
    VennForm, EdgeRForm, DESeq2Form, KEGGbublleForm, PCAForm, ClusterTreeForm, HeatMapForm, CorrForm, FisherForm, \
    CDS2PEPForm, KronaForm, BarForm, SpearmanForm, Bar_TreeForm, SeqlogoForm, ConvertPForm, ViolinForm, BarboxForm
from . import tools


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


def verify_file(taskdir, *args):
    for v in args:
        filename = secure_filename(v.filename)
        inputfile = taskdir + "/" + filename
        v.save(inputfile)
        if os.path.getsize(inputfile) > 10 * 1024 * 1024:
            shutil.rmtree(taskdir)
            abort(413)
    return [str(taskdir + "/" + secure_filename(v.filename)) for v in args]


def taskprepare(toolname, *args):
    uuid = uuid4().hex
    # 不能使用pathlib，与flask存储文件用法冲突
    taskdir = f"./app/static/user/{current_user.name}/task/{uuid}"
    os.makedirs(taskdir + "/out")
    inputfiles = verify_file(taskdir, *args)

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
    tool = Toolslist.query.filter_by(url=toolname).first()
    tool.usenum += 1
    db.session.add(tool)
    db.session.commit()

    return taskdir, uuid, inputfiles


@tools.route('/rev_com.html', methods=["GET", "POST"])
@login_required
def rev_com():
    form = RevComForm()
    if form.validate_on_submit():
        taskdir, uuid, inputfile = taskprepare("tools.rev_com", form.url.data)

        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(f"Options: {form.func.data}\n")
        # 异步运行执行程序
        script = f"python ./app/static/program/rev_com/rev_com.py {inputfile[0]} {form.func.data} 2>>{taskdir}/run.log"
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
        taskdir, uuid, inputfile = taskprepare("tools.pooling", form.url.data)

        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(
                f"Options: {form.lane.data} {form.vol.data} {form.sizes.data}\n")
        script = f"python ./app/static/program/pooling/libraryPooling.py {inputfile[0]} {form.lane.data} {form.vol.data} {form.sizes.data} 2>>{taskdir}/run.log"
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
        taskdir, uuid, inputfile = taskprepare("tools.splitlane", form.url.data)

        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(f"Options: {form.lane.data}\n")
        script = f"python ./app/static/program/splitlane/splitlane.py {inputfile[0]} {form.lane.data} 2>>{taskdir}/run.log"
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
        taskdir, uuid, inputfile = taskprepare("tools.deg_filter", form.url.data)

        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(
                f"Options: {form.fc.data} {form.fccol.data} {form.pq.data} {form.yuzhi.data} {form.pqcol.data} {form.outpre.data}\n")
        if form.pq.data == "1":
            script = f"perl ./app/static/program/deg_filter/Select_DiffexpGene.pl -i {inputfile[0]} -fc {form.fc.data} -fccolumn {form.fccol.data} -pvalue {form.yuzhi.data} -pcolumn {form.pqcol.data} -head -prefix {form.outpre.data} 2>>{taskdir}/run.log"
        else:
            script = f"perl ./app/static/program/deg_filter/Select_DiffexpGene.pl -i {inputfile[0]} -fc {form.fc.data} -fccolumn {form.fccol.data} -fdr {form.yuzhi.data} -fdrcolumn {form.pqcol.data} -head -prefix {form.outpre.data} 2>>{taskdir}/run.log"
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
        taskdir, uuid, inputfile = taskprepare("tools.volcano", form.url.data)

        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(
                f"Options: {form.fc.data} {form.fccol.data} {form.pq.data} {form.pqcol.data} {form.outpre.data}\n")
        script = f"perl ./app/static/program/volcano/Volcano_plot.pl -i {inputfile[0]} -f {form.fc.data} -log2col {form.fccol.data} -pvalue {form.pq.data} -pCol {form.pqcol.data} -prefix {form.outpre.data} 2>>{taskdir}/run.log"
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
        taskdir, uuid, inputfile = taskprepare("tools.ma_plot", form.url.data)

        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(
                f"Options: {form.fc.data} {form.fccol.data} {form.pq.data} {form.pqcol.data} {form.exp1.data} {form.exp2.data} {form.outpre.data}\n")
        script = f"perl ./app/static/program/ma_plot/MA_plot.pl -i {inputfile[0]} -log2col {form.fccol.data} -exp1col {form.exp1.data} -exp2col {form.exp2.data} -pvalue {form.pq.data} -pCol {form.pqcol.data} -prefix {form.outpre.data} -f {form.fc.data} 2>>{taskdir}/run.log"
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
        taskdir, uuid, inputfile = taskprepare("tools.edger", form.url.data)

        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(
                f"Options: {form.exp1.data} {form.exp2.data} {form.bcv.data} {form.gene.data} {form.outpre.data}\n")
        script = f"perl ./app/static/program/edger/DiffExp_edgeR.pl -i {inputfile[0]} -count1col {form.exp1.data} -count2col {form.exp2.data} -genecol {form.gene.data} -bcv {form.bcv.data} -prefix {form.outpre.data} 2>>{taskdir}/run.log"
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
        taskdir, uuid, inputfile = taskprepare("tools.deseq2", form.url.data)

        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(
                f"Options: {form.exp1.data} {form.exp2.data} {form.gene.data} {form.outpre.data}\n")
        script = f"perl ./app/static/program/deseq2/DiffExp_DeSeq2.pl -i {inputfile[0]} -count1col {form.exp1.data} -count2col {form.exp2.data} -genecol {form.gene.data} -prefix {form.outpre.data} 2>>{taskdir}/run.log"
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
        taskdir, uuid, inputfile = taskprepare("tools.keggbublle", form.url.data)

        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(
                f"Options: {form.pathcol.data} {form.genecol.data} {form.bgcol.data} {form.pqcol.data} {form.outpre.data}\n")
        script = f"perl ./app/static/program/keggbublle/Pathway_EnrichFigure.pl -i {inputfile[0]} -pathcol {form.pathcol.data} -genecol {form.genecol.data} -background {form.bgcol.data} -pcol {form.pqcol.data} -prefix {form.outpre.data} 2>>{taskdir}/run.log"
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
        taskdir, uuid, inputfile = taskprepare("tools.pca", form.url.data)

        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(
                f"Options: {form.expcol.data} {form.genecol.data} {form.outpre.data}\n")
        script = f"perl ./app/static/program/pca/PCA.pl -i {inputfile[0]} -expcol {form.expcol.data} -genecol {form.genecol.data} -prefix {form.outpre.data} 2>>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()

        return redirect(url_for("admin.index"))
    return render_template('admin/tools/pca.html', form=form)


@tools.route('/clustertree.html', methods=["GET", "POST"])
@login_required
def clustertree():
    form = ClusterTreeForm()
    if form.validate_on_submit():
        taskdir, uuid, inputfile = taskprepare("tools.clustertree", form.url.data)

        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(
                f"Options: {form.expcol.data} {form.method.data} {form.outpre.data}\n")
        script = f"perl ./app/static/program/clustertree/ClusterTree.pl -i {inputfile[0]} -expcol {form.expcol.data} -method {form.method.data} -prefix {form.outpre.data} 2>>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()

        return redirect(url_for("admin.index"))
    return render_template('admin/tools/clustertree.html', form=form)


@tools.route('/pheatmap.html', methods=["GET", "POST"])
@login_required
def pheatmap():
    form = HeatMapForm()
    if form.validate_on_submit():
        taskdir, uuid, inputfile = taskprepare("tools.pheatmap", form.url.data)

        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(
                f"Options: {form.namecol.data} {form.datacol.data} {form.outpre.data} {form.display_numbers.data} \
                {form.width.data} {form.height.data} {form.scale.data} {form.cluster_cols.data} {form.cluster_rows.data} \
                {form.show_colnames.data} {form.show_rownames.data}\n")
        script = f"perl ./app/static/program/pheatmap/heatmap.pl -in {inputfile[0]} -namecol {form.namecol.data} -datacol {form.datacol.data} -prefix {form.outpre.data} -scale {form.scale.data} -width {form.width.data} -height {form.height.data} -cluster_rows {form.cluster_rows.data} -cluster_cols {form.cluster_cols.data}  -show_rownames {form.show_rownames.data} -show_colnames {form.show_colnames.data} -display_numbers {form.display_numbers.data} 2>>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()

        return redirect(url_for("admin.index"))
    return render_template('admin/tools/pheatmap.html', form=form)


@tools.route('/correlation.html', methods=["GET", "POST"])
@login_required
def correlation():
    form = CorrForm()
    if form.validate_on_submit():
        taskdir, uuid, inputfile = taskprepare("tools.correlation", form.url.data)

        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(
                f"Options: {form.exp1.data} {form.exp2.data} {form.name1.data} {form.name2.data} {form.gene.data} {form.method.data} {form.outpre.data}\n")
        script = f"perl ./app/static/program/correlation/Correlation.pl -i {inputfile[0]} -exp1col {form.exp1.data} -exp2col {form.exp2.data} -name1 {form.name1.data} -name2 {form.name2.data} -genecol {form.gene.data} -method {form.method.data} -prefix {form.outpre.data} 2>>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()

        return redirect(url_for("admin.index"))
    return render_template('admin/tools/correlation.html', form=form)


@tools.route('/fisher.html', methods=["GET", "POST"])
@login_required
def fisher():
    form = FisherForm()
    if form.validate_on_submit():
        taskdir, uuid, inputfile = taskprepare("tools.fisher", form.url.data)

        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(
                f"Options: {form.n11.data} {form.n12.data} {form.n21.data} {form.n22.data} {form.method.data} {form.outpre.data}\n")
        script = f"perl ./app/static/program/fisher/Fisher.pl -i {inputfile[0]} -n11 {form.n11.data} -n12 {form.n12.data} -n21 {form.n21.data} -n22 {form.n22.data} -method {form.method.data} -prefix {form.outpre.data} 2>>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()

        return redirect(url_for("admin.index"))
    return render_template('admin/tools/fisher.html', form=form)


@tools.route('/cds2pep.html', methods=["GET", "POST"])
@login_required
def cds2pep():
    form = CDS2PEPForm()
    if form.validate_on_submit():
        taskdir, uuid, inputfile = taskprepare("tools.cds2pep", form.url.data)

        best = "-best" if form.best.data else ""
        stop = "-stop" if form.stop.data else ""
        N = "-n" if form.N.data else ""
        if form.method.data == "1":
            method = "-for"
        elif form.method.data == "-1":
            method = "-rev"
        else:
            method = ""
        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(
                f"Options: {best} {stop} {N} {method} {form.outpre.data}\n")
        script = f"perl ./app/static/program/cds2pep/CDS2Protein.pl -i {inputfile[0]} {best} {stop} {N} {method} -prefix {form.outpre.data} 2>>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()

        return redirect(url_for("admin.index"))
    return render_template('admin/tools/cds2pep.html', form=form)


@tools.route('/krona.html', methods=['GET', 'POST'])
@login_required
def krona():
    form = KronaForm()
    tool = Toolslist.query.filter_by(url="tools.krona").first()
    if form.validate_on_submit():
        taskdir, uuid, inputfile = taskprepare("tools.krona", form.url.data)

        with open(f"{taskdir}/run.log", "w", encoding='utf-8') as optfile:
            optfile.write(
                f"Options: {form.url.data} \n")
        script = ""
        if form.method.data == "0":
            script = f"perl ./app/static/program/krona/01.Krona/Krona.pl -i {inputfile[0]} -outdir {taskdir} -n root" \
                     f"  2>>{taskdir}/run.log"
        elif form.method.data == "1":
            script = f"perl ./app/static/program/krona/01.Krona/downsize_otu.biom -i {inputfile[0]} -type {biom} " \
                     f" -outdir {taskdir} -n root  2>>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()
        return redirect(url_for("admin.index"))
    return render_template('admin/tools/krona.html', form=form, tool=tool)


@tools.route('/bar.html', methods=['GET', 'POST'])
@login_required
def bar():
    form = BarForm()
    tool = Toolslist.query.filter_by(url="tools.bar").first()
    if form.validate_on_submit():
        taskdir, uuid, inputfile = taskprepare("tools.bar", form.url.data)

        with open(f"{taskdir}/run.log", "w", encoding='utf-8') as optfile:
            optfile.write(
                f"Options: {form.url.data} \n")
        script = f"perl ./app/static/program/bar/bar_plot.pl -i {inputfile[0]} -pre Family " \
                 f"  2>>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()
        return redirect(url_for("admin.index"))
    return render_template('admin/tools/bar.html', form=form, tool=tool)


@tools.route('/spearman.html', methods=['GET', 'POST'])
@login_required
def spearman():
    form = SpearmanForm()
    tool = Toolslist.query.filter_by(url="tools.spearman").first()
    if form.validate_on_submit():
        taskdir, uuid, inputfile = taskprepare("tools.spearman", form.url.data)

        with open(f"{taskdir}/run.log", "w", encoding='utf-8') as optfile:
            optfile.write(
                f"Options: {form.url.data} \n")
        script = f"perl ./app/static/program/spearman/spearman_plot.pl -i {inputfile[0]} -outdir {taskdir} -n root" \
                 f"  2>>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()
        return redirect(url_for("admin.index"))
    return render_template('admin/tools/spearman.html', form=form, tool=tool)


@tools.route('/lefse.html', methods=['GET', 'POST'])
@login_required
def lefse():
    form = SpearmanForm()
    if form.validate_on_submit():
        taskdir, uuid, inputfile = taskprepare("tools.lefse", form.url.data)

        with open(f"{taskdir}/run.log", "w", encoding='utf-8') as optfile:
            optfile.write(
                f"Options: {form.url.data} \n")
        script = f"perl ./app/static/program/lefse/lefse.pl -i {inputfile[0]} -outdir {taskdir} -n root" \
                 f"  2>>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()
        return redirect(url_for("admin.index"))
    return render_template('admin/tools/lefse.html', form=form)


@tools.route('/bar_tree.html', methods=['GET', 'POST'])
@login_required
def bar_tree():
    form = Bar_TreeForm()
    tool = Toolslist.query.filter_by(url="tools.bar_tree").first()
    if form.validate_on_submit():
        taskdir, uuid, fs = taskprepare("tools.bar_tree", form.fai1.data, form.fai2.data)
        f1, f2 = fs
        with open(f"{taskdir}/run.log", "w", encoding='utf-8') as optfile:
            optfile.write(
                f"Options: {f1}  {f2}\n")
        script = f"perl ./app/static/program/bar_tree/bar_tree.pl -i {taskdir}/{form.fai1.data.filename} -map {taskdir}/{form.fai2.data.filename} -pre genus " \
                 f"  2>>{taskdir}/run.log"
        print(script)
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()
        return redirect(url_for("admin.index"))
    return render_template('admin/tools/bar_tree.html', form=form, tool=tool)


@tools.route('/seqlogo.html', methods=['GET', 'POST'])
@login_required
def seqlogo():
    form = SeqlogoForm()
    tool = Toolslist.query.filter_by(url="tools.seqlogo").first()
    if form.validate_on_submit():
        taskdir, uuid, inputfile = taskprepare("tools.seqlogo", form.url.data)

        with open(f"{taskdir}/run.log", "w", encoding='utf-8') as optfile:
            optfile.write(
                f"Options: {form.url.data} {form.method.data} {form.color.data} {form.col.data} {form.h.data} {form.w.data}\n")
        script = f"python ./app/static/program/seqlogo/seqlogo.py {inputfile[0]} {form.method.data} {form.color.data} {form.col.data} {form.h.data} {form.w.data} 2>>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()
        return redirect(url_for("admin.index"))
    return render_template('admin/tools/seqlogo.html', form=form, tool=tool)


@tools.route('/convertp.html', methods=['GET', 'POST'])
@login_required
def convertp():
    form = ConvertPForm()
    tool = Toolslist.query.filter_by(url="tools.convertp").first()
    if form.validate_on_submit():
        taskdir, uuid, inputfile = taskprepare("tools.convertp", form.url.data)

        with open(f"{taskdir}/run.log", "w", encoding='utf-8') as optfile:
            optfile.write(
                f"Options: {form.url.data} {form.method.data} {form.density.data} \n")
        script = f"python ./app/static/program/convertp/convertpics.py {inputfile[0]} {form.method.data} {form.density.data} 2>>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()
        return redirect(url_for("admin.index"))
    return render_template('admin/tools/convertp.html', form=form, tool=tool)


@tools.route('/violin.html', methods=['GET', 'POST'])
@login_required
def violin():
    form = ViolinForm()
    tool = Toolslist.query.filter_by(url="tools.violin").first()
    if form.validate_on_submit():
        taskdir, uuid, inputfile = taskprepare("tools.violin", form.url.data)

        with open(f"{taskdir}/run.log", "w", encoding='utf-8') as optfile:
            optfile.write(
                f"Options: {form.url.data} {form.tcol.data} {form.dcol.data} {form.outpre.data}\n")
        script = f"perl ./app/static/program/violin/violin.pl -in {inputfile[0]} -tcol {form.tcol.data} -dcol {form.dcol.data} -out {form.outpre.data} 2>>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()
        return redirect(url_for("admin.index"))
    return render_template('admin/tools/violin.html', form=form, tool=tool)


@tools.route('/barbox.html', methods=["GET", "POST"])
@login_required
def barbox():
    form = BarboxForm()
    tool = Toolslist.query.filter_by(url="tools.barbox").first()
    if form.validate_on_submit():
        f1 = secure_filename(form.durl.data.filename)
        f2 = secure_filename(form.gurl.data.filename)
        uuid = uuid4().hex
        taskdir = f"./app/static/user/{current_user.name}/task/{uuid}"
        os.makedirs(taskdir + "/out")
        in1 = taskdir + "/" + f1
        form.durl.data.save(in1)
        in2 = ""
        if f2:
            in2 = taskdir + "/" + f2
            form.gurl.data.save(in2)
            if os.path.getsize(in2) > 10 * 1024 * 1024:
                shutil.rmtree(taskdir)
                abort(413)
        if os.path.getsize(in1) > 10 * 1024 * 1024:
            shutil.rmtree(taskdir)
            abort(413)

        task = Tasklist(
            title="箱线图",
            taskid=uuid,
            status="进行中",
            resulturl=taskdir,
            user_id=int(current_user.id)
        )
        db.session.add(task)
        db.session.commit()

        tool = Toolslist.query.filter_by(title="箱线图").first()
        tool.usenum += 1
        db.session.add(tool)
        db.session.commit()

        with open(f"{taskdir}/run.log", "w") as optfile:
            optfile.write(
                f"Options: {form.log.data} {form.dcol.data} {form.title.data} {form.xlab.data} {form.ylab.data} {form.outpre.data}\n")
        script = f"perl ./app/static/program/barbox/barbox.pl -in {in1} -group {in2} -dcol {form.dcol.data} -log {form.log.data} -title {form.title.data} -xlab {form.xlab.data} -ylab {form.ylab.data} -out {form.outpre.data} 2>>{taskdir}/run.log"
        app = current_app._get_current_object()
        crun = threading.Thread(target=runtools, args=(app, script, uuid))
        crun.start()

        return redirect(url_for("admin.index"))
    return render_template('admin/tools/barbox.html', form=form, tool=tool)
