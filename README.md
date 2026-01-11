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
- [10. 常见问题（FAQ）](#10-常见问题faq)
- [11. AI 协作开发提示（让 AI 更懂这个仓库）](#11-ai-协作开发提示让-ai-更懂这个仓库)

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

### 1.1 这些理念在代码里的落点（快速索引）

> 这一节是“带你定位”的索引，不改变现有约束，只帮助将来回看时更快上手。

- 应用工厂入口：`app/__init__.py` -> `create_app()`
- 配置切换：`app/config.py`（Development/Production/Testing）
- 蓝图路由：`app/routes/`（`auth.py` / `main.py` / `i18n.py`）
- 数据模型：`app/models/`（框架模型建议以 `sk_` 前缀命名）
- 测试：`tests/`（pytest）

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

### 3.1 功能入口快速定位

- 登录/注册/注销：`/auth/login`、`/auth/register`、`/auth/logout`（见 `app/routes/auth.py`）
- 仪表盘：`/dashboard`（见 `app/routes/main.py`）
- 用户列表示例页：`/users`（见 `app/routes/main.py`）
- 健康检查：`/health`（见 `app/routes/main.py`）
- 语言切换：`/i18n/set/<lang>`（见 `app/routes/i18n.py`）

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

### 4.3 配置与代码组织（补充说明）

- 配置建议集中在 `app/config.py`，统一通过环境变量进入配置类，再由 `create_app()` 加载。
- 不建议业务代码到处 `os.getenv()`：统一从 `current_app.config` 读取，便于测试与部署。
- 新功能尽量按“模块 -> blueprint -> template/static -> tests”成套落地，减少“只写路由没测试”的漂移。

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

#### 5.2.1 环境变量清单（建议补齐到 .env.example）

> 下面是“建议你在未来作为模板复用时一定要检查”的变量清单。是否启用由代码实现决定；这一节主要用于快速排错与交接。

- `SECRET_KEY`
  - 用途：Flask session/cookie 签名。
  - 建议：生产环境必须是强随机且不可泄露。
- `APP_ENV`
  - 取值：`development` / `production` / `testing`
  - 用途：切换 Config（Development/Production/Testing）与不同数据库策略。
- `DATABASE_URL`
  - 用途：开发/生产数据库连接 URL。
  - 示例（MySQL）：`mysql+pymysql://user:password@host:3306/dbname?charset=utf8mb4`
  - 示例（SQLite，仅快速试跑）：`sqlite:///instance/starterkit.db`
- （测试专用）`TEST_DATABASE_URL`
  - 用途：pytest 强制使用的测试数据库 URL（通常是 sqlite），避免误连开发/生产数据库。
  - 示例：`sqlite:///instance/test.db`
- （可选）`FLASK_DEBUG`
  - 用途：调试开关（常见为 `1`）。实际是否生效取决于运行方式与配置逻辑。

> 小提示：SQLite 使用相对路径时与“当前工作目录”相关；如果你发现 DB 文件位置不对，优先检查 `DATABASE_URL` 的写法与运行时工作目录。

### 5.3 启动项目

```bash
python run.py
```

默认访问：
- 登录：`/auth/login`
- 注册：`/auth/register`（注册成功自动登录并跳转 dashboard）
- 仪表盘：`/dashboard`

### 5.4 一个推荐的本地开发工作流（可复用模板）

1. 配置 `.env`
2. 安装依赖
3. 启动 `python run.py`
4. 打开 `/auth/register` 注册一个账号（开发/测试阶段）
5. 进入 `/dashboard` 验证登录态与页面布局

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

### 6.1 日常迁移建议（补充）

- **典型流程**：改模型（models）→ `db migrate` 生成脚本 → 人工 review 迁移脚本 → `db upgrade` 应用。
- **多人协作**：避免同时改同一张表结构；合并前务必回放迁移，减少冲突。
- **包含数据迁移时**：建议写清楚 upgrade/downgrade 的数据处理逻辑（并加备份/回滚策略）。

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

### 7.3 i18n 开发约定（补充）

- **模板中文案必须包裹**：统一使用 `{{ _('文案') }}`，否则无法被 Babel 提取。
- **新增/修改文案后的固定动作**：extract → update → 翻译 po → compile。

---

## 8. 运行测试

```bash
pytest -q
```

测试说明：
- `TestingConfig` 默认强制使用 SQLite，避免误连 MySQL。
- 覆盖：注册/登录/访问控制/健康检查/i18n。

### 8.1 测试工作流与隔离原则（补充）

- 测试环境的目标是：**不会因为本地环境变量配置错误而误连生产/开发数据库**。
- 如果你在测试里需要特定 DB 文件位置，优先通过 `TEST_DATABASE_URL` 明确指定。

---

## 9. 将来迭代规划

- [ ] RBAC 权限模型（角色/权限）
- [ ] 通用 API 返回结构
- [ ] 多主题皮肤切换

---

## 10. 常见问题（FAQ）

### 10.1 `DATABASE_URL` 密码包含特殊字符怎么办？

需要做 URL 编码（例如 `/` → `%2F`）。这是最常见的“能连上但认证失败/解析失败”原因之一。

### 10.2 pytest 会不会误连 MySQL / 生产库？

按设计不会：测试环境使用 `TestingConfig` 并强制走 SQLite（必要时可用 `TEST_DATABASE_URL` 覆盖）。

### 10.3 `flask db` 命令不可用/迁移失败如何排查？

- 确认依赖已安装：`Flask-Migrate`、`Flask-SQLAlchemy`
- 确认命令格式：示例里使用 `flask --app run.py db ...`
- 查看更详细说明：`docs/DB_MIGRATION.md`

### 10.4 语言切换为什么刷新后不生效？

请使用 `/i18n/set/<lang>` 切换语言，它会写入 session/cookie（并在刷新后保持）。

### 10.5 日志文件在哪？怎么调整？

项目使用 RotatingFileHandler（滚动日志）。通常日志会写入 `logs/starterkit.log`（路径与配置以代码为准）。

---

## 11. AI 协作开发提示（让 AI 更懂这个仓库）

> 目标：将来你把这个 Starter Kit 当模板复制出来时，把这段当成“给 AI 的项目说明书”。

### 11.1 给 AI 的最小上下文（建议粘贴到对话开头）

- 这是一个 Flask 应用工厂（create_app）项目，不要改成单文件 Flask。
- 框架表必须以 `sk_` 为前缀；业务表用业务缩写前缀。
- 关键入口/写库/异常要用 `app.logger` 记录日志。
- 模板文案的国际化必须用 `{{ _('...') }}`。
- 任何新增功能尽量同时补：路由 + 模板/静态资源 + 测试（pytest）。

### 11.2 提需求时的推荐格式（让 AI 更稳定输出）

- **目标**：一句话说明要实现什么。
- **范围**：会改哪些模块（routes/models/templates/tests/config）。
- **验收**：期望的页面路径/返回码/数据落库结果/测试用例。
- **约束**：是否能改 DB schema、是否必须向后兼容、是否需要 i18n。

### 11.3 AI 改动后的自检清单

- [ ] 是否遵守 `sk_` 表前缀/命名空间隔离约束？
- [ ] 是否新增了配置项/环境变量？如果有，README 与 `.env.example` 是否同步？
- [ ] 是否补了至少 1 个 happy path 测试 + 1 个失败/边界测试？
- [ ] 是否在关键路径加了必要日志（避免敏感信息）？
- [ ] 是否保持工厂模式与蓝图组织方式？
