import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
conn = mysql.connector.connect(
    host=os.getenv('DB_HOST', '127.0.0.1'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', '12345'),
    database=os.getenv('DB_NAME', 'bank')
)
cursor = conn.cursor()
for table in ['accounts', 'transactions']:
    cursor.execute(f'SHOW CREATE TABLE {table}')
    row = cursor.fetchone()
    print(f'--- {table} CREATE ---')
    print(row[1])
    print()
cursor.close()
conn.close()