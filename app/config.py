# /app/config.py
"""应用配置模块。

目标：
- 支持开发/生产环境切换。
- 所有敏感配置从环境变量读取（配合 python-dotenv 在本地加载 .env）。

约定：
- 优先使用 APP_ENV 作为环境标识：development / production / testing。
- 兼容 FLASK_DEBUG：FLASK_DEBUG=1 视作 development。
"""

from __future__ import annotations

import os


class BaseConfig:
    """基础配置（开发/生产通用）。"""

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///starterkit.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cookie 基础安全配置
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Babel / i18n
    # 默认简体中文，可通过环境变量覆盖
    BABEL_DEFAULT_LOCALE = os.getenv("BABEL_DEFAULT_LOCALE", "zh_CN")


class DevelopmentConfig(BaseConfig):
    """开发环境配置。"""

    DEBUG = True


class ProductionConfig(BaseConfig):
    """生产环境配置。"""

    DEBUG = False
    TESTING = False

    # 生产环境默认固定 zh_CN（也可通过 env 覆盖）
    BABEL_DEFAULT_LOCALE = os.getenv("BABEL_DEFAULT_LOCALE", "zh_CN")


class TestingConfig(BaseConfig):
    """测试环境配置。

注意：
- 为降低误操作风险，测试环境强制使用 sqlite，而不是读取 .env 里的 MySQL。
"""

    TESTING = True
    WTF_CSRF_ENABLED = False

    # 默认使用项目工作目录下的 test.db（pytest 通常在项目根目录执行）
    # 可通过 TEST_DATABASE_URL 覆盖
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL", "sqlite:///test.db")
    BABEL_DEFAULT_LOCALE = os.getenv("BABEL_DEFAULT_LOCALE", "zh_CN")


def get_config_class():
    """根据环境变量决定加载哪个 config class。"""

    # 1) 明确使用 APP_ENV
    app_env = (os.getenv("APP_ENV") or "").strip().lower()

    # 2) 兼容 FLASK_DEBUG：只要显式为 1/true，就认为是开发
    flask_debug = (os.getenv("FLASK_DEBUG") or "").strip().lower() in ("1", "true", "yes")

    if app_env in ("prod", "production"):
        return ProductionConfig

    if app_env in ("test", "testing"):
        return TestingConfig

    if flask_debug:
        return DevelopmentConfig

    # 默认开发
    return DevelopmentConfig
