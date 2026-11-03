from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

import config

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False

SAMPLE_SERVER = {
    "name": "this machine",
    "host": "127.0.0.1",
    "status": "Sample",
    "cpu": "12%",
    "memory": "41%",
}


def _signed_in():
    return session.get("user") == config.ADMIN_USERNAME


@app.context_processor
def inject_signed_in():
    return {"signed_in": _signed_in()}


@app.get("/")
def servers():
    return render_template("servers.html", server=SAMPLE_SERVER)


@app.route("/login", methods=["GET", "POST"])
def login():
    if _signed_in():
        return redirect(url_for("servers"))

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
            return redirect(url_for("servers"))
        error = "Invalid username or password."

    return render_template("login.html", error=error)


@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.get("/servers/add")
def add_server():
    return render_template("add_server.html")


@app.post("/servers/add")
def add_server_submit():
    return render_template(
        "add_server.html",
        notice="This demo does not save servers. The list keeps the sample row.",
    )


@app.get("/servers/this-machine")
def server_detail():
    return render_template("server_detail.html", server=SAMPLE_SERVER)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
