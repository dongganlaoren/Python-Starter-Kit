# /app/routes/__init__.py
"""路由（Blueprint）包。

约定：
- 在 create_app 中统一调用 register_blueprints(app)。
- 具体业务蓝图放在本包下的独立模块文件中。
"""

from flask import Flask


def register_blueprints(app: Flask) -> None:
    """注册所有 Blueprint。"""
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.i18n import i18n_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(i18n_bp)
