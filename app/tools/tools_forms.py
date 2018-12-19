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
        validators=[Nonevalidators("输入相应数目的片段大小"), Regexp(r"[\d,]+", message="必须是整数和英文逗号的组合")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "350[,350,300,500]", "aria-describedby": "basic-addon1"}
    )
    vol = StringField(
        label="volume",
        validators=[Nonevalidators("输入体积"), Regexp(r"[\d\.]+", message="必须是数字")],
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
        validators=[Nonevalidators("输入p值或fdr所在列"), Regexp(r"^\d+$", message="必须是正整数")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "6", "aria-describedby": "basic-addon1"}
    )
    yuzhi = StringField(
        label="阈值",
        validators=[Nonevalidators("输入阈值大小"), Regexp(r"[\d.]+", message="必须是数字")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "0.05", "aria-describedby": "basic-addon1"}
    )
    fccol = StringField(
        label="column",
        validators=[Nonevalidators("输入fold change所在列"), Regexp(r"^\d+$", message="必须是正整数")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "5", "aria-describedby": "basic-addon1"}
    )
    fc = StringField(
        label="阈值",
        validators=[Nonevalidators("输入fold change阈值"), Regexp(r"[\d\.]+", message="必须是数字")],
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
