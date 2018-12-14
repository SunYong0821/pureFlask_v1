# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import FileField, RadioField, SubmitField, SelectField, StringField
from wtforms.validators import DataRequired

from app.admin.forms import Nonevalidators


class RevComForm(FlaskForm):
    url = FileField(
        label='fasta|txt',
        validators=[Nonevalidators("请上传一个文件")],
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
        validators=[Nonevalidators("请上传一个文件")],
        render_kw={"class": "custom-file-input", "id": "customFile"}
    )
    lane = SelectField(
        label="lane number",
        choices=[('1', "1"), ('2', "2"), ('3', "3"), ('4', "4")],
        render_kw={"class": "form-control m-input m-input--air"}
    )
    sizes = StringField(
        label="size",
        validators=[Nonevalidators("请输入相应数目的片段大小")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "350[,350,300,500]"}
    )
    vol = StringField(
        label="volume",
        validators=[Nonevalidators("请输入体积")],
        render_kw={"class": "form-control m-input m-input--air",
                   "placeholder": "体积", "aria-describedby": "basic-addon1"}
    )
    submit = SubmitField("确认", render_kw={
        "class": "btn btn-primary"})

class SplitLaneForm(FlaskForm):
    url = FileField(
        label='excel',
        validators=[Nonevalidators("请上传一个文件")],
        render_kw={"class": "custom-file-input", "id": "customFile"}
    )
    lane = SelectField(
        label="lane number",
        choices=[('2', "2"), ('3', "3"), ('4', "4")],
        render_kw={"class": "form-control m-input m-input--air"}
    )
    submit = SubmitField("确认", render_kw={
        "class": "btn btn-primary"})
