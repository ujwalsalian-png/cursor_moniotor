# Demo Server Monitoring — Requirements

Local demo. One Linux machine: the host where this app runs. Read-only after sign-in.

## Problem

Internal teams currently sign in to servers to check live CPU, memory, network, and port usage. This demo shows those details in a browser so people do not need a shell for a quick check.

## Users

L1, L2, L3, and application teams. Everyone uses the same read-only view. This demo has no separate roles.

## Assumptions

These are the defaults used because later choices were not confirmed:

- Metrics come from this Linux host only. No SSH and no remote agents.
- The app does not ask the user to add servers. It always monitors the machine it is running on.
- One account: username `admin`. The password is stored only as a hash.
- Demo password: `admin123`. Change the hash before any shared use.
- The page refreshes on its own about every 5 seconds. There is also a Refresh button.
- The app listens on `127.0.0.1` only.

## Goals

- Show current CPU, memory, network, and listening-port usage without a server login.
- Keep the screen view-only. No commands, no edits, no process control.
- Run on the machine where Cursor is open, with a short local setup.

## Out of scope

- Remote Linux or Windows hosts
- Add, edit, or remove server forms
- Alerts, history, charts over time, or saved reports
- Multiple users, roles, or password change in the UI
- Shell access or any write action on the host

## Tech

- Python 3, Flask, server-rendered pages
- `psutil` for live host metrics
- Werkzeug password hashing (`pbkdf2:sha256`)
- Bootstrap 5 from a CDN for layout, plus a small local stylesheet
- No database. Metrics are read when the page or API is requested.

## Sign-in

- Public page: sign-in form only.
- Username is fixed: `admin`.
- The app stores a password hash in local config, not the plain password.
- A correct password starts a Flask session. A wrong password shows an error and stays on the form.
- Sign out clears the session.
- Every other page and the metrics endpoint require a signed-in session.

## Monitoring view

One page after sign-in. It shows this host only:

| Area | What the user sees |
| --- | --- |
| Host | Hostname and operating system |
| CPU | Overall percent busy, and per-core percent |
| Memory | Total, used, available, and percent used |
| Network | Each interface: bytes sent, bytes received |
| Ports | Listening TCP/UDP ports: port, address, protocol, process name if available |

- Numbers update about every 5 seconds without a full navigation, and when the user presses Refresh.
- The view has no inputs except sign out and Refresh.
- If a metric cannot be read, that card or row shows "Unavailable" and the rest of the page still loads.

## Pages

- `/login` — username and password
- `/` — monitoring view (signed in)
- `/logout` — ends the session and returns to sign-in
- `/api/metrics` — JSON for the same figures (signed in). The page uses this to refresh.

## Local run

From the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` and sign in as `admin` / `admin123`.

## Done when

- Unsigned users can only reach the sign-in page.
- `admin` with the demo password reaches the monitoring view. Any other password does not.
- The view shows live CPU, memory, network, and listening ports for this machine.
- Values change on the auto-refresh without signing in to a shell.
- The UI has no control that changes the host.
- The app is reachable only on localhost.
