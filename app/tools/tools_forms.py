# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import FileField, RadioField, SubmitField, SelectField, StringField
from wtforms.validators import DataRequired, Regexp
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
        label="输入表达量所在列",
        validators=[Nonevalidators("输入表达量所在列"), Regexp(
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
