# coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired, Length, EqualTo, Regexp

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
            Nonevalidators('请输入邮箱'),
            Length(2, 30, message=u'电子邮箱不符合规范')

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
            Nonevalidators('请输入密码'),
            Length(6, 32, message="密码长度在6-32位")
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
            'class': 'btn btn-focus m-btn m-btn--pill m-btn--custom m-btn--air'
        }
    )


class RegisterForm(FlaskForm):
    name = StringField(label=u"用户名",
                       validators=[
                           Nonevalidators(message="请输入用户名"),
                           Length(2, 10,
                                  message=u"用户名至少需要两个字符,最多10个字符")],
                       render_kw={
                           "class": "form-control m-input",
                           "placeholder": u"用户名",
                       })
    email = StringField(label="邮箱",
                        validators=[
                            Nonevalidators(message="请输入邮箱"),
                            Regexp(r"\w+@microanaly\.com", message="电子邮箱不符合规范")
                        ],
                        description="账号",
                        render_kw={
                            "class": "form-control m-input",
                            "placeholder": "邮箱"

                        })
    pwd = PasswordField(label="密码",
                        validators=[
                            Nonevalidators(message="请输入密码"),
                            Length(6, 32, message="密码长度在6-32位")],
                        description="密码",
                        render_kw={
                            "class": "form-control m-input",
                            "placeholder": "密码"
                        })
    rpwd = PasswordField(label="密码",
                         validators=[
                             EqualTo('pwd', message="两次输入密码不一致")],
                         description="密码",
                         render_kw={
                             "class": "form-control m-input",
                             "placeholder": "确认密码"
                         })
    submit = SubmitField("注册", render_kw={
        "class": "btn btn-focus m-btn m-btn--pill m-btn--custom m-btn--air",
    })

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise validators.StopValidation("邮箱已被注册")
    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first():
            raise validators.StopValidation("用户名已被注册")


class ForgetPasswordRequestForm(FlaskForm):
    email = StringField(label="邮箱",
                        validators=[
                            Nonevalidators(message="请输入邮箱"),
                            Length(4, 24, message="电子邮箱不符合规范"),
                        ],
                        description="账号",
                        render_kw={
                            "class": "form-control m-input",
                            "placeholder": "邮箱"

                        })
    submit = SubmitField("重置", render_kw={
        "class": "btn btn-focus m-btn m-btn--pill m-btn--custom m-btn--air",
    })


class ForgetPasswordForm(FlaskForm):
    pwd = PasswordField(label="密码",
                        validators=[
                            Nonevalidators(message="请输入密码"),
                            Length(6, 32, message="密码长度在6-32位")],
                        description="密码",
                        render_kw={
                            "class": "form-control m-input",
                            "placeholder": "密码"
                        })
    rpwd = PasswordField(label="密码",
                         validators=[
                             EqualTo('pwd', message="两次输入密码不一致")],
                         description="密码",
                         render_kw={
                             "class": "form-control m-input",
                             "placeholder": "确认密码"
                         })
    submit = SubmitField("注册", render_kw={
        "class": "btn btn-focus m-btn m-btn--pill m-btn--custom m-btn--air",
    })
