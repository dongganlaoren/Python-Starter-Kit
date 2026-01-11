# /app/__init__.py
import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, request, session, render_template, redirect, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from flask_migrate import Migrate
from dotenv import load_dotenv
from babel import Locale

from app.config import get_config_class

# 预加载环境变量
load_dotenv()

# 初始化全局插件
db = SQLAlchemy()
babel = Babel()
login_manager = LoginManager()
migrate = Migrate()


def get_locale():
    """国际化语言选择器：默认 zh_CN，支持 en。

优先级：
1) URL 参数 ?lang=zh_CN/en
2) session['lang']
3) cookie['locale']（Flask-Babel 官方常用键名）
4) Accept-Language
"""

    lang = request.args.get("lang")
    if lang in ("zh_CN", "en"):
        session["lang"] = lang
        return Locale.parse(lang)

    lang = session.get("lang")
    if lang in ("zh_CN", "en"):
        return Locale.parse(lang)

    lang = request.cookies.get("locale") or request.cookies.get("lang")
    if lang in ("zh_CN", "en"):
        return Locale.parse(lang)

    best = request.accept_languages.best_match(["zh_CN", "en"]) or "zh_CN"
    return Locale.parse(best)


def create_app():
    app = Flask(__name__)

    # --- 1. 加载配置（支持开发/生产/测试切换） ---
    app.config.from_object(get_config_class())

    # 兼容旧配置：若未配置默认语言，则使用 zh_CN
    app.config.setdefault("BABEL_DEFAULT_LOCALE", "zh_CN")

    # 确保 Flask-Babel 能找到 translations 目录（项目根目录下的 translations/）
    app.config.setdefault(
        "BABEL_TRANSLATION_DIRECTORIES",
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "translations"),
    )

    # --- 2. 初始化插件 ---
    db.init_app(app)
    migrate.init_app(app, db)
    babel.init_app(app, locale_selector=get_locale)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "请先登录"
    login_manager.login_message_category = "warning"

    @login_manager.unauthorized_handler
    def unauthorized():
        # 统一处理未登录访问
        app.logger.info("Unauthorized access, redirect to login: %s", request.path)
        return redirect(url_for("auth.login", next=request.path))

    @login_manager.user_loader
    def load_user(user_id: str):
        """flask-login 用户加载器。"""
        from app.models.sk_models import SkUser

        try:
            return SkUser.query.get(int(user_id))
        except Exception:
            return None

    # --- 3. 配置日志系统 ---
    configure_logging(app)

    # --- 4. 注册蓝图 ---
    from app.routes import register_blueprints

    register_blueprints(app)

    # --- 5. 注册错误处理器 ---
    @app.errorhandler(404)
    def not_found(_e):
        app.logger.info("404 Not Found")
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(_e):
        app.logger.error("500 Internal Server Error")
        return render_template("errors/500.html"), 500


    return app


def configure_logging(app):
    """配置 app.logger 的输出格式和存储路径。"""
    if not os.path.exists("logs"):
        os.mkdir("logs")

    formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")

    file_handler = RotatingFileHandler(
        "logs/starterkit.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # 避免重复添加 handler（尤其是测试/热重载场景）
    if not any(isinstance(h, RotatingFileHandler) for h in app.logger.handlers):
        app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info("StarterKit Logging Initialized")