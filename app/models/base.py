# /app/models/base.py
"""模型层基础抽象。

需求/约定：
- BaseModel 需包含自动时间戳（created_at/updated_at）。
- 使用 Flask-SQLAlchemy 的 db.Model。
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func

from app import db


class BaseModel(db.Model):
    """所有 ORM 模型的抽象基类。"""

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self) -> dict:
        """将模型转换为可序列化 dict（简单实现，可按需扩展）。"""
        result = {}
        for col in self.__table__.columns:
            value = getattr(self, col.name)
            if isinstance(value, datetime):
                result[col.name] = value.isoformat()
            else:
                result[col.name] = value
        return result

