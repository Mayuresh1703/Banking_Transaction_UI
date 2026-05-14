from db import get_connection
from decimal import Decimal

try:
    conn = get_connection()
    cursor = conn.cursor()

    # Test creating a user
    cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', ('Test User', 'test@example.com'))
    user_id = cursor.lastrowid
    print(f"User created with ID: {user_id}")

    # Test creating account
    cursor.execute('INSERT INTO accounts (user_id, balance) VALUES (%s, %s)', (user_id, Decimal('0.00')))
    print("Account created")

    conn.commit()
    print("Success! Database schema is correct.")

except Exception as e:
    print(f"Error: {e}")
    if conn:
        conn.rollback()

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()