# /tests/conftest.py
"""pytest 全局夹具。

注意：
- 本项目使用 Flask 工厂模式 create_app，因此测试里应通过创建 app 实例来隔离环境。
- 测试默认使用 sqlite 临时文件数据库，不依赖 MySQL。
"""

import os
import sys
from pathlib import Path

import pytest

# 确保项目根目录在导入路径中（避免 pytest 工作目录变化导致无法 import app）
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app, db


@pytest.fixture()
def app(tmp_path):
    """创建一个测试用 Flask app（强制 sqlite 临时文件数据库）。"""

    db_path = tmp_path / "test.db"

    os.environ.setdefault("SECRET_KEY", "test-secret")
    os.environ["APP_ENV"] = "testing"
    os.environ["TEST_DATABASE_URL"] = f"sqlite:///{db_path}"

    app = create_app()
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,  # 测试中关闭 CSRF
    )

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    """Flask 测试客户端。"""
    return app.test_client()
