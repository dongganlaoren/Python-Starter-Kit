# /docs/DB_MIGRATION.md

# 数据库迁移指南（Flask-Migrate / Alembic）

本项目使用 Flask 工厂模式 `create_app()`，并基于 **Flask-Migrate（Alembic）** 管理数据库结构变更。

> 约定提醒：
> - 框架基础表必须以 `sk_` 开头（例如 `sk_user`）。
> - `.env` 不进入 Git；请使用 `.env.example` 作为模板。

---

## 1. 前置条件（开发环境：MySQL）

### 1.1 安装依赖

```bash
pip install -r requirements.txt
```

### 1.2 配置环境变量（推荐：根目录创建 `.env`）

示例（MySQL / SQLAlchemy URL）：

```bash
DATABASE_URL=mysql+pymysql://root:password@127.0.0.1:3306/flask_starterkit?charset=utf8mb4
SECRET_KEY=replace-me
```

#### 密码含特殊字符怎么办？

如果密码里包含 `@`、`:`、`/`、`?`、`#`、`&` 等字符，建议：

- 方式 A（推荐）：对密码进行 URL 编码（percent-encoding）
  - 例如把 `p@ss/word` 编码为 `p%40ss%2Fword`

- 方式 B：把用户名/密码放到 MySQL 账号里尽量避免特殊字符

> 否则 SQLAlchemy 可能解析出错，导致连接失败。

---

## 2. 初始化迁移目录（只需执行一次）

在项目根目录执行：

```bash
flask --app run.py db init
```

成功后会生成：
- `migrations/` 目录

---

## 3. 生成迁移脚本（第一次或后续变更）

当你新增/修改模型（例如 `SkUser`）后：

```bash
flask --app run.py db migrate -m "init"
```

这会在 `migrations/versions/` 下生成一份迁移脚本。

---

## 4. 执行迁移（升级数据库结构）

```bash
flask --app run.py db upgrade
```

执行完成后，数据库会出现 Alembic 管理表（一般叫 `alembic_version`）。

---

## 5. 常用命令速查

- 查看当前版本

```bash
flask --app run.py db current
```

- 查看历史

```bash
flask --app run.py db history
```

- 回滚到上一个版本

```bash
flask --app run.py db downgrade -1
```

---

## 6. 常见问题

### Q1: `flask db` 找不到命令？

请确认：
- `requirements.txt` 中包含 `Flask-Migrate`
- `app/__init__.py` 中已经执行 `migrate.init_app(app, db)`
- 命令使用 `flask --app run.py db ...`

### Q2: 连接 MySQL 失败？

请依次检查：
- `.env` 是否存在且 `DATABASE_URL` 正确
- MySQL 是否可连通（host/port/用户名/密码）
- 密码是否包含特殊字符且未 URL 编码

---

## 7. 推荐工作流

1) 改模型（`app/models/`）
2) 生成迁移：`flask --app run.py db migrate -m "xxx"`
3) 执行升级：`flask --app run.py db upgrade`
4) 如需回滚：`flask --app run.py db downgrade -1`
