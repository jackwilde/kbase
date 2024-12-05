from os import environ
import secrets


def generate_secret_key():
    """
    Generate a secret key for this application.
    return: 64-bit secret key
    """
    return secrets.token_urlsafe(64)


class DbSettings:
    """
    Creates a DbSettings object for this application from environment variables.

    Attributes
    ----------
    name : str
        database name
    host: str
        database host
    port: str
        database port (default is 5432)
    user: str
        database user
    password: str
        database password
    """

    def __init__(self):
        try:
            self.name = environ.get('POSTGRES_DB')
            self.host = environ.get('POSTGRES_HOST')
            self.port = environ.get('POSTGRES_PORT', "5432")
            self.user = environ.get('POSTGRES_USER')
            self.password = environ.get('POSTGRES_PASSWORD')
        except KeyError as e:
            print(f'An error occurred: {e} not set')
            raise SystemExit(1)


class DjangoSettings:
    """
    Creates a DjangoSettings object for this application from environment variables.

    Attributes
    ----------
    secret_key : str
        secret key use for cryptographic signing
    time_zone: str
        server timezone. (default is UTC)
    debug: str
        debug mode. (default is False)
    allowed_hosts: str
        list of approved hostnames for the website
    csfr_trusted_origin: str
        list of approved hostnames for CSFR protection
    """

    def __init__(self):
        try:
            self.secret_key = environ.get('SECRET_KEY')
            self.time_zone = environ.get('TIME_ZONE', 'UTC')
            self.debug = (environ.get('DEBUG', 'false').lower() == 'true')
            self.allowed_hosts = environ.get('ALLOWED_HOST', '').split(',')
            self.csfr_trusted_origin = environ.get('CSRF_TRUSTED_ORIGINS').split(',') if environ.get(
                'CSRF_TRUSTED_ORIGINS') else []
        except KeyError as e:
            print(f'An error occurred: {e} not set')
            raise SystemExit(1)
