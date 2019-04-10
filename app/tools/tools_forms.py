# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import FileField, RadioField, SubmitField, SelectField, StringField, BooleanField
from wtforms.validators import Regexp
from app.admin.forms import Nonevalidators


class RevComForm(FlaskForm):
    url = FileField(
        label='fasta|txt',
        validators=[Nonevalidators("上传一个文件")],
        render_kw={"class": "custom-file-input", "id": "customFile"}
    )
    func = RadioField(
        label="run single function",
        # validators=[DataRequired("至少选择一项")], radio验证器无法使用
        choices=[('1', "反向"), ('2', "互补"), ('3', "反向互补")],
        render_kw={"class": "m-radio"}
    )
    submit = SubmitField("确认", render_kw={
        "class": "btn btn-primary"})


class PoolingForm(FlaskForm):
    url = FileField(
        label='excel',
        validators=[Nonevalidators("上传一个文件")],
        render_kw={"class": "custom-file-input", "id": "customFile"}
    )
    lane = SelectField(
        label="lane number",
        choices=[('1', "1"), ('2', "2"), ('3', "3"), ('4', "4")],
        render_kw={"class": "form-control m-input m-input--air"}
    )
    sizes = StringField(
        label="size",
        validators=[Nonevalidators("输入相应数目的片段大小"), Regexp(
            r"[\d,]+", message="必须是整数和英文逗号的组合")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "350[,350,300,500]", "aria-describedby": "basic-addon1"}
    )
    vol = StringField(
        label="volume",
        validators=[Nonevalidators("输入体积"), Regexp(
            r"[\d\.]+", message="必须是数字")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "体积", "aria-describedby": "basic-addon1"}
    )
    submit = SubmitField("确认", render_kw={
        "class": "btn btn-primary"})


class SplitLaneForm(FlaskForm):
    url = FileField(
        label='excel',
        validators=[Nonevalidators("上传一个文件")],
        render_kw={"class": "custom-file-input", "id": "customFile"}
    )
    lane = SelectField(
        label="lane number",
        choices=[('2', "2"), ('3', "3"), ('4', "4")],
        render_kw={"class": "form-control m-input m-input--air"}
    )
    submit = SubmitField("确认", render_kw={
        "class": "btn btn-primary"})


class DEGForm(FlaskForm):
    url = FileField(
        label='txt',
        validators=[Nonevalidators("上传一个文件")],
        render_kw={"class": "custom-file-input", "id": "customFile"}
    )
    pq = RadioField(
        label="p/fdr",
        choices=[('1', "pvalue"), ('2', "fdr")],
        render_kw={"class": "m-radio"}
    )
    pqcol = StringField(
        label="column",
        validators=[Nonevalidators("输入p值或fdr所在列"), Regexp(
            r"^\d+$", message="必须是正整数")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "6", "aria-describedby": "basic-addon1"}
    )
    yuzhi = StringField(
        label="阈值",
        validators=[Nonevalidators("输入阈值大小"), Regexp(
            r"[\d\.]+", message="必须是数字")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "0.05", "aria-describedby": "basic-addon1"}
    )
    fccol = StringField(
        label="column",
        validators=[Nonevalidators("输入fold change所在列"), Regexp(
            r"^\d+$", message="必须是正整数")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "5", "aria-describedby": "basic-addon1"}
    )
    fc = StringField(
        label="阈值",
        validators=[Nonevalidators("输入fold change阈值"), Regexp(
            r"[\d\.]+", message="必须是数字")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "1", "aria-describedby": "basic-addon1"}
    )
    outpre = StringField(
        label="out",
        validators=[Nonevalidators("输入输出结果前缀")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "A-VS-B", "aria-describedby": "basic-addon1"}
    )
    submit = SubmitField("确认", render_kw={
        "class": "btn btn-primary"})


