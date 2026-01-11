# /tests/test_i18n.py


def test_language_switch_en_shows_english(client):
    resp = client.get("/health")
    assert resp.status_code == 200

    # 切换语言到英文
    resp = client.get("/i18n/set/en", follow_redirects=True)
    assert resp.status_code == 200

    # session 中应保存 en
    with client.session_transaction() as sess:
        assert sess.get("lang") == "en"

    # 打开公开页面：应能看到英文翻译
    resp = client.get("/auth/login")
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)

    # base/auth layout 中有“语言”字样，应翻译为 Language
    assert "Language" in html
