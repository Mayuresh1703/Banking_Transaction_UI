import os

from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode

load_dotenv()

DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'your_password')
DB_NAME = os.getenv('DB_NAME', 'bank')


def test_connection():
    print(f'Testing MySQL connection to {DB_HOST}:{DB_PORT} as {DB_USER} using database {DB_NAME}...')
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            autocommit=True,
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('ERROR: Invalid MySQL credentials.')
        else:
            print(f'ERROR: Could not connect to MySQL: {err}')
        return

    try:
        print('Connected to MySQL server successfully.')
        cursor = conn.cursor()
        cursor.execute('SHOW DATABASES LIKE %s', (DB_NAME,))
        exists = cursor.fetchone()
        if exists:
            print(f'Database "{DB_NAME}" already exists.')
        else:
            print(f'Database "{DB_NAME}" does not exist yet.')
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    test_connection()
