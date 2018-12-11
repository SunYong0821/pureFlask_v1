# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import FileField, RadioField, SubmitField

from app.admin.forms import Nonevalidators


class RevComForm(FlaskForm):
    url = FileField(
        label='fasta|txt',
        validators=[Nonevalidators("请上传一个文件")],
        render_kw={"class": "file"}
    )
    func = RadioField(
        label="run single function",
        validators=[Nonevalidators("至少选择一项")],
        choices=[('1', "反向"), ('2', "互补"), ('3', "反向互补")],
        render_kw={"name": "example_1", "class": "m-radio"}
    )
    submit = SubmitField("确认", render_kw={
        "class": "btn btn-primary"})
