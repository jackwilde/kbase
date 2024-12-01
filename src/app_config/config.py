from os import environ

class DbSettings:
    def __init__(self):
        try:
            self.name = environ.get('POSTGRES_DB')
            self.host = environ.get('POSTGRES_HOST')
            self.port = environ.get('POSTGRES_PORT', 5432)
            self.user = environ.get('POSTGRES_USER')
            self.password = environ.get('POSTGRES_PASSWORD')
        except KeyError as e:
            print(f'An error occurred: {e} not set')
            raise SystemExit(1)


class DjangoSettings:
    def __init__(self):
        try:
            self.secret_key = environ.get('SECRET_KEY')
            self.time_zone = environ.get('TIME_ZONE', 'UTC')
            self.debug = (environ.get('DEBUG', 'false').lower() == 'true')
            self.allowed_hosts = environ.get('ALLOWED_HOST', '').split(',')
            self.csfr_trusted_origin = environ.get('CSRF_TRUSTED_ORIGINS').split(',') if environ.get('CSRF_TRUSTED_ORIGINS') else []
        except KeyError as e:
            print(f'An error occurred: {e} not set')
            raise SystemExit(1)