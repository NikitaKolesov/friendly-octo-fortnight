from contextlib import contextmanager
from datetime import timedelta
from os import getenv
from pathlib import Path

import mysql.connector as connector
from mysql.connector import DatabaseError, ProgrammingError
from retrying import retry


def iter_lines_csv(fp):
    while True:
        line = fp.readline()
        if not line:
            return
        yield line.strip().split(',')


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
    mysql_password = getenv('MYSQL_PASSWORD', 'iLoveGachiMuchi')
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


def main():
    with connection_context() as conn:
        mysql_table = getenv('MYSQL_TABLE', Path(getenv('CSV_PATH', '/data/data.csv')).name)
        cursor = conn.cursor()
        cursor.execute(
            f"""\
        CREATE TABLE IF NOT EXISTS {mysql_table} (
        id INT NOT NULL AUTO_INCREMENT,
        data TEXT NOT NULL,
        val FLOAT NOT NULL,
        PRIMARY KEY (id) )"""
        )
        with open(getenv('CSV_PATH', '/data/data.csv'), 'r') as f:
            for line in iter_lines_csv(f):
                insert_st = f"INSERT INTO {mysql_table} (data, val) VALUES ('{line[0]}', {line[1]})"
                cursor.execute(insert_st)
        conn.commit()
        cursor.execute(f'SELECT * from {mysql_table};')
        records = cursor.fetchall()
        print(records)


if __name__ == '__main__':
    main()
