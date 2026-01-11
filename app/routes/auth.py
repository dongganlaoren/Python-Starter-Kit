# /app/routes/auth.py
"""认证相关路由（注册/登录/注销）。

需求/约定：
- 认证基于 sk_user。
- 关键路由与数据库写入需 app.logger 记录。
- 表单校验：后端使用 WTForms。
"""

from __future__ import annotations

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from flask_babel import _

from app import db
from app.forms import LoginForm, RegisterForm
from app.models.sk_models import SkUser

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """用户注册。"""
    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        current_app.logger.info("Register attempt: %s", email)

        exists = SkUser.query.filter_by(email=email).first()
        if exists:
            current_app.logger.info("Register blocked, email exists: %s", email)
            # 更友好：直接标注到表单字段错误中，用户更容易定位
            form.email.errors.append(_("该邮箱已被注册，请直接登录或更换邮箱"))
            flash(_("邮箱已注册"), "warning")
            return render_template("auth/register.html", form=form)

        user = SkUser()
        user.email = email
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()
        current_app.logger.info("Register success: %s", email)

        # 注册成功后自动登录
        login_user(user)
        current_app.logger.info("Auto login after register: %s", email)

        flash(_("注册成功"), "success")
        return redirect(url_for("main.dashboard"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """用户登录。"""
    form = LoginForm()
    next_url = request.args.get("next")

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        current_app.logger.info("Login attempt: %s", email)

        user = SkUser.query.filter_by(email=email).first()
        if not user or not user.check_password(form.password.data):
            current_app.logger.info("Login failed: %s", email)
            flash(_("邮箱或密码错误"), "danger")
            return render_template("auth/login.html", form=form)

        login_user(user)
        current_app.logger.info("Login success: %s", email)

        return redirect(next_url or url_for("main.dashboard"))

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
def logout():
    """注销。"""
    current_app.logger.info("Logout")
    logout_user()
    flash(_("已退出登录"), "info")
    return redirect(url_for("auth.login"))
