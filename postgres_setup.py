import psycopg
import sys
from dotenv import dotenv_values

config = dotenv_values('.env')

TIMEOUT = 10

try:
    DB_ADMIN = config['DB_ADMIN']
    DB_ADMIN_PASSWORD = config['DB_ADMIN_PASSWORD']
    DB_HOST = config['DB_HOST']
    DB_PORT = config['DB_PORT']
    DB_NAME = config['DB_NAME']
    DB_USER = config['DB_USER']
    DB_PASSWORD = config['DB_PASSWORD']
except KeyError as e:
    print(f'An error occurred: {e} not set')
    sys.exit(1)

try:
    with psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_ADMIN,
            password=DB_ADMIN_PASSWORD,
            connect_timeout=TIMEOUT) as conn:

        conn.autocommit = True
        with conn.cursor() as cursor:

            # Create Database
            cursor.execute('SELECT FROM pg_database WHERE datname = %s', (DB_NAME,))
            db = cursor.fetchone()
            if db is None:
                cursor.execute(f'CREATE DATABASE {DB_NAME}')
                print(f"Database '{DB_NAME}' created successfully.")
            else:
                print(f"Database '{DB_NAME}' already exists.")

            # Create User
            cursor.execute('SELECT FROM pg_roles WHERE rolname = %s', (DB_USER,))
            user = cursor.fetchone()
            if user is None:
                # Create the user if they don't exist
                cursor.execute(f"CREATE USER {DB_USER} WITH PASSWORD '{DB_PASSWORD}';")
                print(f'User {DB_USER} created successfully.')
            else:
                # If the user exists, optionally update the password
                cursor.execute(f"ALTER USER {DB_USER} WITH PASSWORD '{DB_PASSWORD}';")
                print(f'User {DB_USER} already exists. Password updated.')

            # Set User permissions
            cursor.execute(f'GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER};')
            print(f'Granted all privileges on database {DB_NAME} to user {DB_USER}.')


except psycopg.DatabaseError as e:
    print(e)
    sys.exit(1)
