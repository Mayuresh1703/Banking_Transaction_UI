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
cursor.execute('DESCRIBE users')
columns = cursor.fetchall()
print("Users table structure:")
for col in columns:
    print(col)

cursor.close()
conn.close()