class VolcanoForm(FlaskForm):
    url = FileField(
        label='txt',
        validators=[Nonevalidators("上传一个文件")],
        render_kw={"class": "custom-file-input", "id": "customFile"}
    )
    pqcol = StringField(
        label="column",
        validators=[Nonevalidators("输入p值或fdr所在列"), Regexp(
            r"^\d+$", message="必须是正整数")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "6", "aria-describedby": "basic-addon1"}
    )
    pq = StringField(
        label="阈值",
        validators=[Nonevalidators("输入阈值大小"), Regexp(
            r"[\d\.]+", message="必须是数字")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "0.05", "aria-describedby": "basic-addon1"}
    )
    fccol = StringField(
        label="column",
        validators=[Nonevalidators("输入fold change所在列"), Regexp(
            r"^\d+$", message="必须是正整数")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "5", "aria-describedby": "basic-addon1"}
    )
    fc = StringField(
        label="阈值",
        validators=[Nonevalidators("输入fold change阈值"), Regexp(
            r"[\d\.]+", message="必须是数字")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "1", "aria-describedby": "basic-addon1"}
    )
    outpre = StringField(
        label="out",
        validators=[Nonevalidators("输入输出结果前缀")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "A-VS-B", "aria-describedby": "basic-addon1"}
    )
    submit = SubmitField("确认", render_kw={
        "class": "btn btn-primary"})


class MAplotForm(FlaskForm):
    url = FileField(
        label='txt',
        validators=[Nonevalidators("上传一个文件")],
        render_kw={"class": "custom-file-input", "id": "customFile"}
    )
    pqcol = StringField(
        label="column",
        validators=[Nonevalidators("输入p值或fdr所在列"), Regexp(
            r"^\d+$", message="必须是正整数")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "6", "aria-describedby": "basic-addon1"}
    )
    pq = StringField(
        label="阈值",
        validators=[Nonevalidators("输入阈值大小"), Regexp(
            r"[\d\.]+", message="必须是数字")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "0.05", "aria-describedby": "basic-addon1"}
    )
    fccol = StringField(
        label="column",
        validators=[Nonevalidators("输入fold change所在列"), Regexp(
            r"^\d+$", message="必须是正整数")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "5", "aria-describedby": "basic-addon1"}
    )
    fc = StringField(
        label="阈值",
        validators=[Nonevalidators("输入fold change阈值"), Regexp(
            r"[\d\.]+", message="必须是数字")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "1", "aria-describedby": "basic-addon1"}
    )
    exp1 = StringField(
        label="阈值",
        validators=[Nonevalidators("输入样本组1所在列"), Regexp(
            r"[\d-]+", message="必须是正整数和-的组合")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "3[3-5]", "aria-describedby": "basic-addon1"}
    )
    exp2 = StringField(
        label="阈值",
        validators=[Nonevalidators("输入样本组2所在列"), Regexp(
            r"[\d-]+", message="必须是正整数和-的组合")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "6[6-8]", "aria-describedby": "basic-addon1"}
    )
    outpre = StringField(
        label="out",
        validators=[Nonevalidators("输入输出结果前缀")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "A-VS-B", "aria-describedby": "basic-addon1"}
    )
    submit = SubmitField("确认", render_kw={
        "class": "btn btn-primary"})


class EZCLForm(FlaskForm):
    fai1 = FileField(
        label='txt',
        validators=[Nonevalidators("上传一个文件")],
        render_kw={"class": "custom-file-input", "id": "customFile"}
    )
    fai2 = FileField(
        label='txt',
        validators=[Nonevalidators("上传一个文件")],
        render_kw={"class": "custom-file-input", "id": "customFile"}
    )
    links = FileField(
        label='txt',
        validators=[Nonevalidators("上传一个文件，必须有6列")],
        render_kw={"class": "custom-file-input", "id": "customFile"}
    )
    name = StringField(
        label="column",
        validators=[Nonevalidators("输入A和B显示名称"), Regexp(
            r"[,a-zA-Z0-9]+", message="必须是字母、数字和逗号（英文）的组合")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "AAA,BBB", "aria-describedby": "basic-addon1"}
    )
    opacity = StringField(
        label="透明度",
        validators=[Nonevalidators("输入透明度"), Regexp(
            r"^[\.0-9]+$", message="必须是数字和点的组合")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "0.2", "aria-describedby": "basic-addon1"}
    )
    outpre = StringField(
        label="out",
        validators=[Nonevalidators("输入输出结果前缀")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "A-VS-B", "aria-describedby": "basic-addon1"}
    )
    submit = SubmitField("确认", render_kw={
        "class": "btn btn-primary"})


