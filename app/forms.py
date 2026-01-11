# /app/forms.py
"""表单层（Flask-WTF + WTForms）。

需求/约定：
- 前后端均需校验；后端使用 WTForms 做基础约束。
- 代码与注释中文优先。
"""

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp


class RegisterForm(FlaskForm):
    """用户注册表单。"""

    email = StringField(
        "邮箱",
        validators=[DataRequired(message="邮箱不能为空"), Email(message="邮箱格式不正确")],
    )
    password = PasswordField(
        "密码",
        validators=[
            DataRequired(message="密码不能为空"),
            Length(min=8, message="密码至少 8 位"),
            Regexp(r"^(?=.*[A-Za-z])(?=.*\d).+$", message="密码需包含字母和数字"),
        ],
    )
    password2 = PasswordField(
        "确认密码",
        validators=[
            DataRequired(message="确认密码不能为空"),
            EqualTo("password", message="两次密码不一致"),
        ],
    )


class LoginForm(FlaskForm):
    """用户登录表单。"""

    email = StringField(
        "邮箱",
        validators=[DataRequired(message="邮箱不能为空"), Email(message="邮箱格式不正确")],
    )
    password = PasswordField(
        "密码",
        validators=[DataRequired(message="密码不能为空")],
    )
