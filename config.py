import os

SECRET_KEY = os.environ.get("SECRET_KEY", "demo-localhost-only")
ADMIN_USERNAME = "admin"
# Werkzeug pbkdf2:sha256 hash. The plain password is not stored here.
ADMIN_PASSWORD_HASH = (
    "pbkdf2:sha256:1000000$6eTwJsWnIk4Z23Zi$"
    "212c91b88f302bb800d32e8faa4a71e0b9d4d7464a6964e2c2374ddfc2f43c19"
)