class VennForm(FlaskForm):
    files = FileField(
        label='txt',
        validators=[Nonevalidators("上传2~5个文件")],
        render_kw={"class": "custom-file-input",
                   "id": "customFile", "multiple": ""}
    )
    head = RadioField(
        label="head",
        choices=[('T', "有"), ('F', "无")],
        render_kw={"class": "m-radio"}
    )
    col = StringField(
        label="column",
        validators=[Nonevalidators("选择一列进行绘图"), Regexp(
            r"^[0-9]+$", message="必须是正整数")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "1", "aria-describedby": "basic-addon1"}
    )
    submit = SubmitField("确认", render_kw={
        "class": "btn btn-primary"})


class EdgeRForm(FlaskForm):
    url = FileField(
        label='txt',
        validators=[Nonevalidators("上传一个文件")],
        render_kw={"class": "custom-file-input", "id": "customFile"}
    )
    exp1 = StringField(
        label="阈值",
        validators=[Nonevalidators("输入样本组1所在列"), Regexp(
            r"[\d-]+", message="必须是正整数和-的组合")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "3[3-5]", "aria-describedby": "basic-addon1"}
    )
    exp2 = StringField(
        label="阈值",
        validators=[Nonevalidators("输入样本组2所在列"), Regexp(
            r"[\d-]+", message="必须是正整数和-的组合")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "6[6-8]", "aria-describedby": "basic-addon1"}
    )
    bcv = StringField(
        label="column",
        validators=[Nonevalidators("输入bcv值"), Regexp(
            r"^[\.0-9]+$", message="必须是小数")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "0.3", "aria-describedby": "basic-addon1"}
    )
    gene = StringField(
        label="column",
        validators=[Nonevalidators("输入gene名称所在列"), Regexp(
            r"^\d+$", message="必须是正整数")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "1", "aria-describedby": "basic-addon1"}
    )
    outpre = StringField(
        label="out",
        validators=[Nonevalidators("输入输出结果前缀")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "A-VS-B", "aria-describedby": "basic-addon1"}
    )
    submit = SubmitField("确认", render_kw={
        "class": "btn btn-primary"})


class DESeq2Form(FlaskForm):
    url = FileField(
        label='txt',
        validators=[Nonevalidators("上传一个文件")],
        render_kw={"class": "custom-file-input", "id": "customFile"}
    )
    exp1 = StringField(
        label="阈值",
        validators=[Nonevalidators("输入样本组1所在列"), Regexp(
            r"\d+-\d+", message="必须是正整数和-的组合，必须有重复样本")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "3-5", "aria-describedby": "basic-addon1"}
    )
    exp2 = StringField(
        label="阈值",
        validators=[Nonevalidators("输入样本组2所在列"), Regexp(
            r"\d+-\d+", message="必须是正整数和-的组合，必须有重复样本")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "6-8", "aria-describedby": "basic-addon1"}
    )
    gene = StringField(
        label="column",
        validators=[Nonevalidators("输入gene名称所在列"), Regexp(
            r"^\d+$", message="必须是正整数")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "1", "aria-describedby": "basic-addon1"}
    )
    outpre = StringField(
        label="out",
        validators=[Nonevalidators("输入输出结果前缀")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "A-VS-B", "aria-describedby": "basic-addon1"}
    )
    submit = SubmitField("确认", render_kw={
        "class": "btn btn-primary"})


