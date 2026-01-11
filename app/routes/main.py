# /app/routes/main.py
"""主业务路由（Dashboard 等）。

需求/约定：
- 提供 Dashboard 页面（登录后可访问）。
- 提供健康检查路由，便于测试/部署探活。
- 关键入口记录 app.logger。
"""

from __future__ import annotations

from flask import Blueprint, current_app, jsonify, redirect, render_template, url_for
from flask_login import current_user, login_required

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """首页：根据登录状态跳转到 dashboard 或 login。"""
    current_app.logger.info("Index accessed")
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("auth.login"))


@main_bp.route("/dashboard")
@login_required
def dashboard():
    """仪表盘。"""
    current_app.logger.info("Dashboard accessed")
    return render_template("dashboard.html")


@main_bp.route("/health")
def health():
    """健康检查。"""
    return jsonify({"status": "ok"})


@main_bp.route("/users")
@login_required
def users_index():
    """用户管理页面（占位）。"""
    current_app.logger.info("Users management accessed")
    return render_template("users/index.html")

