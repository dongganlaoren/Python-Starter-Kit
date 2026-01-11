# /scripts/check_db_url.py
"""DATABASE_URL 连接串检查工具。

用途：
- 在不泄露密码的前提下，检查 DATABASE_URL 是否能被 SQLAlchemy 解析。
- 可选：尝试建立连接（会实际连数据库）。

运行示例：
- 仅解析：python scripts/check_db_url.py
- 解析 + 连接：python scripts/check_db_url.py --connect

注意：
- 若 MySQL 密码包含特殊字符，应进行 URL 编码（percent-encoding）。
"""

from __future__ import annotations

import argparse
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url


def mask_password(db_url: str) -> str:
    """隐藏密码，输出更安全的连接串用于日志/控制台。"""
    url_obj = make_url(db_url)
    if url_obj.password:
        url_obj = url_obj.set(password="***")
    return str(url_obj)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connect", action="store_true", help="是否尝试实际连接数据库")
    args = parser.parse_args()

    load_dotenv(".env")

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("[ERROR] DATABASE_URL 未设置")
        return 2

    # 解析校验
    try:
        url_obj = make_url(db_url)
    except Exception as e:
        print("[ERROR] DATABASE_URL 解析失败:", e)
        return 3

    print("[OK] DATABASE_URL 可解析:", mask_password(db_url))
    print("     drivername:", url_obj.drivername)
    print("     host:", url_obj.host)
    print("     port:", url_obj.port)
    print("     database:", url_obj.database)

    if not args.connect:
        return 0

    # 实际连接（短连接）
    try:
        engine = create_engine(db_url, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.exec_driver_sql("SELECT 1")
        print("[OK] 数据库连接成功")
        return 0
    except Exception as e:
        print("[ERROR] 数据库连接失败:", e)
        return 4


if __name__ == "__main__":
    raise SystemExit(main())

