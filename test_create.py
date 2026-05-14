from db import get_connection
from decimal import Decimal

conn = get_connection()
cursor = conn.cursor()

try:
    # Try to create a user
    cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', ('Test User', 'test@example.com'))
    user_id = cursor.lastrowid
    print(f"User created with ID: {user_id}")

    # Try to create account
    cursor.execute('INSERT INTO accounts (user_id, balance) VALUES (%s, %s)', (user_id, Decimal('0.00')))
    print("Account created")

    conn.commit()
    print("Success!")

except Exception as e:
    print(f"Error: {e}")
    conn.rollback()

finally:
    cursor.close()
    conn.close()