class KEGGbublleForm(FlaskForm):
    url = FileField(
        label='txt',
        validators=[Nonevalidators("上传一个文件")],
        render_kw={"class": "custom-file-input", "id": "customFile"}
    )
    pathcol = StringField(
        label="输入pathway所在列",
        validators=[Nonevalidators("输入pathway所在列"), Regexp(
            r"^\d+$", message="必须是正整数")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "3", "aria-describedby": "basic-addon1"}
    )
    genecol = StringField(
        label="输入富集基因数目所在列",
        validators=[Nonevalidators("输入富集基因数目所在列"), Regexp(
            r"^\d+$", message="必须是正整数")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "4", "aria-describedby": "basic-addon1"}
    )
    bgcol = StringField(
        label="输入背景基因基所在列",
        validators=[Nonevalidators("输入背景基因基所在列"), Regexp(
            r"^\d+$", message="必须是正整数")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "5", "aria-describedby": "basic-addon1"}
    )
    pqcol = StringField(
        label="输入p值或fdr所在列",
        validators=[Nonevalidators("输入p值或fdr所在列"), Regexp(
            r"^\d+$", message="必须是正整数")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "6", "aria-describedby": "basic-addon1"}
    )
    outpre = StringField(
        label="输入输出结果前缀",
        validators=[Nonevalidators("输入输出结果前缀")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "A-VS-B", "aria-describedby": "basic-addon1"}
    )
    submit = SubmitField("确认", render_kw={
        "class": "btn btn-primary"})


class PCAForm(FlaskForm):
    url = FileField(
        label='txt',
        validators=[Nonevalidators("上传一个文件")],
        render_kw={"class": "custom-file-input", "id": "customFile"}
    )
    expcol = StringField(
        label="输入数据所在列",
        validators=[Nonevalidators("输入数据所在列"), Regexp(
            r"^\d+-\d+$", message="必须是正整数和-的组合")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "3-8", "aria-describedby": "basic-addon1"}
    )
    genecol = StringField(
        label="输入基因名称所在列",
        validators=[Nonevalidators("输入基因名称所在列"), Regexp(
            r"^\d+$", message="必须是正整数")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "1", "aria-describedby": "basic-addon1"}
    )
    outpre = StringField(
        label="输入输出结果前缀",
        validators=[Nonevalidators("输入输出结果前缀")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "A-VS-B", "aria-describedby": "basic-addon1"}
    )
    submit = SubmitField("确认", render_kw={
        "class": "btn btn-primary"})


class ClusterTreeForm(FlaskForm):
    url = FileField(
        label='txt',
        validators=[Nonevalidators("上传一个文件")],
        render_kw={"class": "custom-file-input", "id": "customFile"}
    )
    expcol = StringField(
        label="输入数据所在列",
        validators=[Nonevalidators("输入表达量所在列"), Regexp(
            r"^\d+-\d+$", message="必须是正整数和-的组合")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "3-8", "aria-describedby": "basic-addon1"}
    )
    method = SelectField(
        label="选择聚类所用方法",
        choices=[('complete', "complete"), ('average', "average"), ('median', "median"), ('centroid', "centroid")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "", "aria-describedby": "basic-addon1"}
    )
    outpre = StringField(
        label="输入输出结果前缀",
        validators=[Nonevalidators("输入输出结果前缀")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "A-VS-B", "aria-describedby": "basic-addon1"}
    )
    submit = SubmitField("确认", render_kw={
        "class": "btn btn-primary"})


