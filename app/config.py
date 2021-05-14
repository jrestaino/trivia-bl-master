import os

# configuraciones. True para que el servidor pueda ser levantado en modo debug
DEBUG = True

# configuracion BD

POSTGRES = {
    'user': 'd052835',
    'pw': 'Pone tu pass aca',
    'db': 'd052835',
    'host': '179.27.167.7',
    'port': '5432',
}

SECRET_KEY = os.getenv('SECRET_KEY') or 'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'

SQLALCHEMY_TRACK_MODIFICATIONS = False

#postgresql://username:password@hostname/database
#SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/trivia"
SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES['user']}:" \
                          f"{POSTGRES['pw']}@{POSTGRES['host']}:" \
                          f"{POSTGRES['port']}/{POSTGRES['db']}"

