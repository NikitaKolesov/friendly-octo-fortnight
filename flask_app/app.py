from contextlib import contextmanager
from datetime import timedelta
from os import getenv
from pathlib import Path

from flask import Flask
from mysql import connector
from mysql.connector import DatabaseError, ProgrammingError
from retrying import retry

app = Flask(__name__)


def retry_if_database_error(exception):
    """Return True if we should retry (in this case when it's an DatabaseError or ProgrammingError), False otherwise"""
    # DatabaseError when failed to connect to db
    # ProgrammingError when access denied to db
    return isinstance(exception, DatabaseError) or isinstance(exception, ProgrammingError)


@retry(
    wait_fixed=timedelta(seconds=5).seconds * 1000,
    stop_max_delay=timedelta(minutes=1).seconds * 1000,
    retry_on_exception=retry_if_database_error,
)
def connect_to_db():
    mysql_user = getenv('MYSQL_USER', 'user')
    mysql_password = getenv('MYSQL_PASSWORD', 'userpwd')
    mysql_host = getenv('MYSQL_HOST', 'db')
    mysql_port = getenv('MYSQL_PORT', '3306')
    mysql_database = getenv('MYSQL_DATABASE', 'main')
    return connector.connect(
        user=mysql_user, password=mysql_password, host=mysql_host, port=int(mysql_port), database=mysql_database
    )


@contextmanager
def connection_context():
    conn = connect_to_db()
    yield conn
    conn.close()


def select_all():
    mysql_table = getenv('MYSQL_TABLE', Path(getenv('CSV_PATH', '/data/data.csv')).name)
    with connection_context() as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * from {mysql_table};')
        records = cursor.fetchall()
        return {r[0]: {'text': r[1], 'number': r[2]} for r in records}


@app.route('/')
def data():
    text = select_all()
    return text


@app.route('/health')
def health():
    return '', 200


@app.errorhandler(404)
def page_not_found(e):
    return "Chat is going so fast that noone will notice that I'm gay", 404