class HeatMapForm(FlaskForm):
    url = FileField(
        label='txt',
        validators=[Nonevalidators("上传一个文件")],
        render_kw={"class": "custom-file-input", "id": "customFile"}
    )
    namecol = StringField(
        label="输入行名所在列",
        validators=[Nonevalidators("输入行名所在列"), Regexp(
            r"^\d+$", message="必须是正整数")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "1", "aria-describedby": "basic-addon1"}
    )
    datacol = StringField(
        label="输入数据所在列",
        validators=[Nonevalidators("输入数据所在列"), Regexp(
            r"^[\d\-,]+$", message="必须是正整数、逗号和-的组合")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "2-7[2,5-7]", "aria-describedby": "basic-addon1"}
    )
    width = StringField(
        label="输入输出图像宽度",
        validators=[Nonevalidators("输入数据所在列"), Regexp(
            r"^\d+$", message="必须是正整数")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "6", "aria-describedby": "basic-addon1"}
    )
    height = StringField(
        label="输入输出图像高度",
        validators=[Nonevalidators("输入数据所在列"), Regexp(
            r"^\d+$", message="必须是正整数")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "8", "aria-describedby": "basic-addon1"}
    )
    scale = SelectField(
        label="选择均一化方法",
        choices=[('row', "行"), ('column', "列"), ('none', "都不做")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "", "aria-describedby": "basic-addon1"}
    )
    cluster_rows = SelectField(
        label="选择是否行聚类",
        choices=[('TRUE', "是"), ('FALSE', "否")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "", "aria-describedby": "basic-addon1"}
    )
    cluster_cols = SelectField(
        label="选择是否列聚类",
        choices=[('TRUE', "是"), ('FALSE', "否")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "", "aria-describedby": "basic-addon1"}
    )
    show_rownames = SelectField(
        label="选择是否显示行名",
        choices=[('TRUE', "是"), ('FALSE', "否")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "", "aria-describedby": "basic-addon1"}
    )
    show_colnames = SelectField(
        label="选择是否显示列名",
        choices=[('TRUE', "是"), ('FALSE', "否")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "", "aria-describedby": "basic-addon1"}
    )
    display_numbers = SelectField(
        label="选择是否显示数字",
        choices=[('TRUE', "是"), ('FALSE', "否")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "", "aria-describedby": "basic-addon1"}
    )
    outpre = StringField(
        label="输入输出结果前缀",
        validators=[Nonevalidators("输入输出结果前缀")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "A-VS-B", "aria-describedby": "basic-addon1"}
    )
    submit = SubmitField("确认", render_kw={
        "class": "btn btn-primary"})


class CorrForm(FlaskForm):
    url = FileField(
        label='txt',
        validators=[Nonevalidators("上传一个文件")],
        render_kw={"class": "custom-file-input", "id": "customFile"}
    )
    exp1 = StringField(
        label="输入A单样本或样本组所在列",
        validators=[Nonevalidators("输入样本组1所在列"), Regexp(
            r"[\d\-]+", message="必须是正整数或-的组合")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "2[3-5]", "aria-describedby": "basic-addon1"}
    )
    name1 = StringField(
        label="输入A单样本或样本组名称",
        validators=[Nonevalidators("输入A单样本或样本组名称"), Regexp(
            r"\w+", message="必须是字母加数字的组合")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "A[A1,A2,A3]", "aria-describedby": "basic-addon1"}
    )
    exp2 = StringField(
        label="输入B单样本或样本组所在列",
        validators=[Nonevalidators("输入样本组2所在列"), Regexp(
            r"[\d\-]+", message="必须是正整数或-的组合")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "6[7-9]", "aria-describedby": "basic-addon1"}
    )
    name2 = StringField(
        label="输入B单样本或样本组名称",
        validators=[Nonevalidators("输入B单样本或样本组名称"), Regexp(
            r"\w+", message="必须是字母加数字的组合")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "B[B1,B2,B3]", "aria-describedby": "basic-addon1"}
    )
    gene = StringField(
        label="输入gene名称所在列",
        validators=[Nonevalidators("输入gene名称所在列"), Regexp(
            r"^\d+$", message="必须是正整数")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "1", "aria-describedby": "basic-addon1"}
    )
    method = SelectField(
        label="选择相关性方法",
        choices=[('pearson', "pearson"), ('spearman', "spearman")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "", "aria-describedby": "basic-addon1"}
    )
    outpre = StringField(
        label="输入输出结果前缀",
        validators=[Nonevalidators("输入输出结果前缀")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "A-VS-B", "aria-describedby": "basic-addon1"}
    )
    submit = SubmitField("确认", render_kw={
        "class": "btn btn-primary"})


