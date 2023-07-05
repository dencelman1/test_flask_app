import os
from collections import namedtuple
from dotenv import load_dotenv


# pgAdmin4 - "C:\Program Files\PostgreSQL\15\pgAdmin 4\python\python.exe" "C:\Program Files\PostgreSQL\15\pgAdmin 4\web\pgAdmin4.py"
# psqlServer - net start postgresql

# pg_ctl status -D "C:\Program Files\PostgreSQL\15\data"
# pg_ctl start -D "C:\Program Files\PostgreSQL\15\data" -o "-p 8010"
# pg_ctl stop -D "C:\Program Files\PostgreSQL\15\data"

SQLALCHEMY_TRACK_MODIFICATIONS = True

host = "127.0.0.1"
port = 8000

SSL_KEY_PATH = None
SSL_CERT_PATH = None



def get_uri():
    load_dotenv()
    uri_keys = ["protocol", 'user', "password", "host", "port", "database_name"]
    uri_values = {key: str(os.getenv(key.upper())) for key in uri_keys}
    print(uri_values)
    return '{protocol}://{user}:{password}@{host}:{port}/{database_name}'.format(**uri_values)

def get_ssl_path():
    SslPath = namedtuple("SSL_PATH", ["key", 'cert', 'local'])

    is_local = False
    if [SSL_CERT_PATH, SSL_KEY_PATH] == [None]*2:
        is_local = True

    return SslPath(key=SSL_KEY_PATH, cert=SSL_CERT_PATH, local=is_local)


SQLALCHEMY_DATABASE_URI = get_uri()
SSL_PATH = get_ssl_path()

basedir = os.path.abspath(os.path.dirname(__file__))
