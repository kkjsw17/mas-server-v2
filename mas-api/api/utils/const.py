"""
Constant Variables
"""

LOGGERS = [
    "uvicorn",
    "uvicorn.asgi",
    "uvicorn.access",
    "uvicorn.error",
    "gunicorn",
    "gunicorn.access",
    "gunicorn.error",
    "gunicorn.http.wsgi",
    "gunicorn.http",
]

DATABASE_DRIVER_CLASS = {"mysql": "mysql+aiomysql"}

OAUTH2_ALGORITHM = "HS256"
OAUTH2_ACCESS_TOKEN_EXPIRE_MINUTES = 30

COOKIE_AUTHORIZATION_NAME = "mas-auth-token"
COOKIE_DOMAIN = "localhost"

JWT_DECODING_OPTIONS = {
    "verify_at_hash": False,
    "verify_signature": True,
    "verify_aud": False,
    "exp": True,
}

"""
Exception Related
"""

SCRIPT_DELETION_VALIDATION_EXCEPTION_MESSAGE = (
    "script_ids must be list of integer, like `1,2,3`"
)

MEETING_TITLE_LENGTH_VALIDATION_MESSAGE = (
    "Title must be no longer than 20 characters long."
)
MEETING_CAPACITY_VALIDATION_MESSAGE = "Capacity must be no more than 10 people. We are trying to increase the number of meetings. 🥲"
