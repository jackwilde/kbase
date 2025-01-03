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
    site_url: str
        Full url of site including protocol, eg https://example.com
    allowed_hosts: str
        list of approved hostnames for the website
    """

    def __init__(self):
        try:
            self.secret_key = environ.get('SECRET_KEY')
            self.time_zone = environ.get('TIME_ZONE', 'UTC')
            self.debug = (environ.get('DEBUG', 'false').lower() == 'true')
            self.site_url = environ.get('SITE_URL')
            self.allowed_hosts = environ.get('ALLOWED_HOST', '').split(',')
        except KeyError as e:
            print(f'An error occurred: {e} not set')
            raise SystemExit(1)


class EmailSettings:
    """
    Creates an EmailSettings object for this application from environment variables.

    Attributes
    ----------
    host : str
        SMTP server address
    port: str
        SMTP server port
    use_tls: bool
        use TLS (default is True)
    user: str
        SMTP user name
    password: str
        SMTP password
    default_from_email: str
        Default sender email
    """

    def __init__(self):
        try:
            self.host = environ.get('EMAIL_HOST')
            self.port = environ.get('EMAIL_PORT', "587")
            self.use_tls = (environ.get('EMAIL_USE_TLS', 'true').lower() == 'true')
            self.user = environ.get('EMAIL_HOST_USER')
            self.password = environ.get('EMAIL_HOST_PASSWORD')
            self.default_from_email = environ.get('DEFAULT_FROM_EMAIL')
        except KeyError as e:
            print(f'An error occurred: {e} not set')
            raise SystemExit(1)
