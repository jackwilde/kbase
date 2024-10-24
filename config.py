from dotenv import dotenv_values
import sys

values = dotenv_values('.env')

class DbSettings:
    def __init__(self):
        try:
            self.name = values['DB_NAME']
            self.host = values['DB_HOST']
            self.port = values['DB_PORT']
            self.user = values['DB_USER']
            self.password = values['DB_PASSWORD']
        except KeyError as e:
            print(f'An error occurred: {e} not set')
            sys.exit(1)


class DjangoSettings:
    def __init__(self):
        try:
            self.secret_key = values['SECRET_KEY']
            self.time_zone = values['TIME_ZONE']
            self.debug = values['DEBUG']
        except KeyError as e:
            print(f'An error occurred: {e} not set')
            sys.exit(1)