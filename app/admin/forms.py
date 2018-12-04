# coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired

from app.models import User


class LoginForm(FlaskForm):
    email = StringField(
        label='账号',
        validators=[
            DataRequired('请输入账号')
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
            DataRequired('请输入密码')
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
