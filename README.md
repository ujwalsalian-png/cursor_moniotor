# Server monitor

Local read-only demo for this Linux machine. After sign-in, the page shows live host, CPU, memory, network, and listening-port details.

## Run

From the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

The app listens on `127.0.0.1` only. Debug mode is off. GitHub Actions runs the tests and a localhost boot check. The demo is still started on this machine.

## Sign in

Unsigned visits to the monitor go to the sign-in page.

- Username: `admin`
- The password is stored only as a Werkzeug `pbkdf2:sha256` hash
- Demo password: `admin123`

A wrong password stays on the form and shows one generic error. Sign out clears the session.

## What the page shows

- Host card: this machine's hostname and operating system
- CPU card: overall percent and per-core percent
- Memory card: total, used, available, and percent used
- Network table: bytes sent and bytes received for each interface
- Ports table: listening TCP and UDP ports, with the process name when it is available

`GET /api/metrics` returns the same figures and requires a signed-in session. The page reloads those figures about every 5 seconds and when Refresh is pressed. A section that cannot be read shows `Unavailable`.

## Tests

```bash
.venv/bin/pytest
```
