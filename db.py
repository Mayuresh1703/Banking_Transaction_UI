import os

from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'your_password'),
    'database': os.getenv('DB_NAME', 'bank'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'autocommit': False,
}

auth_plugin = os.getenv('DB_AUTH_PLUGIN')
if auth_plugin:
    DB_CONFIG['auth_plugin'] = auth_plugin

SCHEMA_SQL = open('init_db.sql', 'r', encoding='utf-8').read()


def initialize_schema(conn):
    cursor = conn.cursor()
    try:
        cursor.execute(f"USE `{DB_CONFIG['database']}`")
        for statement in SCHEMA_SQL.split(';'):
            sql = statement.strip()
            if sql:
                cursor.execute(sql)
        conn.commit()
    finally:
        cursor.close()


def create_database_if_missing():
    server_config = DB_CONFIG.copy()
    server_config.pop('database', None)
    try:
        conn = mysql.connector.connect(**server_config)
        cursor = conn.cursor()
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        conn.commit()
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass


def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        # Ensure table schema exists
        cursor = conn.cursor(buffered=True)
        try:
            cursor.execute('DESCRIBE users')
        except mysql.connector.Error as err:
            if err.errno in (errorcode.ER_NO_SUCH_TABLE, errorcode.ER_BAD_TABLE_ERROR):
                initialize_schema(conn)
            else:
                raise
        finally:
            cursor.close()
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database_if_missing()
            conn = mysql.connector.connect(**DB_CONFIG)
            initialize_schema(conn)
            return conn
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            if DB_CONFIG['password'] in ('your_password', ''):
                raise RuntimeError(
                    f'Invalid MySQL credentials for {DB_CONFIG["user"]}@{DB_CONFIG["host"]}. '
                    'Update .env with the correct password, or leave DB_PASSWORD blank if your MySQL user has no password.'
                ) from err
            raise RuntimeError(
                f'Invalid MySQL credentials for {DB_CONFIG["user"]}@{DB_CONFIG["host"]}. Check .env and verify MySQL user permissions.'
            ) from err
        else:
            raise
