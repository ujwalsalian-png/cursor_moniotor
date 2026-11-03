# Server monitor

Local demo. The servers page matches a sample list for this machine. CPU and memory on that row are sample text, not live readings.

## Run

From the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

The app listens on `127.0.0.1` only. Debug mode is off.

## Sign in

The servers list is visible before sign-in. Use **Sign in** in the header.

- Username: `admin`
- The password is stored only as a Werkzeug `pbkdf2:sha256` hash
- Demo password: `admin123`

A wrong password stays on the form and shows one generic error. Sign out clears the session.

## Tests

```bash
.venv/bin/pytest
```
