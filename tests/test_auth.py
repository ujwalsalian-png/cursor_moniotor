import app as app_module


def _client():
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()


def test_unsigned_home_redirects_to_login():
    response = _client().get("/", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")


def test_wrong_password_stays_on_the_form():
    response = _client().post("/login", data={"username": "admin", "password": "nope"})
    assert response.status_code == 200
    page = response.get_data(as_text=True)
    assert "Invalid username or password." in page
    assert "nope" not in page


def test_correct_password_starts_a_session():
    client = _client()
    response = client.post(
        "/login",
        data={"username": "admin", "password": "admin123"},
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")
    cookie = response.headers["Set-Cookie"]
    assert "HttpOnly" in cookie
    assert "SameSite=Lax" in cookie
    page = client.get("/").get_data(as_text=True)
    assert "Sign out" in page
    assert "admin123" not in page


def test_sign_out_clears_the_session():
    client = _client()
    client.post("/login", data={"username": "admin", "password": "admin123"})
    response = client.get("/logout", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")
    home = client.get("/", follow_redirects=False)
    assert home.status_code == 302
    assert home.headers["Location"].endswith("/login")
    page = client.get("/login").get_data(as_text=True)
    assert "Sign in" in page
    assert "Sign out" not in page
