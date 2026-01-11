# /docs/README_EXTRA.md

# StarterKit 说明文档补充

本文补充项目的运行约定、模块说明与开发建议，避免约定丢失。

---

## 1. 关键约定（来自 requirements.md / README.md）

1) **中文优先**：沟通、注释中文优先。

2) **文件首行写相对路径**：例如 `# /app/routes/main.py`。

3) **日志规范**：
- 路由入口、数据库增删改查、异常捕获都要使用 `app.logger` 记录关键事件。

4) **命名空间契约**：
- 框架基础表：以 `sk_` 开头（例如 `sk_user`）
- 业务表：建议使用项目缩写前缀（例如 `pro_`）

---

## 2. 当前已实现的模块

- 认证（注册/登录/注销）：`app/routes/auth.py`
- Dashboard：`app/routes/main.py`
- 用户模型：`app/models/sk_models.py`（`SkUser` => `sk_user`）
- 基础模型：`app/models/base.py`（`BaseModel`）
- 表单：`app/forms.py`
- 前端布局：`app/templates/base.html`（本地 Bootstrap 5.3.8）

---

## 3. 登录拦截方式（升级后）

- 统一使用 Flask-Login 的 `@login_required`
- 未登录访问时：由 `LoginManager.unauthorized_handler` 统一跳转到登录页，并携带 `?next=/xxx`

---

## 4. 快速启动

```bash
pip install -r requirements.txt
python run.py
```

访问：
- 登录页：`/auth/login`
- 注册页：`/auth/register`
- Dashboard：`/dashboard`

---

## 5. 测试

```bash
pytest -vv
```

---

## 6. 数据库迁移

请阅读：`docs/DB_MIGRATION.md`