class FisherForm(FlaskForm):
    url = FileField(
        label='txt',
        validators=[Nonevalidators("上传一个文件")],
        render_kw={"class": "custom-file-input", "id": "customFile"}
    )
    n11 = StringField(
        label="输入n11所在列",
        validators=[Nonevalidators("输入n11所在列"), Regexp(
            r"^\d+$", message="必须是正整数")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "2", "aria-describedby": "basic-addon1"}
    )
    n12 = StringField(
        label="输入n12所在列",
        validators=[Nonevalidators("输入n12所在列"), Regexp(
            r"^\d+$", message="必须是正整数")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "3", "aria-describedby": "basic-addon1"}
    )
    n21 = StringField(
        label="输入n21所在列",
        validators=[Nonevalidators("输入n21所在列"), Regexp(
            r"^\d+$", message="必须是正整数")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "4", "aria-describedby": "basic-addon1"}
    )
    n22 = StringField(
        label="输入n22所在列",
        validators=[Nonevalidators("输入n22所在列"), Regexp(
            r"^\d+$", message="必须是正整数")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "5", "aria-describedby": "basic-addon1"}
    )
    method = SelectField(
        label="选择检验方法",
        choices=[('twotailed', "twotailed"), ('left', "left"), ('right', "right")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "", "aria-describedby": "basic-addon1"}
    )
    outpre = StringField(
        label="输入输出结果前缀",
        validators=[Nonevalidators("输入输出结果前缀")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "A-VS-B", "aria-describedby": "basic-addon1"}
    )
    submit = SubmitField("确认", render_kw={
        "class": "btn btn-primary"})


class CDS2PEPForm(FlaskForm):
    url = FileField(
        label='txt',
        validators=[Nonevalidators("上传一个文件")],
        render_kw={"class": "custom-file-input", "id": "customFile"}
    )
    best = BooleanField(
        label="选择最长的序列输出"
    )
    stop = BooleanField(
        label="出现终止密码子是否终止",
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "", "aria-describedby": "basic-addon1"}
    )
    N = BooleanField(
        label="出现N碱基是否终止",
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "", "aria-describedby": "basic-addon1"}
    )
    method = SelectField(
        label="选择方向翻译",
        choices=[('1', "正向"), ('-1', "反向"), ('0', "双向")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "", "aria-describedby": "basic-addon1"}
    )
    outpre = StringField(
        label="输入输出结果前缀",
        validators=[Nonevalidators("输入输出结果前缀")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "A-VS-B", "aria-describedby": "basic-addon1"}
    )
    submit = SubmitField("确认", render_kw={
        "class": "btn btn-primary"})


class KronaForm(FlaskForm):
    url = FileField(
        label='txt',
        validators=[Nonevalidators("上传一个文件")],
        render_kw={"class": "custom-file-input", "id": "otu_table"}
    )
    method = SelectField(
        label="选择文件类型",
        choices=[('1', "biom"), ('0', "text")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "", "aria-describedby": "basic-addon1"}
    )

    submit = SubmitField("确认", render_kw={
        "class": "btn btn-primary"})


class BarForm(FlaskForm):
    url = FileField(
        label='txt',
        validators=[Nonevalidators("上传一个文件")],
        render_kw={"class": "custom-file-input", "id": "bar_table"}
    )

    submit = SubmitField("确认", render_kw={
        "class": "btn btn-primary"})


class SpearmanForm(FlaskForm):
    url = FileField(
        label='txt',
        validators=[Nonevalidators("上传一个文件")],
        render_kw={"class": "custom-file-input", "id": "spearman_table"}
    )

    submit = SubmitField("确认", render_kw={
        "class": "btn btn-primary"})


class Bar_TreeForm(FlaskForm):
    url = FileField(
        label='txt',
        validators=[Nonevalidators("上传一个文件")],
        render_kw={"class": "custom-file-input", "id": "bar_tree_table"}
    )

    submit = SubmitField("确认", render_kw={
        "class": "btn btn-primary"})
