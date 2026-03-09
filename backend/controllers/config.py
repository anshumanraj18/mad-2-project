class config:
    SECRET_KEY = 'super-secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SECURITY_PASSWORD_SALT = 'super-secret-salt'

    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'

    WTF_CSRF_ENABLED = False
    SECURITY_CSRF_PROTECT_MECHANISMS = []
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True