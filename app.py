from flask import Flask, request, jsonify
from decimal import Decimal
from db import get_connection
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def query_one(cursor, sql, params=None):
    cursor.execute(sql, params or ())
    return cursor.fetchone()


def query_all(cursor, sql, params=None):
    cursor.execute(sql, params or ())
    return cursor.fetchall()


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'Banking API is running',
        'endpoints': [
            '/user',
            '/deposit',
            '/withdraw',
            '/transfer',
            '/balance/<user_id>',
            '/transactions/<user_id>'
        ]
    }), 200


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    name = data.get('name')
    email = data.get('email')
    if not name or not email:
        return jsonify({'error': 'name and email are required'}), 400

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
        user_id = cursor.lastrowid
        cursor.execute('INSERT INTO accounts (user_id, balance) VALUES (%s, %s)', (user_id, Decimal('0.00')))
        conn.commit()
        return jsonify({'user_id': user_id}), 201
    except Exception as exc:
        conn.rollback()
        return jsonify({'error': str(exc)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/deposit', methods=['POST'])
def deposit():
    data = request.get_json() or {}
    user_id = data.get('user_id')
    amount = data.get('amount')
    if not user_id or amount is None:
        return jsonify({'error': 'user_id and amount are required'}), 400
    if amount <= 0:
        return jsonify({'error': 'amount must be positive'}), 400

    conn = get_connection()
    try:
        cursor = conn.cursor()
        row = query_one(cursor, 'SELECT id, balance FROM accounts WHERE user_id = %s FOR UPDATE', (user_id,))
        if not row:
            return jsonify({'error': 'account not found'}), 404

        account_id, balance = row
        new_balance = Decimal(balance) + Decimal(amount)
        cursor.execute('UPDATE accounts SET balance = %s WHERE id = %s', (new_balance, account_id))
        cursor.execute(
            'INSERT INTO transactions (account_id, type, amount, description) VALUES (%s, %s, %s, %s)',
            (account_id, 'deposit', amount, 'Deposit')
        )
        conn.commit()
        return jsonify({'account_id': account_id, 'new_balance': str(new_balance)}), 200
    except Exception as exc:
        conn.rollback()
        return jsonify({'error': str(exc)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.get_json() or {}
    user_id = data.get('user_id')
    amount = data.get('amount')
    if not user_id or amount is None:
        return jsonify({'error': 'user_id and amount are required'}), 400
    if amount <= 0:
        return jsonify({'error': 'amount must be positive'}), 400

    conn = get_connection()
    try:
        cursor = conn.cursor()
        row = query_one(cursor, 'SELECT id, balance FROM accounts WHERE user_id = %s FOR UPDATE', (user_id,))
        if not row:
            return jsonify({'error': 'account not found'}), 404

        account_id, balance = row
        balance = Decimal(balance)
        if balance < Decimal(amount):
            return jsonify({'error': 'insufficient funds'}), 400

        new_balance = balance - Decimal(amount)
        cursor.execute('UPDATE accounts SET balance = %s WHERE id = %s', (new_balance, account_id))
        cursor.execute(
            'INSERT INTO transactions (account_id, type, amount, description) VALUES (%s, %s, %s, %s)',
            (account_id, 'withdraw', amount, 'Withdrawal')
        )
        conn.commit()
        return jsonify({'account_id': account_id, 'new_balance': str(new_balance)}), 200
    except Exception as exc:
        conn.rollback()
        return jsonify({'error': str(exc)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/transfer', methods=['POST'])
def transfer():
    data = request.get_json() or {}
    source_user_id = data.get('source_user_id')
    target_user_id = data.get('target_user_id')
    amount = data.get('amount')
    if not source_user_id or not target_user_id or amount is None:
        return jsonify({'error': 'source_user_id, target_user_id and amount are required'}), 400
    if amount <= 0:
        return jsonify({'error': 'amount must be positive'}), 400
    if source_user_id == target_user_id:
        return jsonify({'error': 'source and target must differ'}), 400

    conn = get_connection()
    try:
        cursor = conn.cursor()
        source = query_one(cursor, 'SELECT id, balance FROM accounts WHERE user_id = %s FOR UPDATE', (source_user_id,))
        target = query_one(cursor, 'SELECT id, balance FROM accounts WHERE user_id = %s FOR UPDATE', (target_user_id,))

        if not source or not target:
            return jsonify({'error': 'source or target account not found'}), 404

        source_id, source_balance = source
        target_id, target_balance = target
        source_balance = Decimal(source_balance)
        if source_balance < Decimal(amount):
            return jsonify({'error': 'insufficient funds'}), 400

        new_source_balance = source_balance - Decimal(amount)
        new_target_balance = Decimal(target_balance) + Decimal(amount)

        cursor.execute('UPDATE accounts SET balance = %s WHERE id = %s', (new_source_balance, source_id))
        cursor.execute('UPDATE accounts SET balance = %s WHERE id = %s', (new_target_balance, target_id))

        cursor.execute(
            'INSERT INTO transactions (account_id, type, amount, related_account_id, description) VALUES (%s, %s, %s, %s, %s)',
            (source_id, 'transfer_out', amount, target_id, f'Transfer to user {target_user_id}')
        )
        cursor.execute(
            'INSERT INTO transactions (account_id, type, amount, related_account_id, description) VALUES (%s, %s, %s, %s, %s)',
            (target_id, 'transfer_in', amount, source_id, f'Transfer from user {source_user_id}')
        )
        conn.commit()
        return jsonify({
            'source_account_id': source_id,
            'source_balance': str(new_source_balance),
            'target_account_id': target_id,
            'target_balance': str(new_target_balance)
        }), 200
    except Exception as exc:
        conn.rollback()
        return jsonify({'error': str(exc)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/balance/<int:user_id>', methods=['GET'])
def balance(user_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        row = query_one(cursor, 'SELECT balance FROM accounts WHERE user_id = %s', (user_id,))
        if not row:
            return jsonify({'error': 'account not found'}), 404
        return jsonify({'user_id': user_id, 'balance': str(row[0])}), 200
    finally:
        cursor.close()
        conn.close()


@app.route('/transactions/<int:user_id>', methods=['GET'])
def transactions(user_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        row = query_one(cursor, 'SELECT id FROM accounts WHERE user_id = %s', (user_id,))
        if not row:
            return jsonify({'error': 'account not found'}), 404
        account_id = row[0]
        rows = query_all(cursor, 'SELECT id, type, amount, related_account_id, description, created_at FROM transactions WHERE account_id = %s ORDER BY created_at DESC', (account_id,))
        data = [
            {
                'id': tx[0],
                'type': tx[1],
                'amount': str(tx[2]),
                'related_account_id': tx[3],
                'description': tx[4],
                'created_at': tx[5].isoformat() if hasattr(tx[5], 'isoformat') else str(tx[5])
            }
            for tx in rows
        ]
        return jsonify({'user_id': user_id, 'transactions': data}), 200
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
