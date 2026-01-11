# /README.md

# FlaskStarterKit

FlaskStarterKit 是一个基于 **Flask 工厂模式**的通用后端 Starter Kit。内置：

- 用户注册/登录（Flask-Login）+ Dashboard
- 数据库（Flask-SQLAlchemy）+ 迁移（Flask-Migrate/Alembic）
- 国际化（Flask-Babel）中英文切换
- Bootstrap 5 + 手写后台布局（Sidebar + Navbar）
- 生产可用的日志（RotatingFileHandler）

> 定位：适合中小型后台/管理系统作为“可运行、可扩展”的起步框架。

---

## 目录

- [1. 项目意图与核心理念](#1-项目意图与核心理念)
- [2. 技术栈清单](#2-技术栈清单)
- [3. 当前目录结构（已实现）](#3-当前目录结构已实现)
- [4. 命名约定与开发守则](#4-命名约定与开发守则)
- [5. 快速开始](#5-快速开始)
- [6. 数据库迁移（Flask-Migrate）](#6-数据库迁移flask-migrate)
- [7. 国际化（Flask-Babel）](#7-国际化flask-babel)
- [8. 运行测试](#8-运行测试)
- [9. 将来迭代规划](#9-将来迭代规划)

---

## 1. 项目意图与核心理念

- **可持续迭代（Framework vs Business）**：
  推荐通过 Git 分支管理，`main` 分支保持框架核心的纯净与更新，业务项目通过分支继承并扩展。

- **命名空间隔离**：
  严格区分“框架资产”与“业务资产”，避免升级/迁移时产生命名冲突。

- **小白友好且专业**：
  代码注释清晰（中文），采用 Flask 工厂模式，关键入口与写入行为使用 `app.logger` 记录。

- **精简 UI**：
  拒绝臃肿后台模板，采用 Bootstrap 5 + 手写 CSS 组合，确保可控和易改。

---

## 2. 技术栈清单

- **Python**：3.x
- **Web 框架**：Flask（应用工厂模式）
- **数据库**：默认开发 MySQL（可切换），测试环境强制使用 SQLite
- **ORM**：Flask-SQLAlchemy
- **迁移**：Flask-Migrate（Alembic）
- **鉴权**：Flask-Login
- **表单**：Flask-WTF / WTForms
- **国际化**：Flask-Babel
- **日志**：RotatingFileHandler
- **前端**：Bootstrap 5.3.8（本地静态资源集成）

---

## 3. 当前目录结构（已实现）

> 以下为仓库当前实际结构（会随迭代演进）。

```text
Python-Starter-Kit/
├── app/
│   ├── __init__.py              # create_app + DB/Babel/Login/Logging 初始化
│   ├── config.py                # Development/Production/Testing 配置切换
│   ├── forms.py                 # Login/Register 表单
│   ├── models/
│   │   ├── base.py              # BaseModel
│   │   └── sk_models.py         # SkUser 等（表名前缀 sk_）
│   ├── routes/
│   │   ├── __init__.py          # 注册蓝图
│   │   ├── auth.py              # 注册/登录/注销
│   │   ├── i18n.py              # 语言切换 /i18n/set/<lang>
│   │   └── main.py              # /dashboard /users /health
│   ├── static/
│   │   ├── css/admin.css
│   │   ├── ico/Python Starter Kit.png
│   │   ├── js/common.js
│   │   └── vendor/bootstrap-5.3.8/   # Bootstrap 本地资源
│   ├── templates/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── users/index.html
│   │   ├── auth/
│   │   │   ├── _layout.html
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── errors/
│   │       ├── 404.html
│   │       └── 500.html
│   └── utils/
│       └── auth.py
├── migrations/                  # Alembic 迁移目录（flask db init 后生成）
├── translations/                # Babel 翻译文件（.po/.mo）
├── tests/                       # pytest 测试
├── docs/                        # 补充说明文档（迁移等）
├── requirements.txt
└── run.py
```

---

## 4. 命名约定与开发守则

### 4.1 数据库命名规范

为了支持框架长期迭代，建议遵守：

- **框架基础表**：必须以 `sk_`（StarterKit）开头。
  - 示例：`sk_user`、`sk_config`

- **业务项目表**：以业务项目缩写开头。
  - 示例：`pro_order`、`pro_article`

### 4.2 开发守则

- **日志记录**：关键路由入口、写库动作需要 `app.logger.info()/error()`。
- **国际化**：模板中文案统一使用 `{{ _('文案') }}`。
- **风格建议**：
  - 类名：大驼峰（`SkUser`）
  - 变量/字段：小写 + 下划线（`user_name`）

---

## 5. 快速开始

### 5.1 安装依赖

```bash
pip install -r requirements.txt
```

### 5.2 环境变量（.env / .env.example）

- **项目真正生效的是 `.env`**（被 `python-dotenv` 加载）。
- `.env.example` 仅用于提供示例模板（应提交到 Git）。

推荐做法：复制并修改：

```bash
cp .env.example .env
```

关键变量（示例）：

- `SECRET_KEY=...`
- `APP_ENV=development|production|testing`
- `DATABASE_URL=mysql+pymysql://user:password@host:3306/dbname?charset=utf8mb4`

> 注意：如果密码包含特殊字符（如 `/`），需要做 URL 编码（例如 `/` → `%2F`）。

### 5.3 启动项目

```bash
python run.py
```

默认访问：
- 登录：`/auth/login`
- 注册：`/auth/register`（注册成功自动登录并跳转 dashboard）
- 仪表盘：`/dashboard`

---

## 6. 数据库迁移（Flask-Migrate）

本项目已集成 Flask-Migrate：

1) 初始化迁移目录（只需一次）：

```bash
flask --app run.py db init
```

2) 生成迁移脚本：

```bash
flask --app run.py db migrate -m "init"
```

3) 应用迁移：

```bash
flask --app run.py db upgrade
```

> 更详细说明见：`docs/DB_MIGRATION.md`

---

## 7. 国际化（Flask-Babel）

### 7.1 语言切换

- 页面右上角“语言”菜单
- 或直接访问：`/i18n/set/en` / `/i18n/set/zh_CN`

切换后会写入 session/cookie，刷新仍保持。

### 7.2 翻译文件维护流程

1) 提取文案：

```bash
pybabel extract -F babel.cfg -o messages.pot .
```

2) 更新翻译：

```bash
pybabel update -i messages.pot -d translations
```

3) 编译生成 .mo：

```bash
pybabel compile -d translations
```

---

## 8. 运行测试

```bash
pytest -q
```

测试说明：
- `TestingConfig` 默认强制使用 SQLite，避免误连 MySQL。
- 覆盖：注册/登录/访问控制/健康检查/i18n。

---

## 9. 将来迭代规划

- [ ] RBAC 权限模型（角色/权限）
- [ ] 通用 API 返回结构
- [ ] 多主题皮肤切换
