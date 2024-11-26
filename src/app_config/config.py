from os import environ

class DbSettings:
    def __init__(self):
        try:
            self.name = environ['POSTGRES_DB']
            self.host = environ['POSTGRES_HOST']
            self.port = environ['POSTGRES_PORT']
            self.user = environ['POSTGRES_USER']
            self.password = environ['POSTGRES_PASSWORD']
        except KeyError as e:
            print(f'An error occurred: {e} not set')
            raise SystemExit(1)


class DjangoSettings:
    def __init__(self):
        try:
            self.secret_key = environ['SECRET_KEY']
            self.time_zone = environ['TIME_ZONE']
            self.debug = (environ['DEBUG'].lower() == 'true')
            self.allowed_hosts = environ['ALLOWED_HOST'].split(',')
            self.csfr_trusted_origin  = environ['CSRF_TRUSTED_ORIGINS'].split(',')
        except KeyError as e:
            print(f'An error occurred: {e} not set')
            raise SystemExit(1)