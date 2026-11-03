from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

import config
import metrics

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False

_PUBLIC_ENDPOINTS = {"login", "static"}


def _signed_in():
    return session.get("user") == config.ADMIN_USERNAME


@app.template_filter("bytes")
def _bytes_filter(value):
    return metrics.format_bytes(value)


@app.context_processor
def inject_signed_in():
    return {"signed_in": _signed_in()}


@app.before_request
def require_sign_in():
    if request.endpoint in _PUBLIC_ENDPOINTS or _signed_in():
        return None
    if request.path.startswith("/api/"):
        return jsonify({"error": "Unauthorized"}), 401
    return redirect(url_for("login"))


@app.get("/")
def dashboard():
    return render_template("dashboard.html", metrics=metrics.collect_all())


@app.get("/api/metrics")
def api_metrics():
    if not _signed_in():
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(metrics.collect_all())


@app.route("/login", methods=["GET", "POST"])
def login():
    if _signed_in():
        return redirect(url_for("dashboard"))

    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        password_ok = username == config.ADMIN_USERNAME and check_password_hash(
            config.ADMIN_PASSWORD_HASH, password
        )
        if password_ok:
            session.clear()
            session["user"] = config.ADMIN_USERNAME
            return redirect(url_for("dashboard"))
        error = "Invalid username or password."

    return render_template("login.html", error=error)


@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
