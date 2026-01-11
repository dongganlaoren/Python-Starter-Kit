# /app/routes/i18n.py
"""国际化（i18n）相关路由。

目的：
- 提供一个专用的语言切换入口，避免仅使用 ?lang= 在复杂查询参数/POST 场景下丢参数。
- 切换后尽量回到用户之前的页面。

约定：
- 支持 zh_CN / en。
"""

from __future__ import annotations

from flask import Blueprint, current_app, redirect, request, session, url_for


i18n_bp = Blueprint("i18n", __name__, url_prefix="/i18n")


@i18n_bp.route("/set/<lang>")
def set_language(lang: str):
    """设置语言并返回上一页。"""

    if lang not in ("zh_CN", "en"):
        current_app.logger.info("Invalid lang: %s", lang)
        return redirect(request.referrer or url_for("main.index"))

    session["lang"] = lang
    current_app.logger.info("Language set: %s", lang)

    # 兼容：同时写入 session 与 cookie（locale 为常用键名）
    resp = redirect(request.referrer or url_for("main.index"))
    resp.set_cookie("locale", lang, max_age=60 * 60 * 24 * 365, samesite="Lax", path="/")
    resp.set_cookie("lang", lang, max_age=60 * 60 * 24 * 365, samesite="Lax", path="/")
    return resp
