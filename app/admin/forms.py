# coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired

from app.models import User


class Nonevalidators(object):

    def __init__(self, message):
        self.message = message

    def __call__(self, form, field):
        if field.data == "":
            raise validators.StopValidation(self.message)  # StopValidation 不再继续后面的验证  ValidationError 继续后面的验证
        return None


class LoginForm(FlaskForm):
    email = StringField(
        label='账号',
        validators=[
            Nonevalidators('请输入账号')
        ],
        description='账号',
        render_kw={
            'class': 'form-control m-input',
            'placeholder': '请输入账号',

        }
    )
    pwd = PasswordField(
        label='密码',
        validators=[
            Nonevalidators('请输入密码')
        ],
        description='密码',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入密码',

        }
    )
    submit = SubmitField(
        '登陆',
        render_kw={
            'class': 'btn btn-primary btn-block btn-flat'
        }
    )

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise validators.StopValidation("邮箱已被注册")
