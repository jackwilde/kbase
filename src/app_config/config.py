from os import environ

class DbSettings:
    def __init__(self):
        try:
            self.name = environ['DB_NAME']
            self.host = environ['DB_HOST']
            self.port = environ['DB_PORT']
            self.user = environ['DB_USER']
            self.password = environ['DB_PASSWORD']
        except KeyError as e:
            print(f'An error occurred: {e} not set')
            raise SystemExit(1)


class DjangoSettings:
    def __init__(self):
        try:
            self.secret_key = environ['SECRET_KEY']
            self.time_zone = environ['TIME_ZONE']
            self.debug = (environ['DEBUG'] == 'True')
            self.allowed_host = environ['ALLOWED_HOST']
            self.csfr_trusted_origin  = environ['CSRF_TRUSTED_ORIGINS']
        except KeyError as e:
            print(f'An error occurred: {e} not set')
            raise SystemExit(1)