import os

from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode

load_dotenv()

DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'your_password')
DB_NAME = os.getenv('DB_NAME', 'bank')

schema_sql = open('init_db.sql', 'r', encoding='utf-8').read()


def get_server_connection():
    print(f'Connecting to MySQL on {DB_HOST} as {DB_USER}...')
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            autocommit=True,
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            raise RuntimeError(
                f'Invalid MySQL credentials for {DB_USER}@{DB_HOST}. Check .env and verify MySQL user permissions.'
            ) from err
        raise


def initialize_database():
    conn = get_server_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f'CREATE DATABASE IF NOT EXISTS `{DB_NAME}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        conn.database = DB_NAME
        for statement in schema_sql.split(';'):
            sql = statement.strip()
            if sql:
                cursor.execute(sql)
        print('Database and schema created successfully.')
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    initialize_database()
    initialize_database()
