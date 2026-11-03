# Implementation TODO

Work top to bottom. Finish one checkbox before starting the next. This demo runs only on the machine where Cursor is open.

Source of truth: [requirements.md](requirements.md).

## 1. Project initialization and basic UI

- [x] Add `.gitignore` for `.venv/`, `__pycache__/`, and `.env`
- [x] Add `requirements.txt` with pinned Flask
- [x] Add `app.py` and a server-rendered page at `/`
- [x] Add a read-only dashboard shell with placeholder cards for host, CPU, memory, network, and ports
- [x] Style it with Bootstrap 5 from the CDN and a small `static/style.css`
- [x] Listen on `127.0.0.1:5000` with debug off
- [x] Security: no forms, no shell commands, and no secrets in the repo. Bind to localhost only.
- [x] Documentation: add `README.md` with the local run commands and note that the numbers are placeholders

## 2. Sign-in and unit tests

- [x] Add `/login` and `/logout`
- [x] Accept only username `admin`, checked against a Werkzeug `pbkdf2:sha256` hash in local config
- [x] On success, start a Flask session and open the dashboard. On failure, stay on the form and show one generic error.
- [x] Redirect unsigned requests for `/` to `/login`. Sign-out clears the session.
- [x] Set the session cookie to `HttpOnly` and `SameSite=Lax`
- [x] Add unit tests for a correct password, a wrong password, and sign-out
- [x] Security: never store or log the plain password. Do not print it from tests. Keep the app on localhost. `Secure` stays off because this demo is plain HTTP on localhost.
- [x] Documentation: record the demo username, that the password is stored only as a hash, and how to run the tests

## 3. Show this host

- [x] Read hostname and operating system with `psutil` and replace the host placeholder
- [x] Add a unit test that checks the shape of that data, not a fixed hostname
- [x] Security: read-only calls only. Do not run shell commands.
- [x] Documentation: note in the README that the host card is live

## 4. CPU

- [x] Show overall CPU percent and per-core percent
- [x] Add a unit test around the collector with a fake `psutil` result
- [x] Security: return numbers only. No host commands.
- [x] Documentation: note the CPU card in the README

## 5. Memory

- [x] Show total, used, available, and percent used
- [x] Add a unit test with a fake memory result
- [x] Security: return those four figures only
- [x] Documentation: note the memory card in the README

## 6. Network

- [x] Show each interface with bytes sent and bytes received
- [x] Add a unit test with a fake interface result
- [x] Security: interface counters only. No packet capture and no remote calls.
- [x] Documentation: note the network table in the README

## 7. Listening ports

- [x] Show listening TCP and UDP ports: port, address, protocol, and process name when available
- [x] Add a unit test with a fake connections result
- [x] Security: use the process name only. Do not include the command line. It can contain secrets.
- [x] Documentation: note the ports table in the README

## 8. Metrics API and refresh

- [x] Add `GET /api/metrics` with the same host, CPU, memory, network, and port figures
- [x] Require a signed-in session. Unsigned calls get `401`.
- [x] Update the dashboard from that endpoint about every 5 seconds, and when Refresh is pressed
- [x] If one metric cannot be read, show `Unavailable` for that part and still render the rest
- [x] Add tests for `401` when signed out, `200` when signed in, and a failed metric becoming `Unavailable`
- [x] Security: same-origin fetch only. Escape all values in the page. Do not send stack traces to the browser.
- [x] Documentation: list `/api/metrics` and the refresh behavior in the README

## 9. GitHub Actions CI/CD

- [x] Add `.github/workflows/ci.yml` for push and pull request
- [x] CI job: install pinned dependencies and run the unit tests
- [x] CD check: boot the app on `127.0.0.1` and request `/login`, then stop it. Do not deploy anywhere else.
- [x] Security: set workflow permissions to read-only contents. No secrets in the workflow. Do not bind `0.0.0.0`.
- [x] Documentation: state in the README that GitHub Actions runs the tests, and that the demo is still started locally

## 10. Local demo check

- [x] Run the app locally and sign in as `admin`
- [x] Confirm an unsigned visit reaches only the sign-in page
- [x] Confirm a wrong password stays on the form
- [x] Confirm the dashboard shows live CPU, memory, network, and listening ports for this machine
- [x] Confirm Refresh and the 5-second update change the numbers without a shell login
- [x] Confirm the page has no control that changes the host
- [x] Security: confirm the process listens on `127.0.0.1` only
- [x] Documentation: check the README local-run steps against what you just did
