import app as app_module
import metrics


def _client():
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()


def _sign_in(client):
    return client.post(
        "/login",
        data={"username": "admin", "password": "admin123"},
        follow_redirects=False,
    )


def test_metrics_requires_sign_in():
    response = _client().get("/api/metrics")
    assert response.status_code == 401
    assert response.get_json()["error"] == "Unauthorized"


def test_metrics_returns_sections_when_signed_in():
    client = _client()
    _sign_in(client)

    response = client.get("/api/metrics")

    assert response.status_code == 200
    payload = response.get_json()
    assert set(payload) == {"host", "cpu", "memory", "network", "ports"}


def test_failed_metric_is_null_in_the_api(monkeypatch):
    def explode():
        raise RuntimeError("do not show this stack")

    monkeypatch.setattr(metrics, "collect_cpu", explode)
    client = _client()
    _sign_in(client)

    response = client.get("/api/metrics")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["cpu"] is None
    assert "do not show this stack" not in response.get_data(as_text=True)
