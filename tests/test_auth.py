# /tests/test_auth.py


def test_register_and_login_and_dashboard(client):
    # 注册（密码策略：>=8 且包含字母+数字）
    resp = client.post(
        "/auth/register",
        data={"email": "u1@example.com", "password": "Pass12345", "password2": "Pass12345"},
        follow_redirects=True,
    )
    assert resp.status_code == 200

    # 登录
    resp = client.post(
        "/auth/login",
        data={"email": "u1@example.com", "password": "Pass12345"},
        follow_redirects=True,
    )
    assert resp.status_code == 200

    # Dashboard 必须可访问
    resp = client.get("/dashboard")
    assert resp.status_code == 200


def test_dashboard_requires_login(client):
    resp = client.get("/dashboard")
    # 未登录应跳转到登录页
    assert resp.status_code in (301, 302)
    assert "/auth/login" in resp.headers.get("Location", "")


def test_register_duplicate_email_shows_friendly_message(client):
    # 第一次注册
    resp = client.post(
        "/auth/register",
        data={"email": "dup@example.com", "password": "Pass12345", "password2": "Pass12345"},
        follow_redirects=True,
    )
    assert resp.status_code == 200

    # 第二次注册同邮箱，应提示更友好信息（字段错误或 flash）
    resp = client.post(
        "/auth/register",
        data={"email": "dup@example.com", "password": "Pass12345", "password2": "Pass12345"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert "该邮箱已被注册" in resp.get_data(as_text=True)
