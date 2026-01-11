# /app/models/sk_models.py
"""StarterKit 框架自带基础模型。

需求/约定：
- 框架基础表名必须以 sk_ 开头。
- 第二阶段需提供 SkUser 基础用户模型。
- 认证使用 flask-login。
"""

from __future__ import annotations

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models.base import BaseModel


class SkUser(UserMixin, BaseModel):
    """框架基础用户表（sk_user）。"""

    __tablename__ = "sk_user"

    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, email: str | None = None, **kwargs):
        super().__init__(**kwargs)
        if email is not None:
            self.email = email

    def set_password(self, password: str) -> None:
        """设置密码（保存哈希）。"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """校验密码。"""
        return check_password_hash(self.password_hash, password)
